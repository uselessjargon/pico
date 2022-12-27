from machine import PWM, Pin
import utime

# we'd need a class to setup the led as an object so we can set it's rgb values

class Rgb_led:
    def __init__(self, r_pin:int,g_pin:int,b_pin:int):
        # input the pico pin GPIO PWM pin #'s as output pins
        r_pin = Pin(r_pin, Pin.OUT)
        g_pin = Pin(g_pin, Pin.OUT)
        b_pin = Pin(b_pin, Pin.OUT)
        # set the pins as PWM objects
        self.__rpwm = PWM(r_pin)
        self.__gpwm = PWM(g_pin)
        self.__bpwm = PWM(b_pin)
        # init the freq for each led
        self.__rpwm.freq(2000)
        self.__gpwm.freq(2000)
        self.__bpwm.freq(2000)
        
    def __cnv_rgb(self,rgb):
        # map rgb value of 0-255 to duty cycle, returning an integer only
        # we cap the min and max rgb values at 0 and 255 to stay in range
        in_min = 0
        in_max = 255
        out_min = 0
        out_max = 65535
        if (rgb < in_min):
            rgb = in_min
        if (rgb > in_max):
            rgb = in_max
        return (rgb - in_min) * (out_max - out_min) // (in_max - in_min) + out_min
    
    def set_color(self,r,g,b):
        # input rgb value 0-255 and set the duty cycle for each led
        self.__rpwm.duty_u16(self.__cnv_rgb(r))
        self.__gpwm.duty_u16(self.__cnv_rgb(g))
        self.__bpwm.duty_u16(self.__cnv_rgb(b))


def led_alarm(led1, led2, secs=0):
    # flash led1 and 2 alternating red/blue for secs duration
    # secs = 0 flashes forever
    # issue: if secs = 0 how do I break out/override color. can we use an interupt?
    # https://github.com/peterhinch/micropython-async/blob/master/v3/docs/TUTORIAL.md#8-notes-for-beginners
    msecs = secs * 1000
    ticks = 0
    start_ticks = utime.ticks_ms()
    
    while (ticks <= msecs):
        if (msecs == 0):
            ticks = 0
        else:
            ticks = utime.ticks_ms() - start_ticks 
        led1.set_color(255,0,0)
        led2.set_color(0,0,255)
        utime.sleep_ms(100)
        led1.set_color(0,0,255)
        led2.set_color(255,0,0)
        utime.sleep_ms(100)
  
def led_allgood(led1, led2):
    led1.set_color(0,255,0)
    led2.set_color(0,255,0)

def cops():
    # initialize the leds
    led1 = Rgb_led(2,3,4)
    led2 = Rgb_led(6,7,8)

    while True:
        led_allgood(led1, led2)
        utime.sleep(2)
        led_alarm(led1,led2,5) # this stops the loops for x secs
        


if __name__ == '__main__':
    cops() 