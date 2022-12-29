from machine import Pin
import utime

"""
Author: Uselessjargon

MicroPython class to run the 28BYJ-48 with a ULN2003 Stepper Motor Driver Module in full-step mode.

** Code based on adafruit stepper.cpp with fix for 28BYJ-48 step sequence **

* The sequence of control signals for 4 control wires is as follows for full-steps:
*
* Step C0 C1 C2 C3 (modified for 28BYJ-48)
*    1  1  1  0  0
*    2  0  1  1  0
*    3  0  0  1  1
*    4  1  0  0  1

28BYJ-48 is a uni-polar (DC) 5V stepper motor

Diagram of Pico setup (Courtesy of microcontrollerslab.com)
https://microcontrollerslab.com/wp-content/uploads/2022/03/Raspberry-Pi-Pico-with-28BYJ-48-Stepper-Motor-and-ULN2003-Motor-Driver-connection-diagram.jpg

Example setup and usage:

    Pico  --> ULN2003 --> motor--> code
    -----------------------------------
    GPIO2 --> IN1 --> BLUE   --> pin1 
    GPIO3 --> IN2 --> PINK   --> pin2
    GPIO4 --> IN3 --> YELLOW --> pin3
    GPIO5 --> IN4 --> ORANGE --> pin4

# In full-step mode there are 32 steps with a gear reduction of 64, so 32x64 = 2048 steps per revolution.

import stepper.py
stepper1 = Stepper(2048, 2, 3, 4, 5)
stepper1.set_speed(10)  # max speed is supposedly 15 rpms
stepper1.step(20)       # 20 steps clockwise
stepper1.step(-30)      # 30 steps counter clockwise

# BUGS
- current motor/driver goes in reverse for positive and forward for negative - same happens with test script. Maybe test with arduino

# REFS
    - https://leap.tardate.com/kinetics/steppermotors/28byj48/
    - https://lastminuteengineers.com/28byj48-stepper-motor-arduino-tutorial/
    - https://github.com/arduino-libraries/Stepper/blob/master/src/Stepper.cpp

# FUTURE
    - stop motor [0,0,0,0] if no commands sent after x secs
    - allow input of angles from relative position vs steps (maybe with a class method)
"""

class Stepper:
    def __init__(self, number_of_steps:int, pin1:int, pin2:int, pin3:int, pin4:int) -> None:
        self.step_number = 0 # which step the motor is on
        self.direction = 0 # motor direction
        self.last_step_time = 0 # timestamp in us of the last step taken
        self.number_of_steps = number_of_steps # total number of steps for this motor
        
        # set the pin modes
        self.pin1 = Pin(pin1, Pin.OUT)
        self.pin2 = Pin(pin2, Pin.OUT)
        self.pin3 = Pin(pin3, Pin.OUT)
        self.pin4 = Pin(pin4, Pin.OUT)


    def set_speed(self, what_speed:float):
        """
        Set revolutions per minute by calculating the delay between steps e.g., motor has 2038 steps/rev so
        delay = (60 sec/2038 steps converted to microsecs ) / number of rpm's entered
        """
        # cap rpms at 15 so motor doesn't stall
        if (what_speed > 15):
            print(f"{what_speed} RPMs is too high. The 28BYJ-48 stalls out at higher than 15 RPM so capping it at 15.")
            what_speed = 15
        self.step_delay = 60 * 1000 * 1000 / self.number_of_steps / what_speed


    def step(self, steps_to_move:int):
        steps_left = abs(steps_to_move) # how many steps to take
        # determine the direction + = clockwise, - = counter clockwise
        if (steps_to_move > 0):
            self.direction = 1
        if (steps_to_move < 0):
            self.direction = 0
        # decrement the number of steps, moving one step at a time
        while (steps_left > 0):
            now = utime.ticks_us()
            # move only if delay time has passed
            time_diff = now - self.last_step_time
            if (time_diff >= self.step_delay):
                # get timestamp of last step
                self.last_step_time = now
                # increment / decrement the step number depending on direction
                if (self.direction == 1):
                    self.step_number += 1 
                    # if one revolution set step number back to 0
                    if (self.step_number == self.number_of_steps):
                        self.step_number = 0
                else:
                    if (self.step_number == 0):
                        self.step_number = self.number_of_steps
                    self.step_number -= 1
                # decrement steps left
                steps_left -= 1
                # step the motor to step 0, 1, 2, 3 - each step number is sequentially set to 0,1,2,3 due to modulo 4 - cool stuff
                self.step_motor(self.step_number % 4)

    def stop_motor(self):
        # stops current from going to motor after step run
        self.pin1.value(0)
        self.pin2.value(0)
        self.pin3.value(0)
        self.pin4.value(0)
        
    def step_motor(self, this_step:int):
        # python 3.10+ has switch but staying with if statements for compatibility
        # NOTE: as the code is written above it will never hit step 0 first - not sure it matters as long as the order is correct
        if (this_step == 0):
            self.pin1.value(1)
            self.pin2.value(1)
            self.pin3.value(0)
            self.pin4.value(0)
        elif (this_step == 1):
            self.pin1.value(0)
            self.pin2.value(1)
            self.pin3.value(1)
            self.pin4.value(0)
        elif (this_step == 2):
            self.pin1.value(0)
            self.pin2.value(0)
            self.pin3.value(1)
            self.pin4.value(1)
        elif (this_step == 3):
            self.pin1.value(1)
            self.pin2.value(0)
            self.pin3.value(0)
            self.pin4.value(1)


def main():
    stepper1 = Stepper(2048, 2, 3, 4, 5)
    stepper1.set_speed(300)  # set speed to 10 rpms
    stepper1.step(2048)
    utime.sleep(1)
    stepper1.stop_motor()
    
if __name__ == "__main__":
    main()
