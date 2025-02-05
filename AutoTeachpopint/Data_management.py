import os
import sys
import attr
from typing import Optional, Union, List

sys.path.append('../')
sys.path.append("Actions")
sys.path.append("Protocols")

#from AutoTeachpoint import Teach

@attr.s
class Coordinate:
    x: Union[float] = attr.ib(validator=attr.validators.instance_of((float)))
    y: Union[float] = attr.ib(validator=attr.validators.instance_of((float)))
    z: Union[float] = attr.ib(validator=attr.validators.instance_of((float)))
    
    def coordinates(self):
        return {"x": self.x, "y": self.y, "z": self.z}
    
    def sum_coordinates(self, other):
        result_x = self.x + other.x
        result_y = self.y + other.y
        result_z = self.z + other.z
        return Coordinate(result_x, result_y, result_z)
    
    def subtract_coordinates(self, other):
        result_x = self.x + other.x
        result_y = self.y + other.y
        result_z = self.z + other.z
        return Coordinate(result_x, result_y, result_z)
    
    def subtract_coordinates_to_move(self, other):
        result_x = self.x - other.x
        result_y = self.y - other.y
        result_z = self.z - other.z
        return {"x": result_x, "y": result_y, "z": result_z}
    
@attr.s
class Result:
    x: List[float] = attr.ib(default=[])
    y: List[float] = attr.ib(default=[])
    z: List[float] = attr.ib(default=[])

@attr.s
class Station:
    name: str = attr.ib()
    gauge_origine: Coordinate = attr.ib(factory=lambda: Coordinate(0.0, 0.0, 0.0))           #similar to result_avr but with out the hole step down
    probe_origine: Coordinate = attr.ib(factory=lambda: Coordinate(0.0, 0.0, 0.0))
    offset_gripper_probe: Coordinate = attr.ib(factory=lambda: Coordinate(0.0, 0.0, 0.0))
    offset_gauge_station: Coordinate = attr.ib(factory=lambda: Coordinate(0.0, 0.0, 0.0))
    offset_gauge: Coordinate = attr.ib(factory=lambda: Coordinate(0.0, 0.0, 0.0))        #the offset of the center hole to check the probe
    check: Coordinate = attr.ib(factory=lambda: Coordinate(0.0, 0.0, 0.0))
    result_avr: Coordinate = attr.ib(factory=lambda: Coordinate(0.0, 0.0, 0.0))
    skew_origine: Coordinate = attr.ib(factory=lambda: Coordinate(0.0, 0.0, 0.0))
    gripper_center: Coordinate = attr.ib(factory=lambda: Coordinate(0.0, 0.0, 0.0))
    #result_all: Result = attr.ib(default=Result())

class Data_storage:
    #hole_step = Teach.hole_step
    #num_measures = Teach.num_measures
    hole_step = 1.6
    gripper_to_probe_x = 56
    gripper_stepperbase = 60
    hole_to_wall_x_SNTH_LID = 45
    hole_to_wall_y_SNTH_LID  = 42
    hole_to_wall_x_pr = 60 ###CHECK
    hole_to_wall_y_pr = 40 ###CHECK
    probe_height = 67
    old_gauge_height = 19   #the old teachpoint gauge height
    plate_height_pickup = 19 - 7 #plate height minus offset to pick up
    new_gauge_height = 14
    gauge_origine_to_gasket = new_gauge_height - hole_step
    gauge_offset = (55.0, 0.0, -2.0)
    correction_offset = (-0.4, 0.1, 0.0)
    z_hop_step_move_correction = Coordinate(0.0, 0.0, hole_step/2)
    extra_station = Coordinate(0.0, 0.0, 0.0)
    #SYNTH OFSSETS
    wall_to_center_x_synth = 128/2
    wall_to_center_y_synth = 85.8/2
    #LID OFFSETS
    wall_to_center_x_lid = 128.5/2
    wall_to_center_y_lid = 85.8/2
    #PLATE READER OFSSETS
    wall_to_center_x_pr = 129/2
    wall_to_center_y_pr = 86.3/2
    z_offset = probe_height + gauge_origine_to_gasket - gripper_stepperbase - old_gauge_height

    synth = Station(
        name="Synthesis",
        probe_origine=Coordinate(352.0, 6.0, 63.0),
        check=Coordinate(352.0, 6.0, 63.0),
        offset_gripper_probe=Coordinate(gripper_to_probe_x + wall_to_center_x_synth - hole_to_wall_x_SNTH_LID + correction_offset[0], hole_to_wall_y_SNTH_LID - wall_to_center_y_synth + correction_offset[1], z_offset + correction_offset[2]),
        offset_gauge_station=Coordinate(0.0, 0.0, 0.0),
        offset_gauge=Coordinate(*gauge_offset)
    )
    vts = Station(
        name="VTS",
        probe_origine=Coordinate(528.7, 5.4, 71.0),
        check=Coordinate(528.7, 5.4, 71.0),
        offset_gripper_probe=Coordinate(gripper_to_probe_x + wall_to_center_x_lid - hole_to_wall_x_SNTH_LID, hole_to_wall_y_SNTH_LID - wall_to_center_y_lid, z_offset),
        offset_gauge_station=Coordinate(0.0, 0.0, 0.0),
        offset_gauge=Coordinate(*gauge_offset)
    )
    dkn = Station(
        name="Dockin",
        probe_origine=Coordinate(6.1, 5.9, 71.0),
        check=Coordinate(6.1, 5.9, 75.0),
        offset_gripper_probe=Coordinate(gripper_to_probe_x + wall_to_center_x_lid - hole_to_wall_x_SNTH_LID, hole_to_wall_y_SNTH_LID - wall_to_center_y_lid, z_offset),
        offset_gauge_station=Coordinate(0.0, 0.0, 0.0),
        offset_gauge=Coordinate(*gauge_offset)
    )
    pr = Station(
        name="Plate Reader",
        probe_origine=Coordinate(9.1, 57.3, 0.0),
        check=Coordinate(9.1, 57.3, 0.0),
        offset_gripper_probe=Coordinate(gripper_to_probe_x + wall_to_center_x_pr - hole_to_wall_x_pr, hole_to_wall_y_pr - wall_to_center_y_pr, z_offset), ##########Check this: with of plate reader pocket/2 - 45
        offset_gauge_station=Coordinate(0.0, 0.0, 0.0),
        offset_gauge=Coordinate(*gauge_offset)
    )

class Correction:
    
    def gripper_skew_correction(self, targetstation: Station):    ####################################################################### DO THIS
        targetstation.gripper_center.x = targetstation.result_avr.x + targetstation.offset_gripper_probe.x * 
        targetstation.gripper_center.y = targetstation.result_avr.y + targetstation.offset_gripper_probe.y * 
        targetstation.gripper_center.z = targetstation.result_avr.z + targetstation.offset_gripper_probe.z * 
           
        return targetstation
    
    def station_skew_correction(self, targetstation: Station):    ####################################################################### DO THIS
        targetstation.gripper_center.x = targetstation.gripper_center.x + targetstation.offset_gauge_station.x * 
        targetstation.gripper_center.y = targetstation.gripper_center.y + targetstation.offset_gauge_station.y * 
        targetstation.gripper_center.z = targetstation.gripper_center.z + targetstation.offset_gauge_station.z * 
           
        return targetstation
    
class Results:

    # Save the results to a file
    def save_result(self, file_name, results_save):
        try:
            # Get the current working directory
            current_directory = os.getcwd()
            # Specify the subdirectory name
            subdirectory = "results"
            # Create the full path to the subdirectory and file
            full_path = os.path.join(current_directory, subdirectory, file_name)
            # Create the results subdirectory if it doesn't exist
            if not os.path.exists(os.path.join(current_directory, subdirectory)):
                os.makedirs(os.path.join(current_directory, subdirectory))

            # print(f"Output has been saved to '{full_path}'")
            with open(full_path, 'w') as file:
                # Now, any print statements will write to the file
                file.write("These are the results from the teachpoints:\n")
                file.write(f"Station and axi: {file_name}\n")
                file.write(f"Distances Touched: {results_save}\n")
                
            # Restore the standard output
            sys.stdout = sys.__stdout__
            print(f"Output has been saved to '{full_path}'")
            
        except Exception as e:
                print(f"Error saving results: {e}")



    def save_origin_station_pos(self, file_name, pos_save: Coordinate, debug = False):
        results = pos_save.coordinates()
        
        if debug: print(results, results.x, results.y, results.z, type(results))
        
        # Get the current working directory
        current_directory = os.getcwd()

        # Specify the subdirectory name
        subdirectory = "results"

        # Create the full path to the subdirectory and file
        full_path = os.path.join(current_directory, subdirectory, file_name)

        # Create the results subdirectory if it doesn't exist
        if not os.path.exists(os.path.join(current_directory, subdirectory)):
            os.makedirs(os.path.join(current_directory, subdirectory))

        # Open a file in write mode ('w')
        with open(full_path, 'w') as file:
            # Redirect standard output to the file
            sys.stdout = file

            # Now, any print statements will write to the file
            print("This is the origine position for the station:")
            print("        \"X\":", str(results["x"]), ",")
            print("        \"Y\":", str(results["y"]), ",")
            print("        \"Z\":", str(results["z"]))

        # Restore the standard output
        sys.stdout = sys.__stdout__

        print(f"Output has been saved to '{full_path}'")


    # Print results.
    def print_results(self, results_print):
        # print(results)
        for encoder, dist in zip(results_print["encoder_pos"], results_print["dist_touch"]):
            print("Encoder Position:", encoder, "Distance Touch:", dist)
            
    def make_teachpoin_overlay(self, storage: Data_storage):
        data = storage
        # Get the current working directory
        current_directory = os.getcwd()

        # Specify the subdirectory name
        subdirectory = "results"

        # Create the full path to the subdirectory and file
        full_path = os.path.join(current_directory, subdirectory, "overlay_teachpoint")

        # Create the results subdirectory if it doesn't exist
        if not os.path.exists(os.path.join(current_directory, subdirectory)):
            os.makedirs(os.path.join(current_directory, subdirectory))

        # Open a file in write mode ('w')
        with open(full_path, 'w') as file:
            # Redirect standard output to the file
            sys.stdout = file

            # Now, any print statements will write to the file
            print("{\n     \"SynthesisStationReference\": {")
            print("         \"X\": ", str(data.synth.gripper_center.x), ",")
            print("         \"Y\": ", str(data.synth.gripper_center.y), ",")
            print("         \"Z\": ", str(data.synth.gripper_center.z))
            print("     },")
            print("     \"VTSLidReference\": {")
            print("         \"X\": ", str(data.vts.gripper_center.x), ",")
            print("         \"Y\": ", str(data.vts.gripper_center.y), ",")
            print("         \"Z\": ", str(data.vts.gripper_center.z))
            print("     },")
            print("     \"DockingStationLidReference\": {")
            print("         \"X\": ", str(data.dkn.gripper_center.x), ",")
            print("         \"Y\": ", str(data.dkn.gripper_center.y), ",")
            print("         \"Z\": ", str(data.dkn.gripper_center.z))
            print("     },")
            print("     \"PlateReader\": {")
            print("         \"X\": ", str(data.pr.gripper_center.x), ",")
            print("         \"Y\": ", str(data.pr.gripper_center.y), ",")
            print("         \"Z\": ", str(data.pr.gripper_center.z))
            print("     }\n}")

        # Restore the standard output
        sys.stdout = sys.__stdout__

        print(f"Output has been saved to '{full_path}'")


# if __name__ == '__main__':
    # test_data = Data_storage
    # correction = Correction()
    # print(correction.correlation_gripper(test_data.synth))
    # print(test_data.synth.gauge_origine.items)
