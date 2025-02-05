import sys
sys.path.append('../')
sys.path.append("Actions")
sys.path.append("Protocols")

from Hardware import Hardware
from Actions.FluidicActions import Fluidic
from Actions.DispenseActions import Dispense
import time

START_COLUMN=1
STOP_COLUMN=12

EL_PRIMED = False
HPURE = False

hw=Hardware()
fluidic_actions=Fluidic(hw)
dispense_actions=Dispense(hw)

def Prewash(prime=True):

    global EL_PRIMED

    print("Begin Prewash")

    # synthesis_96 in on the SYN station
    # lid+Desalt_96 plate are on the DOCK station at this point
    # oligo_96 is in the VTS

    hw.gripper.grip_go_to_pos("Home")
    # => Gripper is at "Home" position

    # Heater at 46°C
    hw.synth_heater.set_temp(46)
    hw.synth_heater.enable()
    hw.synth_heater.wait_setpoint()

    # -----------------------------------
    # Prime W3 through pump 5 ("EB" line)
    # -----------------------------------
    fluidic_actions.connect_pump_to_rotary_bottle("EB", "W3")
    if prime:
        fluidic_actions.prime_pump(reagent="EB")

    # -----------------------------------
    # Prime EL through pump 8 (direct circuit)
    # -----------------------------------
    fluidic_actions.close_reagent_valves()
    if prime:
        fluidic_actions.prime_pump(reagent="EL")
        EL_PRIMED = True

    # ***********************************
    # EL dispense (direct circuit, pump 8)
    # ***********************************
    fluidic_actions.close_reagent_valves()
        # Dispense 1
    dispense_actions.dispense_full_plate_96(reagent="EL", volume=50, location="SYN_NZL", stackable = ["synthesis_96"],
                                    start_column=START_COLUMN, end_column=STOP_COLUMN,
                                    fill_speed=40000)

    hw.synth_shaker.shake(50, 30)
    hw.vacuum.vacuum_synth(kPa=-40, duration=30)
        # Dispense 2
    dispense_actions.dispense_full_plate_96(reagent="EL", volume=50, location="SYN_NZL", stackable = ["synthesis_96"],
                                    start_column=START_COLUMN, end_column=STOP_COLUMN,
                                    fill_speed=40000)

    hw.synth_shaker.shake(50, 30)
    hw.vacuum.vacuum_synth(kPa=-40, duration=30)

    # ***********************************
    # W3 dispense (rotary circuit, pump 5 ("EB" line))
    # ***********************************
    fluidic_actions.connect_pump_to_rotary_bottle("EB", "W3")
        # Dispense 1
    dispense_actions.dispense_full_plate_96(reagent="EB", volume=100, location="SYN_NZL", stackable = ["synthesis_96"],
                                    start_column=START_COLUMN, end_column=STOP_COLUMN,
                                    fill_speed=40000)

    hw.synth_shaker.shake(33, 300)
    hw.vacuum.vacuum_synth(kPa=-40, duration=30)
        # Dispense 2
    dispense_actions.dispense_full_plate_96(reagent="EB", volume=100, location="SYN_NZL", stackable = ["synthesis_96"],
                                    start_column=START_COLUMN, end_column=STOP_COLUMN,
                                    fill_speed=40000)

    hw.synth_shaker.shake(33, 300)
    hw.vacuum.vacuum_synth(kPa=-40, duration=30)

    # ***********************************
    # EL dispense (direct circuit, pump 8)
    # ***********************************
    fluidic_actions.close_reagent_valves()
        # Dispense 1
    dispense_actions.dispense_full_plate_96(reagent="EL", volume=50, location="SYN_NZL", stackable = ["synthesis_96"],
                                    start_column=START_COLUMN, end_column=STOP_COLUMN,
                                    fill_speed=40000)

    hw.synth_shaker.shake(50, 30)
    hw.vacuum.vacuum_synth(kPa=-40, duration=30)
        # Dispense 2
    dispense_actions.dispense_full_plate_96(reagent="EL", volume=50, location="SYN_NZL", stackable = ["synthesis_96"],
                                    start_column=START_COLUMN, end_column=STOP_COLUMN,
                                    fill_speed=40000)

    hw.synth_shaker.shake(50, 30)
    hw.vacuum.vacuum_synth(kPa=-40, duration=30)

    # -----------------------------------
    # Prime W8 (Water) through pump 4 ("dT" line)
    # -----------------------------------
    fluidic_actions.connect_pump_to_rotary_bottle("dT", "W8")
    if prime:
        fluidic_actions.prime_pump(reagent="dT")

    # -----------------------------------
    # Prime W1 through pump 4 ("dT" line)
    # -----------------------------------
    fluidic_actions.connect_pump_to_rotary_bottle("dT", "W1")
    if prime:
        fluidic_actions.prime_pump(reagent="dT")

    # Heater at 55°C
    hw.synth_heater.set_temp(55)
    hw.synth_heater.enable()
    hw.synth_heater.wait_setpoint()

    # ***********************************
    # W1 dispense (rotary circuit, pump 4 ("dT" line))
    # ***********************************
    fluidic_actions.connect_pump_to_rotary_bottle("dT", "W1")
        # Dispense 1
    dispense_actions.dispense_full_plate_96(reagent="dT", volume=50, location="SYN_NZL", stackable = ["synthesis_96"],
                                    start_column=START_COLUMN, end_column=STOP_COLUMN,
                                    fill_speed=40000)

    hw.synth_shaker.shake(0, 10)
    hw.vacuum.vacuum_synth(kPa=-40, duration=60)
        # Dispense 2
    dispense_actions.dispense_full_plate_96(reagent="dT", volume=50, location="SYN_NZL", stackable = ["synthesis_96"],
                                    start_column=START_COLUMN, end_column=STOP_COLUMN,
                                    fill_speed=40000)

    hw.synth_shaker.shake(0, 10)
    hw.vacuum.vacuum_synth(kPa=-40, duration=60)
        # Dispense 3
    dispense_actions.dispense_full_plate_96(reagent="dT", volume=50, location="SYN_NZL", stackable = ["synthesis_96"],
                                    start_column=START_COLUMN, end_column=STOP_COLUMN,
                                    fill_speed=40000)

    hw.synth_shaker.shake(0, 10)
    hw.vacuum.vacuum_synth(kPa=-40, duration=1200)

    print("End Prewash")


def Liberation(prime=True):

    print("Begin Liberation")

    # synthesis_96 in on the SYN station
    # lid+Desalt_96 plate are on the DOCK station at this point
    # oligo_96 is in the VTS

    # -----------------------------------
    # Prime LB through pump 6 ("W2" line)
    fluidic_actions.connect_pump_to_rotary_bottle("W2", "LB")
    if prime:
        fluidic_actions.prime_pump(reagent="W2")
    # -----------------------------------

    # Heater at 65°C
    hw.synth_heater.set_temp(65)
    hw.synth_heater.enable()
    hw.synth_heater.wait_setpoint()

    dispense_actions.dispense_full_plate_96(reagent="W2", volume=100, location="SYN_NZL", stackable = ["synthesis_96"],
                                    start_column=START_COLUMN, end_column=STOP_COLUMN,
                                    fill_speed=40000)

    hw.synth_shaker.shake(50, 1800)

    print("End Liberation")


def Precipitation(prime=True):

    global EL_PRIMED

    print("Begin Precipitation")

    # synthesis_96 in on the SYN station
    # lid+Desalt_96 plate are on the DOCK station at this point
    # oligo_96 is in the VTS
     
    # -----------------------------------
    # Prime W8 through pump 4 ("dT" line)
    fluidic_actions.connect_pump_to_rotary_bottle("dT", "W8")
    if prime:
        fluidic_actions.prime_pump(reagent="dT")
    # -----------------------------------

    # -----------------------------------
    # Prime W7 through pump 5 ("EB" line)
    fluidic_actions.connect_pump_to_rotary_bottle("EB", "W7")
    if prime:
        fluidic_actions.prime_pump(reagent="EB")
    # -----------------------------------

    # -----------------------------------
    # Prime W7 through pump 6 ("W2" line)
    fluidic_actions.connect_pump_to_rotary_bottle("W2", "W7")
    if prime:
        fluidic_actions.prime_pump(reagent="W2")
    # -----------------------------------

    # -----------------------------------
    # Prime W8 through pump 7 ("DB" line)
    fluidic_actions.connect_pump_to_rotary_bottle("DB", "W8")
    if prime:
        fluidic_actions.prime_pump(reagent="DB")
    # -----------------------------------

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
    # => Gripper is at "Park" position

    # -----------------------------------
    # Prime W6 (IPA) through pump 4 ("dT" line)
    fluidic_actions.connect_pump_to_rotary_bottle("dT", "W6")
    if prime:
        fluidic_actions.prime_pump(reagent="dT")
    # -----------------------------------

    # Moving the desalt_96 plate from DOCKING to VTS
    hw.gripper.move_stackable("DOCK", ["desalt_96","lid"], "desalt_96", "VTS", [])
    # => Gripper is at "VTS" position

    # Moving the synthesis_96 from SYN to DOCKING on top of lid
    hw.gripper.move_stackable("SYN", ["synthesis_96"], "synthesis_96", "DOCK", ["lid"])
    # => Gripper is at "DOCK" position
    hw.gripper.grip_go_to_pos("Home")
    # => Gripper is at "Home" position

    if EL_PRIMED == False:
        fluidic_actions.close_reagent_valves()
        if prime:
            fluidic_actions.prime_pump(reagent="EL")
            EL_PRIMED = True
            
    fluidic_actions.close_reagent_valves()
    dispense_actions.dispense_full_plate_96(reagent="EL", volume=40, location="VTS_NZL", stackable = ["desalt_96"],
                                    start_column=START_COLUMN, end_column=STOP_COLUMN,
                                    fill_speed=40000)

    fluidic_actions.connect_pump_to_rotary_bottle("dT", "W6")
    dispense_actions.dispense_full_plate_96(reagent="dT", volume=375, location="VTS_NZL", stackable = ["desalt_96"],
                                    start_column=START_COLUMN, end_column=STOP_COLUMN,
                                    fill_speed=40000)

    #   Move VTS down
    hw.vts_motor.VTS_go_to_pos("desalt_96")

    # Moving the lid (with synthesis_96) from docking to VTS
    hw.gripper.move_stackable("DOCK", ["lid"], "lid", "VTS", [])
    # => Gripper is at "VTS" position
    hw.gripper.grip_go_to_pos("Home")
    # => Gripper is at "Home" position

    hw.vacuum.vacuum_vts(kPa=-60, duration=30)

    fluidic_actions.close_reagent_valves()
    dispense_actions.dispense_full_plate_96(reagent="EL", volume=50, location="VTS_NZL", stackable = ["synthesis_96", "lid"],
                                    start_column=START_COLUMN, end_column=STOP_COLUMN,
                                    fill_speed=40000)

    hw.vacuum.vacuum_vts(kPa=-50, duration=30)

    print("End Precipitation")


def Desalting(prime=True):

    print("Begin Desalting")

    # Desalt_96 is in the VTS
    # synthesis_96 is on top of lid on the VTS
    # oligo_96 is in the READER

    # Heater at 25°C
    hw.synth_heater.set_temp(25)
    hw.synth_heater.enable()

    # Moving the synthesis_96 plate from VTS to DOCKING
    hw.gripper.move_stackable("VTS", ["synthesis_96","lid"], "synthesis_96", "DOCK", [])
    # => Gripper is at "DOCK" position

    # Moving the lid from VTS to DOCKING
    hw.gripper.move_stackable("VTS", ["lid"], "lid", "DOCK", [])
    # => Gripper is at "DOCK" position

    #   Move VTS up to park
    hw.vts_motor.VTS_go_to_pos("park")

    # Moving the desalt_96 from VTS to SYN
    hw.gripper.move_stackable("VTS", ["desalt_96"], "desalt_96", "SYN", [])
    # => Gripper is at "SYN" position

    # Opening the plate reader
    hw.gripper.grip_go_to_pos("Park")
    hw.reader.opendrawer()

    # Moving the oligo_96 plate from plate reader to the VTS
    hw.gripper.move_stackable("READER", ["oligo_96"], "oligo_96", "VTS", [])
    # => Gripper is at "VTS" position

    # Closing the plate reader
    hw.gripper.grip_go_to_pos("Park")
    hw.reader.closedrawer()

    #   Move VTS up to "oligo_96"
    hw.vts_motor.VTS_go_to_pos("oligo_96")

    # Moving the lid from DOCKING to VTS
    hw.gripper.move_stackable("DOCK", ["lid"], "lid", "VTS", [])
    # => Gripper is at "VTS" position

    hw.gripper.grip_go_to_pos("Home")
    # => Gripper is at "Home" position

    hw.synth_shaker.shake(0, 180)

    hw.vacuum.vacuum_synth(kPa=-40, duration=30)

    print("End Desalting")


def Elution(prime=True):

    global EL_PRIMED
    global HPURE

    print("Begin Elution")

    # Desalt_96 is in the SYN station
    # synthesis_96 is in the DOCK
    # oligo_96 is in the VTS
    # lid is on the VTS

    # Heater at 25°C
    hw.synth_heater.set_temp(25)
    hw.synth_heater.enable()

    #   Move VTS up to "oligo_96"
    hw.vts_motor.VTS_go_to_pos("oligo_96")

    # -----------------------------------
    # Prime W8 (Water) through pump 4 ("dT" line)
    fluidic_actions.connect_pump_to_rotary_bottle("dT", "W8")
    if prime:
        fluidic_actions.prime_pump(reagent="dT")
    # -----------------------------------

    # -----------------------------------
    # Prime W1 (Ethanol) through pump 4 ("dT" line)
    fluidic_actions.connect_pump_to_rotary_bottle("dT", "W1")
    if prime:
        fluidic_actions.prime_pump(reagent="dT")
    # -----------------------------------

    dispense_actions.dispense_full_plate_96(reagent="dT", volume=600, location="SYN_NZL", stackable = ["desalt_96"],
                                    start_column=START_COLUMN, end_column=STOP_COLUMN,
                                    fill_speed=40000)
    hw.synth_shaker.shake(0, 0)

    hw.vacuum.vacuum_synth(kPa=-60, duration=30)

    dispense_actions.dispense_full_plate_96(reagent="dT", volume=600, location="SYN_NZL", stackable = ["desalt_96"],
                                    start_column=START_COLUMN, end_column=STOP_COLUMN,
                                    fill_speed=40000)

    hw.synth_shaker.shake(0, 0)

    hw.vacuum.vacuum_synth(kPa=-60, duration=900)

    # Moving the desalt_96 plate from SYN to the VTS
    hw.gripper.move_stackable("SYN", ["desalt_96"], "desalt_96", "VTS", ["lid"])
    # => Gripper is at "VTS" position

    hw.gripper.grip_go_to_pos("Home")
    # => Gripper is at "Home" position

    if EL_PRIMED == False:
        fluidic_actions.close_reagent_valves()
        if prime:
            fluidic_actions.prime_pump(reagent="EL")
            EL_PRIMED = True
    
    if HPURE == True:
        fluidic_actions.close_reagent_valves()
        dispense_actions.dispense_full_plate_96(reagent="EL", volume=60, location="VTS_NZL", stackable = ["desalt_96","lid"],
                                        start_column=START_COLUMN, end_column=STOP_COLUMN,
                                        fill_speed=40000)

        hw.synth_shaker.shake(0, 180)        # to create a wait for 180 sec

        hw.vacuum.vacuum_vts(kPa=-60, duration=120)

    else:
        # HMASS
        fluidic_actions.close_reagent_valves()
        dispense_actions.dispense_full_plate_96(reagent="EL", volume=50, location="VTS_NZL", stackable = ["desalt_96","lid"],
                                        start_column=START_COLUMN, end_column=STOP_COLUMN,
                                        fill_speed=40000)
        
        hw.synth_shaker.shake(0, 180)        # to create a wait for 180 sec

        hw.vacuum.vacuum_vts(kPa=-60, duration=60)

        dispense_actions.dispense_full_plate_96(reagent="EL", volume=50, location="VTS_NZL", stackable = ["desalt_96","lid"],
                                        start_column=START_COLUMN, end_column=STOP_COLUMN,
                                        fill_speed=40000)
        
        hw.synth_shaker.shake(0, 30)        # to create a wait for 30 sec

        hw.vacuum.vacuum_vts(kPa=-60, duration=120)
        
    # Moving the lid from VTS to DOCKING
    hw.gripper.move_stackable("VTS", ["desalt_96","lid"], "lid", "DOCK", [])
    # => Gripper is at "DOCK" position

    #   Move VTS up to park
    hw.vts_motor.VTS_go_to_pos("park")

    # Moving the oligo_96 plate from VTS to the SYN
    hw.gripper.move_stackable("VTS", ["oligo_96"], "oligo_96", "SYN", [])
    # => Gripper is at "SYN" position

    hw.gripper.grip_go_to_pos("Home")
    # => Gripper is at "Home" position

    hw.vacuum.vacuum_synth(kPa=-40, duration=190)

    hw.synth_shaker.shake(50, 180)

    print("End Elution")

def perform_option(option):
    if option == 1:
        Prewash(prime=True)
    elif option == 2:
        Liberation(prime=True)
    elif option == 3:
        Precipitation(prime=True)
    elif option == 4:
        Desalting(prime=True)
    elif option == 5:
        Elution(prime=True)
    else:
        print("Invalid option")

if __name__ == "__main__":

    hw.home()
    hw.cooler.set_temp(10)
    hw.cooler.enable()
    #hw.cooler.activate_fans()  Done by default when enabling device

    print("PSP 96 wells FullVacuum")
    print("-----------")
    print("1: Prewash")
    print("2: Liberation")
    print("3: Precipitation")
    print("4: Desalting")
    print("5: Elution")

    while True:
        start_option = int(input("Enter the starting option (1-5): "))
        end_option = int(input("Enter the ending option (1-5): "))

        if start_option <= end_option and 1 <= start_option <= 5 and 1 <= end_option <= 5:
            if start_option == 5 or end_option == 5:
                print("1: HPURE")
                print("2: HMASS")
                psptype = int(input("Enter the PSP option (1-2): "))
                if psptype == 1:
                    HPURE = True
            for option in range(start_option, end_option + 1):
                perform_option(option)
        else:
            print("Invalid input. Please enter valid options.")

