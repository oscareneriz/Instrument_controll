import sys
sys.path.append('../')
sys.path.append("Actions")
sys.path.append("Protocols")

from Hardware import Hardware
import time

hw=Hardware()

def Transport(prime=True):

    print("Begin transport sequences (384 OP)")
    # Consumables are set like for a real run
    # synthesis_384 in SYN
    # sacrificial_384 in the VTS
    # oligo_384 on top of lid on top of VTS

    # Opening the plate reader
    hw.gripper.grip_go_to_pos("Park")
    hw.reader.opendrawer()

    # Moving the oligo_384 plate from VTS to plate reader
    hw.gripper.move_stackable("VTS", ["oligo_384","lid"], "oligo_384", "READER", [])

    # Closing the plate reader
    hw.gripper.grip_go_to_pos("Park")
    hw.reader.closedrawer()

    #   Move VTS to sacrificial_384
    hw.vts_motor.VTS_go_to_pos("sacrificial_384")

    # Moving the synthesis_384 from SYN to VTS on top of lid
    hw.gripper.move_stackable("SYN", ["synthesis_384"], "synthesis_384", "VTS", ["lid"])

    # Here "remove droplets" happens in a real run

    # Moving the synthesis_384 plate from VTS to SYN
    hw.gripper.move_stackable("VTS", ["synthesis_384","lid"], "synthesis_384", "SYN", [])

    # Moving the lid from VTS to docking
    hw.gripper.move_stackable("VTS", ["lid"], "lid", "DOCK", [])

    #   Move VTS to park
    hw.vts_motor.VTS_go_to_pos("park")

    # Moving the sacrificial_384 from VTS to DOCK (on top of lid)
    hw.gripper.move_stackable("VTS", ["sacrificial_384"], "sacrificial_384", "DOCK", ["lid"])

    # Opening the plate reader
    hw.gripper.grip_go_to_pos("Park")
    hw.reader.opendrawer()

    # Moving the oligo_384 plate from plate reader to the VTS
    hw.gripper.move_stackable("READER", ["oligo_384"], "oligo_384", "VTS", [])

    # Closing the plate reader
    hw.gripper.grip_go_to_pos("Park")
    hw.reader.closedrawer()

    #   Move VTS to oligo_384
    hw.vts_motor.VTS_go_to_pos("oligo_384")

    # Moving the lid from DOCKING to VTS (with sacrificial_384 on top)
    hw.gripper.move_stackable("DOCK", ["sacrificial_384","lid"], "lid", "VTS", [])

    # Moving the sacrificial_384 plate from VTS to the DOCK
    hw.gripper.move_stackable("VTS", ["sacrificial_384","lid"], "sacrificial_384", "DOCK", [])

    # Moving the synthesis_384 plate from SYN to VTS
    hw.gripper.move_stackable("SYN", ["synthesis_384"], "synthesis_384", "VTS", ["lid"])

    # Here "elution" and "remove droplets" happens in a real run

    # Moving the lid from VTS to DOCKING (with synthesis_384 on top)
    hw.gripper.move_stackable("VTS", ["synthesis_384","lid"], "lid", "DOCK", [])

    #   Move VTS to park
    hw.vts_motor.VTS_go_to_pos("park")

    # Moving the oligo_384 plate from VTS to the SYN
    hw.gripper.move_stackable("VTS", ["oligo_384"], "oligo_384", "SYN", [])

    # Here "tapping" happens in a real run + quantification

    # Moving the lid from DOCKING to VTS (with synthesis on top)
    hw.gripper.move_stackable("DOCK", ["synthesis_384","lid"], "lid", "VTS", [])

    # Moving the sacrificial_384 plate from DOCKING to VTS (with lid and synthesis_384 on top)
    hw.gripper.move_stackable("DOCK", ["sacrificial_384"], "sacrificial_384", "VTS", ["synthesis_384","lid"])

    hw.gripper.grip_go_to_pos("Home")

    print("End transport sequences")

if __name__ == "__main__":

    hw.home()
    input("Press Enter key to start Transport sequences")
    Transport()
        

