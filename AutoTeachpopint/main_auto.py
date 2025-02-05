# Python general
import time
import sys
import os
from pprint import pprint

sys.path.append('../')
sys.path.append("Actions")
sys.path.append("Protocols")

import Teachpoint
import Data_management as data_manage

teach = Teachpoint.Teach()
data_storage = data_manage.Data_storage()
results = data_manage.Results()

teach.num_measures = 1
teach.hole_step = 1.6
teach.hole_dia = 8

# Homing and Probe activating:
###self.hw.probe.home_probe_init()
teach.hw.home()  # Delete when finish testing
#input("\n\nHello, ENTER to start\n")
teach.hw.gripper.grip_in()


##########################################

# Test each axis for Synthesis station:

input("Let's locate the synthesis station!")
data_storage.synth = teach.find_hole(data_storage.synth, False)
teach.hw.gripper.safe_z()
teach.find_hole(data_storage.synth, True)
print(data_storage.synth)
teach.hw.gripper.grip_go_to_pos("Home")


input(  "\n\n YOU HAVE SUCCESFULLY PERFORMED TEACHPOINTS IN THE SYNTHESIS STATION\n"
        " PLEASE SET EVERYHTING CORRECTLY TO PERFORM THEM IN THE VTS STATION\n"
        "    for that change the TEACHPOINT PLATE to the LID on the VTS\n"
        "                  press ENTER when ready\n")
input(  "             Thank you, press ENTER to continue")
data_storage.vts = teach.find_hole(data_storage.vts, False)
teach.hw.gripper.safe_z()
teach.find_hole(data_storage.vts, True)

teach.hw.gripper.grip_go_to_pos("Home")


input(  "\n\n     YOU HAVE SUCCESFULLY PERFORMED TEACHPOINTS IN THE VTS STATION\n"
        "  PLEASE SET EVERYHTING CORRECTLY TO PERFORM THEM IN THE DOKING STATION\n"
        " for that change the LID with the TEACHPOINT PLATE to the Doking Station\n"
        "                      press ENTER when ready\n")
input(  "               Thank you, press ENTER to continue")
data_storage.dkn = teach.find_hole(data_storage.dkn, False)
teach.hw.gripper.safe_z()
teach.find_hole(data_storage.dkn, True)
print(data_storage.dkn)


teach.hw.gripper.grip_go_to_pos("PARK")
input(  "   YOU HAVE SUCCESFULLY PERFORMED TEACHPOINTS IN THE DOKING STATION\n"
        "  PLEASE SET EVERYHTING CORRECTLY TO PERFORM THEM IN THE PLATE MOVER\n"
        "   wait for the reader to open and place the TEACHPOINT PLATEon it\n"
        "                      press ENTER when ready\n")
teach.hw.reader.opendrawer()
input(  "     Thank you, press ENTER to continue with the teachpoint process")
data_storage.pr = teach.find_center_hole(data_storage.pr)
teach.hw.gripper.grip_go_to_pos("PARK")
teach.hw.reader.closedrawer()
print(data_storage.synth)
print(data_storage.vts)
print(data_storage.dkn)


# Call the method on the instance with the correct argument
results.make_teachpoin_overlay(data_storage)
print("Overlay Configuration file successfully created.")

##########################################
#######                            #######
#######     TESTING POSITIONS      #######
#######                            #######
##########################################

teach.hw.gripper.grip_go_to_pos("Home")
teach.hw.gripper.grip_neutral()
input("\n\n           PLEASE REMOVE THE TOUCH PROBE AND PRESS\n"
      "                             ENTER\n"
      "     PLEASE MAKE SURE THE PORBE IS NOT IN THE INTRUMENT AND PRESS\n\n"
      "                             ENTER\n"
      "      TO MOVE THE GRIPPER TO THE SYNTHESIS POSITION TO VERYFY THE\n"
      "              TEACHPOINT WAS PERFORMED PROPERLY PRESS\n"
      "                             ENTER\n\n")

teach.hw.gripper.xyz_move_position(data_storage.synth.gripper_center.coordinates())
input("\n\nPress ENTER when ready to go HOME.")
teach.hw.gripper.grip_go_to_pos("Home")
input("\n\nThe plate mover will check the teachpoint in the VTS")
teach.hw.gripper.xyz_move_position(data_storage.vts.gripper_center.coordinates())
input("\n\nPress ENTER when ready to go HOME.")
teach.hw.gripper.grip_go_to_pos("Home")
input("\n\nThe plate mover will check the teachpoint in the DOCKING Station")
teach.hw.gripper.xyz_move_position(data_storage.dkn.gripper_center.coordinates())
input("\n\nPress ENTER when ready to go HOME.")
input("The plate mover will check the teachpoint in the PLATE READER")
teach.hw.gripper.grip_go_to_pos("PARK")
teach.hw.reader.opendrawer()
teach.hw.gripper.xyz_move_position(data_storage.pr.gripper_center.coordinates())
teach.hw.reader.closedrawer()
teach.hw.gripper.grip_go_to_pos("Home")



















# Probe initial measurement to initialize the probe origins.

#######
#######     HAVE TO ADD SOMETHING HERE THAT WILL SERVE TO INITIALIZE
#######     WHERE THE PROBE IS RELATED TO A GOOD NON CHANGING PLACE
#######     OF THE INSTRUMENT LIKE THE DOCKING ALUMINUM POCKET
#######

##########################################
# # Test each axis for docking station X:

# results_avr, results = teach.find_station(teach.station["dkn_pocket_x_teach"], results_avr, results, begining_move = True, num_measures)
# teach.hw.gripper.safe_z()

# print(results)
# print("RESULTS FROM Docking X")
# for encoder, dist in zip(results["encoder_pos"], results["dist_touch"]):
#     print("Encoder Position:", encoder, "Distance Touch:", dist)

# teach.save_results("Results_X_DKN.txt", results)

# teach.print_results(results)

# aver_dist = (sum(results["dist_touch"]) / len(results["dist_touch"]))
# teach.station["dkn_pocket"]["position"]["x"] = aver_dist + 5.08 + teach.tip_radius
# teach.station["dkn_pocket_y_teach"]["position"]["x"] = aver_dist + 5.08 + teach.tip_radius
# teach.station["dkn_pocket_z_teach"]["position"]["x"] = aver_dist + 13

# ##########################################
# # Test each axis for docking station Y:

# results_avr, results = teach.find_station(teach.station["dkn_pocket_y_teach"], results_avr, results, begining_move = True, num_measures)
# teach.hw.gripper.safe_z()

# print(results)
# print("RESULTS FROM Docking Y")
# for encoder, dist in zip(results["encoder_pos"], results["dist_touch"]):
#     print("Encoder Position:", encoder, "Distance Touch:", dist)

# teach.save_results("Results_Y_DKN.txt", results)

# teach.print_results(results)

# aver_dist = (sum(results["dist_touch"]) / len(results["dist_touch"]))
# teach.station["dkn_pocket"]["position"]["y"] = aver_dist - 5.72 - teach.tip_radius
# teach.station["dkn_pocket_z_teach"]["position"]["y"] = aver_dist - (11.34/2) - teach.tip_radius

# ##########################################
# # Test each axis for docking station Z:

# results_avr, results = teach.find_station(teach.station["dkn_pocket_z_teach"], results_avr, results, begining_move = True, num_measures)
# teach.hw.gripper.safe_z()

# print(results)
# print("RESULTS FROM Docking Z")
# for encoder, dist in zip(results["encoder_pos"], results["dist_touch"]):
#     print("Encoder Position:", encoder, "Distance Touch:", dist)

# teach.save_results("Results_Z_DKN.txt", results)

# teach.print_results(results)

# aver_dist = (sum(results["dist_touch"]) / len(results["dist_touch"]))
# teach.station["dkn_pocket"]["position"]["z"] = aver_dist - 4.52

# # Checking the position for the Docking origin is good.
# teach.xyz_move_position(teach.station["dkn_pocket"])
# input("Enter to go HOME")
# teach.hw.gripper.home()

