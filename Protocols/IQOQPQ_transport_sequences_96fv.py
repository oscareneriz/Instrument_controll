import sys
sys.path.append('../')
sys.path.append("Actions")
sys.path.append("Protocols")

from Hardware import Hardware
import time

hw=Hardware()

def Transport(prime=True):

    print("Begin transport sequences (96 FV)")
    # Consumables are set like for a real run
    # synthesis_96 in SYN
    # oligo_96 in the VTS
    # desalt_96 on top of lid on top of VTS

    # Move lid + desalt_96 on DOCK
    hw.gripper.move_stackable("VTS", ["desalt_96","lid"], "lid", "DOCK", [])
    
    # Opening the plate reader
    hw.gripper.grip_go_to_pos("Park")
    hw.reader.opendrawer()

    # Moving the oligo_96 plate from VTS to plate reader
    #   Move VTS up to park
    hw.vts_motor.VTS_go_to_pos("park")
    hw.gripper.move_stackable("VTS", ["oligo_96"], "oligo_96", "READER", [])

    # Closing the plate reader
    hw.gripper.grip_go_to_pos("Park")
    hw.reader.closedrawer()

    # Moving the desalt_96 plate from DOCKING to VTS
    hw.gripper.move_stackable("DOCK", ["desalt_96","lid"], "desalt_96", "VTS", [])

    # Moving the synthesis_96 from SYN to DOCKING on top of lid
    hw.gripper.move_stackable("SYN", ["synthesis_96"], "synthesis_96", "DOCK", ["lid"])

    #   Move VTS down
    hw.vts_motor.VTS_go_to_pos("desalt_96")

    # Moving the lid (with synthesis_96) from docking to VTS
    hw.gripper.move_stackable("DOCK", ["synthesis_96","lid"], "lid", "VTS", [])

    # Moving the synthesis_96 plate from VTS to DOCKING
    hw.gripper.move_stackable("VTS", ["synthesis_96","lid"], "synthesis_96", "DOCK", [])

    # Moving the lid from VTS to DOCKING
    hw.gripper.move_stackable("VTS", ["lid"], "lid", "DOCK", [])

    #   Move VTS up to park
    hw.vts_motor.VTS_go_to_pos("park")

    # Moving the desalt_96 from VTS to SYN
    hw.gripper.move_stackable("VTS", ["desalt_96"], "desalt_96", "SYN", [])

    # Opening the plate reader
    hw.gripper.grip_go_to_pos("Park")
    hw.reader.opendrawer()

    # Moving the oligo_96 plate from plate reader to the VTS
    hw.gripper.move_stackable("READER", ["oligo_96"], "oligo_96", "VTS", [])

    # Closing the plate reader
    hw.gripper.grip_go_to_pos("Park")
    hw.reader.closedrawer()

    #   Move VTS up to oligo_96
    hw.vts_motor.VTS_go_to_pos("oligo_96")

    # Moving the lid from DOCKING to VTS
    hw.gripper.move_stackable("DOCK", ["lid"], "lid", "VTS", [])

    # Moving the desalt_96 plate from SYN to the VTS
    hw.gripper.move_stackable("SYN", ["desalt_96"], "desalt_96", "VTS", ["lid"])

    # Moving the lid from VTS to DOCKING
    hw.gripper.move_stackable("VTS", ["desalt_96","lid"], "lid", "DOCK", [])

    #   Move VTS up to park
    hw.vts_motor.VTS_go_to_pos("park")

    # Moving the oligo_96 plate from VTS to the SYN
    hw.gripper.move_stackable("VTS", ["oligo_96"], "oligo_96", "SYN", [])

    # Moving the lid from DOCKING to VTS
    hw.gripper.move_stackable("DOCK", ["desalt_96","lid"], "lid", "VTS", [])

    # Moving the synthesis_96 plate from DOCKING to VTS
    hw.gripper.move_stackable("DOCK", ["synthesis_96"], "synthesis_96", "VTS", ["desalt_96","lid"])

    hw.gripper.grip_go_to_pos("Home")

    print("End transport sequences")

if __name__ == "__main__":

    hw.home()
    input("Press Enter key to start Transport sequences")
    Transport()
        

