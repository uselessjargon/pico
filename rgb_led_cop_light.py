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


def init_leds():
    global led1, led2
    led1 = Rgb_led(2,3,4)
    led2 = Rgb_led(6,7,8)


def loop():
    while True:
        print("Red 1")
        led1.set_color(255,0,0)
        print("Blue 2")
        led2.set_color(0,0,255)
        utime.sleep_ms(100)
        print("Blue 1")
        led1.set_color(0,0,255)
        print("Red 2")
        led2.set_color(255,0,0)
        utime.sleep_ms(100)
        


if __name__ == '__main__':
    init_leds()
    loop()  