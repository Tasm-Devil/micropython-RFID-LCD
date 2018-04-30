from machine import PWM
from time import sleep_ms

class BUZZER:
    def __init__(self, pin):
        self.pin = pin
        
    def init(self):
        buz = PWM(self.pin)
        buz.freq(1046)
        buz.duty(512)
        sleep_ms(250)
        buz.deinit()
        sleep_ms(500)
        buz.duty(512)
        sleep_ms(250)
        buz.deinit()

        
    def blues(self):
        buz = PWM(self.pin)
        buz.freq(523)
        buz.duty(512)
        sleep_ms(100)
        buz.freq(622)
        sleep_ms(100)
        buz.freq(698)
        sleep_ms(100)
        buz.freq(739)
        sleep_ms(100)
        buz.freq(783)
        sleep_ms(100)
        buz.freq(987)
        sleep_ms(100)
        buz.freq(1046)
        sleep_ms(100)
        buz.freq(987)
        sleep_ms(100)
        buz.freq(783)
        sleep_ms(100)
        buz.freq(739)
        sleep_ms(100)
        buz.freq(698)
        sleep_ms(100)
        buz.freq(622)
        buz.deinit()
    
    def wrong(self):
        buz = PWM(self.pin)
        buz.freq(369)
        buz.duty(512)
        sleep_ms(100)
        buz.deinit()
        sleep_ms(50)
        buz.duty(369)
        sleep_ms(100)
        buz.deinit()
    
    
