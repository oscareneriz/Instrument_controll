import sys
sys.path.append('../')
sys.path.append("Actions")
sys.path.append("Protocols")

import Utils
from Hardware import Hardware
from Actions.FluidicActions import Fluidic
from Actions.DispenseActions import Dispense
import time

START_COLUMN=1
STOP_COLUMN=24

hw=Hardware()
fluidic_actions=Fluidic(hw)
dispense_actions=Dispense(hw)

NBCYCLES = 1

def Synthesis(prime=True):

    global NBCYCLES
    
    print("Cycle ", NBCYCLES)

    # ***********************************
    # Elongation
    # ***********************************
    print("EL")
    fluidic_actions.close_reagent_valves()
    dispense_actions.dispense_full_plate_384(reagent="EB", volume=25, location="SYN_NZL", stackable = ["synthesis_384"],
                                    start_column=START_COLUMN, end_column=STOP_COLUMN,
                                    fill_speed=40000)

    Utils.triggercamera("Cycle " + str(NBCYCLES) + "/200 - Elongation - Dispense")
    hw.synth_shaker.shake(40, 240)
    Utils.triggercamera("Cycle " + str(NBCYCLES) + "/200 - Elongation - Incubation")
    hw.vacuum.vacuum_synth(kPa=-40, duration=25)
    Utils.triggercamera("Cycle " + str(NBCYCLES) + "/200 - Elongation - Evacuation")

    # ***********************************
    # Post-Elongation Wash
    # ***********************************
    print("WB1")
    dispense_actions.dispense_full_plate_384(reagent="EL", volume=25, location="SYN_NZL", stackable = ["synthesis_384"],
                                    start_column=START_COLUMN, end_column=STOP_COLUMN,
                                    fill_speed=40000)

    hw.synth_shaker.shake(40, 20)
    hw.vacuum.vacuum_synth(kPa=-40, duration=30)

    # ***********************************
    # Deblock 1/2
    # ***********************************
    print("DB1")
    dispense_actions.dispense_full_plate_384(reagent="DB", volume=25, location="SYN_NZL", stackable = ["synthesis_384"],
                                    start_column=START_COLUMN, end_column=STOP_COLUMN,
                                    fill_speed=40000)

    hw.synth_shaker.shake(40, 30)
    hw.vacuum.vacuum_synth(kPa=-40, duration=30)

    # ***********************************
    # Deblock 2/2
    # ***********************************
    print("DB2")
    dispense_actions.dispense_full_plate_384(reagent="DB", volume=15, location="SYN_NZL", stackable = ["synthesis_384"],
                                    start_column=START_COLUMN, end_column=STOP_COLUMN,
                                    fill_speed=40000)

    hw.synth_shaker.shake(40, 30)
    hw.vacuum.vacuum_synth(kPa=-40, duration=30)

    # ***********************************
    # Wash
    # ***********************************
    print("W2")
    dispense_actions.dispense_full_plate_384(reagent="W2", volume=15, location="SYN_NZL", stackable = ["synthesis_384"],
                                    start_column=START_COLUMN, end_column=STOP_COLUMN,
                                    fill_speed=40000)

    hw.synth_shaker.shake(40, 20)
    hw.vacuum.vacuum_synth(kPa=-40, duration=30)
    
    NBCYCLES = NBCYCLES + 1

if __name__ == "__main__":

    hw.home()
    hw.cooler.set_temp(10)
    hw.cooler.enable()
    #hw.cooler.activate_fans()  Done by default when enabling device

    # Heater at 80°C
    hw.synth_heater.set_temp(80)
    hw.synth_heater.enable()
    hw.synth_heater.wait_setpoint()

    Utils.triggercamera("test")
    
    while 1:
        Synthesis()
