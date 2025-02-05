import sys
sys.path.append('../')
sys.path.append("Actions")
sys.path.append("Protocols")

from Hardware import Hardware
from Actions.FluidicActions import Fluidic
from Actions.DispenseActions import Dispense
import time

START_COLUMN=1
STOP_COLUMN=24

EL_PRIMED = False

hw=Hardware()
fluidic_actions=Fluidic(hw)
dispense_actions=Dispense(hw)

def Prewash(prime=True):

    global EL_PRIMED

    print("Begin Prewash")

    # synthesis_384 in on the SYN station
    # lid+oligo_384 plate are on the VTS station at this point
    # sacrificial_384 is in the VTS

    # Opening the plate reader
    hw.gripper.grip_go_to_pos("Park")
    hw.reader.opendrawer()

    # Moving the oligo_384 plate from VTS to plate reader
    hw.gripper.move_stackable("VTS", ["oligo_384","lid"], "oligo_384", "READER", [])

    # Closing the plate reader
    hw.gripper.grip_go_to_pos("Park")
    hw.reader.closedrawer()
    # => Gripper is at "Park" position

    #   Move VTS up to sacrificial_384
    hw.vts_motor.VTS_go_to_pos("sacrificial_384")

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
    dispense_actions.dispense_full_plate_384(reagent="EL", volume=25, location="SYN_NZL", stackable = ["synthesis_384"],
                                    start_column=START_COLUMN, end_column=STOP_COLUMN,
                                    fill_speed=40000)

    hw.synth_shaker.shake(33, 30)
    hw.vacuum.vacuum_synth(kPa=-40, duration=30)
        # Dispense 2
    dispense_actions.dispense_full_plate_384(reagent="EL", volume=25, location="SYN_NZL", stackable = ["synthesis_384"],
                                    start_column=START_COLUMN, end_column=STOP_COLUMN,
                                    fill_speed=40000)

    hw.synth_shaker.shake(33, 30)
    hw.vacuum.vacuum_synth(kPa=-40, duration=30)

    # ***********************************
    # W3 dispense (rotary circuit, pump 5 ("EB" line))
    # ***********************************
    fluidic_actions.connect_pump_to_rotary_bottle("EB", "W3")
        # Dispense 1
    dispense_actions.dispense_full_plate_384(reagent="EB", volume=50, location="SYN_NZL", stackable = ["synthesis_384"],
                                    start_column=START_COLUMN, end_column=STOP_COLUMN,
                                    fill_speed=40000)

    hw.synth_shaker.shake(33, 300)
    hw.vacuum.vacuum_synth(kPa=-40, duration=30)
        # Dispense 2
    dispense_actions.dispense_full_plate_384(reagent="EB", volume=50, location="SYN_NZL", stackable = ["synthesis_384"],
                                    start_column=START_COLUMN, end_column=STOP_COLUMN,
                                    fill_speed=40000)

    hw.synth_shaker.shake(33, 300)
    hw.vacuum.vacuum_synth(kPa=-40, duration=30)

    # ***********************************
    # EL dispense (direct circuit, pump 8)
    # ***********************************
    fluidic_actions.close_reagent_valves()
        # Dispense 3
    dispense_actions.dispense_full_plate_384(reagent="EL", volume=25, location="SYN_NZL", stackable = ["synthesis_384"],
                                    start_column=START_COLUMN, end_column=STOP_COLUMN,
                                    fill_speed=40000)

    hw.synth_shaker.shake(33, 30)
    hw.vacuum.vacuum_synth(kPa=-40, duration=30)
        # Dispense 4
    dispense_actions.dispense_full_plate_384(reagent="EL", volume=25, location="SYN_NZL", stackable = ["synthesis_384"],
                                    start_column=START_COLUMN, end_column=STOP_COLUMN,
                                    fill_speed=40000)

    hw.synth_shaker.shake(33, 30)
    hw.vacuum.vacuum_synth(kPa=-40, duration=30)

    # Buzz synthesis_384
    hw.vacuum.set_pressure(kPa=-40)
    hw.MCB.vac_pull_vac_hs()
    hw.synth_shaker.shake(0, 10)
    hw.synth_shaker.shake(80, 60)
    hw.MCB.vac_vent_hs()

    # -----------------------------------
    # Prime W8 through pump 4 ("dT" line)
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
    dispense_actions.dispense_full_plate_384(reagent="dT", volume=25, location="SYN_NZL", stackable = ["synthesis_384"],
                                    start_column=START_COLUMN, end_column=STOP_COLUMN,
                                    fill_speed=40000)

    hw.synth_shaker.shake(0, 10)
    hw.vacuum.vacuum_synth(kPa=-40, duration=60)
        # Dispense 2
    dispense_actions.dispense_full_plate_384(reagent="dT", volume=25, location="SYN_NZL", stackable = ["synthesis_384"],
                                    start_column=START_COLUMN, end_column=STOP_COLUMN,
                                    fill_speed=40000)

    hw.synth_shaker.shake(0, 10)
    hw.vacuum.vacuum_synth(kPa=-40, duration=60)
        # Dispense 3
    dispense_actions.dispense_full_plate_384(reagent="dT", volume=25, location="SYN_NZL", stackable = ["synthesis_384"],
                                    start_column=START_COLUMN, end_column=STOP_COLUMN,
                                    fill_speed=40000)

    hw.synth_shaker.shake(0, 10)
    hw.vacuum.vacuum_synth(kPa=-40, duration=1200)

    print("End Prewash")


def Liberation(prime=True):

    print("Begin Liberation")

    # synthesis_384 in on the SYN station
    # lid is on the VTS station at this point
    # oligo_384 plate is in the reader
    # sacrificial_384 is in the VTS

    # -----------------------------------
    # Prime LB through pump 6 ("W2" line)
    fluidic_actions.connect_pump_to_rotary_bottle("W2", "LB")
    if prime:
        fluidic_actions.prime_pump(reagent="W2")
    # -----------------------------------

    # Heater at 70°C
    hw.synth_heater.set_temp(70)
    hw.synth_heater.enable()
    hw.synth_heater.wait_setpoint()

    dispense_actions.dispense_full_plate_384(reagent="W2", volume=20, location="SYN_NZL", stackable = ["synthesis_384"],
                                    start_column=START_COLUMN, end_column=STOP_COLUMN,
                                    fill_speed=40000)

    hw.synth_shaker.shake(50, 1800)

    print("End Liberation")


def Precipitation(prime=True):

    print("Begin Precipitation")

    # synthesis_384 in on the SYN station
    # lid is on the VTS station at this point
    # oligo_384 plate is in the reader
    # sacrificial_384 is in the VTS

    # Heater at 25°C
    hw.synth_heater.set_temp(25)
    hw.synth_heater.enable()

    # -----------------------------------
    # Prime W8 through pump 1 ("dA" line)
    fluidic_actions.connect_pump_to_rotary_bottle("dA", "W8")
    if prime:
        fluidic_actions.prime_pump(reagent="dA")
    # -----------------------------------

    # -----------------------------------
    # Prime W8 through pump 2 ("dC" line)
    fluidic_actions.connect_pump_to_rotary_bottle("dC", "W8")
    if prime:
        fluidic_actions.prime_pump(reagent="dC")
    # -----------------------------------

    # -----------------------------------
    # Prime W8 through pump 3 ("dG" line)
    fluidic_actions.connect_pump_to_rotary_bottle("dG", "W8")
    if prime:
        fluidic_actions.prime_pump(reagent="dG")
    # -----------------------------------

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

    # -----------------------------------
    # Prime W6 (IPA) through pump 4 ("dT" line)
    fluidic_actions.connect_pump_to_rotary_bottle("dT", "W6")
    if prime:
        fluidic_actions.prime_pump(reagent="dT")
    # -----------------------------------

    fluidic_actions.connect_pump_to_rotary_bottle("dT", "W6")
    dispense_actions.dispense_full_plate_384(reagent="dT", volume=50, location="SYN_NZL", stackable = ["synthesis_384"],
                                    start_column=START_COLUMN, end_column=STOP_COLUMN,
                                    fill_speed=40000)


    hw.synth_shaker.shake(0, 1200)
    hw.vacuum.vacuum_synth(kPa=-40, duration=40)

    # Buzz synthesis_384
    hw.vacuum.set_pressure(kPa=-40)
    hw.MCB.vac_pull_vac_hs()
    hw.synth_shaker.shake(0, 10)
    hw.synth_shaker.shake(80, 60)
    hw.MCB.vac_vent_hs()

    print("End Precipitation")


def Desalting(prime=True):

    print("Begin Desalting")

    # synthesis_384 in on the SYN station
    # lid is on the VTS station at this point
    # oligo_384 plate is in the reader
    # sacrificial_384 is in the VTS

    # Heater at 25°C
    hw.synth_heater.set_temp(25)
    hw.synth_heater.enable()

    # -----------------------------------
    # Prime W8 through pump 4 ("dT" line)
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

    # ***********************************
    # W1 dispense (rotary circuit, pump 4 ("dT" line))
    # ***********************************
    fluidic_actions.connect_pump_to_rotary_bottle("dT", "W1")
        # Dispense 1
    dispense_actions.dispense_full_plate_384(reagent="dT", volume=70, location="SYN_NZL", stackable = ["synthesis_384"],
                                    start_column=START_COLUMN, end_column=STOP_COLUMN,
                                    fill_speed=40000)

    hw.synth_shaker.shake(0, 0)
    hw.vacuum.vacuum_synth(kPa=-60, duration=60)
        # Dispense 2
    dispense_actions.dispense_full_plate_384(reagent="dT", volume=70, location="SYN_NZL", stackable = ["synthesis_384"],
                                    start_column=START_COLUMN, end_column=STOP_COLUMN,
                                    fill_speed=40000)

    hw.synth_shaker.shake(0, 0)
    hw.vacuum.vacuum_synth(kPa=-60, duration=60)
        # Dispense 3
    dispense_actions.dispense_full_plate_384(reagent="dT", volume=70, location="SYN_NZL", stackable = ["synthesis_384"],
                                    start_column=START_COLUMN, end_column=STOP_COLUMN,
                                    fill_speed=40000)

    hw.synth_shaker.shake(0, 0)
    hw.vacuum.vacuum_synth(kPa=-60, duration=60)
        # Dispense 4
    dispense_actions.dispense_full_plate_384(reagent="dT", volume=70, location="SYN_NZL", stackable = ["synthesis_384"],
                                    start_column=START_COLUMN, end_column=STOP_COLUMN,
                                    fill_speed=40000)

    hw.synth_shaker.shake(0, 0)
    hw.vacuum.vacuum_synth(kPa=-60, duration=60)
        # Dispense 5
    dispense_actions.dispense_full_plate_384(reagent="dT", volume=70, location="SYN_NZL", stackable = ["synthesis_384"],
                                    start_column=START_COLUMN, end_column=STOP_COLUMN,
                                    fill_speed=40000)

    hw.synth_shaker.shake(0, 0)
    hw.vacuum.vacuum_synth(kPa=-60, duration=1200)

    print("End Desalting")


def Elution(prime=True):

    global EL_PRIMED
    
    print("Begin Elution")

    # synthesis_384 in on the SYN station
    # lid is on the VTS station at this point
    # oligo_384 plate is in the reader
    # sacrificial_384 is in the VTS

    # Heater at 25°C
    hw.synth_heater.set_temp(25)
    hw.synth_heater.enable()

    #   Move VTS up to sacrificial_384
    hw.vts_motor.VTS_go_to_pos("sacrificial_384")

    # Moving the synthesis_384 plate from SYN to the VTS on top of the lid
    hw.gripper.move_stackable("SYN", ["synthesis_384"], "synthesis_384", "VTS", ["lid"])

    hw.vacuum.vacuum_vts(kPa=-40, duration=40)

    # remove droplets
    hw.gripper.move_stackable("VTS", ["synthesis_384","lid"], "lid", "DOCK", [], remove_droplets=True)

    # Moving the synthesis_384 plate from VTS to the SYN
    hw.gripper.move_stackable("VTS", ["synthesis_384","lid"], "synthesis_384", "SYN", [])

    hw.gripper.grip_go_to_pos("Home")
    # => Gripper is at "Home" position

    if EL_PRIMED == False:
        fluidic_actions.close_reagent_valves()
        if prime:
            fluidic_actions.prime_pump(reagent="EL")
            EL_PRIMED = True

    fluidic_actions.close_reagent_valves()
    dispense_actions.dispense_full_plate_384(reagent="EL", volume=40, location="SYN_NZL", stackable = ["synthesis_384"],
                                    start_column=START_COLUMN, end_column=STOP_COLUMN,
                                    fill_speed=40000)

    hw.synth_shaker.shake(40, 180)

    # Moving the lid from VTS to the DOCK
    hw.gripper.move_stackable("VTS", ["lid"], "lid", "DOCK", [])

    #   Move VTS up to park
    hw.vts_motor.VTS_go_to_pos("park")

    # Moving the sacrificial_384 from VTS to the DOCK on top of the lid
    hw.gripper.move_stackable("VTS", ["sacrificial_384"], "sacrificial_384", "DOCK", ["lid"])

    # Opening the plate reader
    hw.gripper.grip_go_to_pos("Park")
    hw.reader.opendrawer()

    # Moving the oligo_384 plate from plate reader to the VTS
    hw.gripper.move_stackable("READER", ["oligo_384"], "oligo_384", "VTS", [])
    # => Gripper is at "VTS" position

    # Closing the plate reader
    hw.gripper.grip_go_to_pos("Park")
    hw.reader.closedrawer()

    #   Move VTS up to oligo_384
    hw.vts_motor.VTS_go_to_pos("oligo_384")

    # Moving the lid from DOCK to the VTS
    hw.gripper.move_stackable("DOCK", ["lid"], "lid", "VTS", [])

    # Moving the sacrificial_384 from VTS to the DOCK
    hw.gripper.move_stackable("VTS", ["sacrificial_384", "lid"], "sacrificial_384", "DOCK", [])

    # Moving the synthesis_384 plate from SYN to the VTS on top of the lid
    hw.gripper.move_stackable("SYN", ["synthesis_384"], "synthesis_384", "VTS", ["lid"])

    # hw.vacuum.vacuum_vts(kPa=-10, duration=40)

    # hw.vacuum.vacuum_vts(kPa=-20, duration=70)

    hw.vacuum.set_pressure(kPa=-10)
    hw.MCB.vac_pull_vac_tx()
    hw.synth_shaker.shake(0, 40)        # to create a wait for 40 sec
    hw.vacuum.set_pressure(kPa=-20)
    hw.synth_shaker.shake(0, 70)        # to create a wait for 70 sec
    hw.MCB.vac_vent_tx()

    # remove droplets
    hw.gripper.move_stackable("VTS", ["synthesis_384","lid"], "lid", "DOCK", [], remove_droplets=True)

    # Moving the lid from VTS to the DOCK
    hw.gripper.move_stackable("VTS", ["lid"], "lid", "DOCK", [])

    #   Move VTS up to park
    hw.vts_motor.VTS_go_to_pos("park")

    # Moving the oligo_384 from VTS to the SYN
    hw.gripper.move_stackable("VTS", ["oligo_384"], "oligo_384", "SYN", [])

    hw.gripper.grip_go_to_pos("Home")
    # => Gripper is at "Home" position

    # Buzz oligo_384
    hw.vacuum.set_pressure(kPa=-20)
    hw.MCB.vac_pull_vac_hs()
    hw.synth_shaker.shake(80, 300)
    hw.MCB.vac_vent_hs()

    # Tapping
    hw.gripper.move_stackable("SYN", ["oligo_384"], "oligo_384", "VTS", [], tapping=True)

    # Moving the lid from DOCKING to VTS (with synthesis on top)
    hw.gripper.move_stackable("DOCK", ["synthesis_384","lid"], "lid", "VTS", [])

    # Moving the sacrificial_384 plate from DOCKING to VTS (with lid and synthesis_384 on top)
    hw.gripper.move_stackable("DOCK", ["sacrificial_384"], "sacrificial_384", "VTS", ["synthesis_384","lid"])

    hw.gripper.grip_go_to_pos("Home")
    # => Gripper is at "Home" position

    # -----------------------------------
    # Prime W8 through pump 4 ("dT" line)
    fluidic_actions.connect_pump_to_rotary_bottle("dT", "W8")
    if prime:
        fluidic_actions.prime_pump(reagent="dT")
    # -----------------------------------

    # -----------------------------------
    # Prime W8 through pump 5 ("EB" line)
    fluidic_actions.connect_pump_to_rotary_bottle("EB", "W8")
    if prime:
        fluidic_actions.prime_pump(reagent="EB")
    # -----------------------------------

    # -----------------------------------
    # Prime W8 through pump 6 ("W2" line)
    fluidic_actions.connect_pump_to_rotary_bottle("W2", "W8")
    if prime:
        fluidic_actions.prime_pump(reagent="W2")
    # -----------------------------------

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

    print("PSP 384 wells OnePot")
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
            for option in range(start_option, end_option + 1):
                perform_option(option)
        else:
            print("Invalid input. Please enter valid options.")

