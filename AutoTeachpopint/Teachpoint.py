# Python general
import time
import sys
import math
import copy

sys.path.append('../')
sys.path.append("Actions")
sys.path.append("Protocols")
sys.path.append("Eden_AutoTeachpopin")

# Project specific
import Hardware
import Gripper
import Data_management

class Teach:
    results_lib = Data_management.Results()
    correction = Data_management.Correction()
    data_storage = Data_management.Data_storage()
    hw = Hardware.Hardware()
    positive = True
    negative = False
    tip_radius = 1
    hole_dia = 8
    hole_step = 1.6
    num_measures = 1
    z_backstep = hole_step/2
    dist_backup = hole_dia/3
    
    ################################
    #   Get values from stations   #
    ################################

    # Loops reading probe to find wall.
    def find_wall(self, axis: Gripper.Stepper):
        wall_found = False
        encoder_pos = 0
        dist_touch = 0.0
        # print("Finding wall")
        while not wall_found:
            read = self.hw.probe.read_probe()
            if read == 0:
                encoder_pos = int(axis.read_encoder_pos())
                axis.motor_stop()
                dist_touch = encoder_pos / axis.CONVERSION_MM
                # print("Encoder read:", encoder_pos)
                # print("X or Y displacement position:", dist_touch)
                wall_found = True
        # print("My face hurts!!! I found the wall")
        return encoder_pos, dist_touch



    # For a starting position and a direction it finds the distance for the axis.
    def glide_axis(self, axis: Gripper.Stepper, direction, dist_backup=1, num_measures=3):
        # print("Moooooooving to the infinite and further awayyyy!!!!!")
        encoder_pos = []
        dist_touch = []
        for i in range(num_measures):
            # Setting speed low to use the probe.
            self.hw.gripper.speed_home()

            # Selects movement direction to glide in the axis.
            if direction:
                print("pos")
                self.hw.gripper.move_positive(axis, 25)
            else:
                print("neg")
                self.hw.gripper.move_negative(axis, 25)

            # Finds the wall and distance for the given axis.
            encoder, dist = self.find_wall(axis)
            encoder_pos.append(encoder)
            dist_touch.append(dist)
            
            # Setting speed back to normal.
            self.hw.gripper.speed_normal()

            if i < num_measures:
                self.hw.gripper.backup_safe(axis, direction, dist_backup)
                time.sleep(0.35)

            
        return dist_touch

    def measure_wall(self, axis, direction, file_name, num_measures=3, dist_backup = 5):
        #Getting the measurements
        dist_touch = self.glide_axis(axis, direction, dist_backup, num_measures)
        print(dist_touch)

        #Average the results
        dist_avr = sum(dist_touch)/num_measures

        #self.results_lib.save_results(file_name, axis, dists_touch, num_measures)

        return dist_avr

    def avr_bilateral_axes(self, axi: Gripper.Stepper, file_name, dist_backup=1, num_measures=3):
        dist_pos = self.measure_wall(axi, self.positive, "positive_"+file_name, num_measures, dist_backup)
        time.sleep(0.25)
        dist_neg = self.measure_wall(axi, self.negative, "negative_"+file_name, num_measures, dist_backup)
        time.sleep(1)
        dist_center = (dist_pos + dist_neg)/2
        return dist_center
    ##################################################################################################################################################################################### wait times changed  from 0.5 and 2
    
    def skew_calculator(self, targetstation: Data_management.Station):
        axis_variation = targetstation.gauge_origine.subtract_coordinates(targetstation.skew_origine)
        print(axis_variation.x, axis_variation.y,type(axis_variation.x), type(axis_variation.y))
        print(axis_variation.y/axis_variation.x)
        angle_skewed = math.asin(axis_variation.y/axis_variation.x)*180/math.pi
        print("Axis ", targetstation.name, "skew: ")
        print("Axes variation: ", axis_variation)
        print("Angle skewed: ", angle_skewed)
        return
        
    
    def find_hole(self, targetstation: Data_management.Station, skew = False, debug = False):      #skew = FAlse when we do not want to test for skew
        if skew:
            targetstation.check = targetstation.probe_origine.sum_coordinates(targetstation.offset_gauge)
        else:
            targetstation.check = copy.deepcopy(targetstation.probe_origine)

        #FINDING Z HIGHT #################################################
        # Set the speed to regular movement speed
        self.hw.gripper.speed_normal()
        
        # Move to start position.
        self.hw.gripper.xyz_move_position(targetstation.check.coordinates())
        
        # Glide and find the position of side of hole.
        targetstation.result_avr.z = self.measure_wall(self.hw.gripper.z_axis, self.positive, "Results_Z_"+targetstation.name+".txt", self.num_measures, self.z_backstep)

        # Update center Z position.
        targetstation.check.z = targetstation.result_avr.z

        #Save Z center results.
        self.results_lib.save_result("Result_Z_"+targetstation.name+".txt", targetstation.result_avr.z, self.num_measures)
        
        
        #FINDING X CENTER#################################################
        #Measure and Compute center for X and update center X position. 
        targetstation.result_avr.x = self.avr_bilateral_axes(self.hw.gripper.x_axis, "results_x_"+targetstation.name+"_side.txt", self.dist_backup, self.num_measures)
        targetstation.check.x = targetstation.result_avr.x

        #Save X center results.
        self.results_lib.save_result("Result_X_"+targetstation.name+".txt", targetstation.result_avr.x, self.num_measures)

        #Move to center position
        if debug: print(targetstation.check, targetstation.check.subtract_coordinates_to_move(self.data_storage.z_hop_step_move_correction))
        self.hw.gripper.xyz_move_position(targetstation.check.subtract_coordinates_to_move(self.data_storage.z_hop_step_move_correction))


        #FINDING Y CENTER#################################################
        #Measure and Compute center of Y and update center Y position. 
        targetstation.result_avr.y = self.avr_bilateral_axes(self.hw.gripper.y_axis, "results_y_"+targetstation.name+"_side.txt", self.dist_backup, self.num_measures)
        targetstation.check.y = targetstation.result_avr.y

        #Save Y center results.
        self.results_lib.save_result("Result_Y_"+targetstation.name+".txt", targetstation.result_avr.y, self.num_measures)


        #Move to center of the hole.
        self.hw.gripper.xyz_move_position(targetstation.result_avr.coordinates())
        
        #Go home
        input("Center of the big hole. Press ENTER to go HOME")
        self.hw.gripper.safe_z()
        self.hw.gripper.grip_go_to_pos("Home")

        #Compute and save skew of station
        if skew:
            targetstation.skew_origine = copy.deepcopy(targetstation.result_avr)
            self.skew_calculator(targetstation)
            print("Hello, world!")
            print("These is the origine position for the station:")
            xyzpositions = targetstation.result_avr.coordinates()
            print("X position:", str(xyzpositions["x"]))
            print("Y position:", str(xyzpositions["y"]))
            print("Z position:", str(xyzpositions["z"]))
        #Save the value of the center of the station.
        else:
            targetstation.gauge_origine = copy.deepcopy(targetstation.result_avr)
            self.results_lib.save_origin_station_pos(""+targetstation.name+"_Origin_probe", targetstation.gauge_origine)

        #Add offsets to the probe centered values, to get gripper centered values. 
        targetstation = self.correction.correlation_gripper(targetstation)
        #Apply offset from skew to gripper centered values
        targetstation = self.correction.skew_correction(targetstation)  ####################################################################### DO THIS
        
        #Save final output of the station centered in the gripper to use directly for teachpoints
        self.results_lib.save_origin_station_pos(""+targetstation.name+"_Origin_gripper", targetstation.gripper_center)

        return  targetstation