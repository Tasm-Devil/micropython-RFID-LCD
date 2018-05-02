from time import sleep_ms
from machine import I2C, Pin

import ssd1306                      # oled-Display
from lib.lcd.esp8266_i2c_lcd import I2cLcd  # LC-Display

from extras.buzzer import BUZZER

from mfrc522 import MFRC522

#0,    2,   4,   5,   12,  13,  14, (15), 16 <-- Nutzbare GPIO-Pins
#(D3), D4,  D2,  D1,  D6,  D7,  D5, (D8), D0 <-- Bezeichnungen auf Board
#    , sda, rst,      mosi,miso,sck,    ,    <-- mfrc522 RFID-Modul
#                scl                    ,sda <-- I2C Display ssd1306
#                                   buz      <-- Buzzer
# D3 darf zum Zeitpunk des Starts nicht verbunden sein. Also nicht nutzbar.
# Die Leitung rst wird nicht benötigt.
# Also ist D2 noch frei!

# I2C-Bus init
i2c = I2C(scl=Pin(16), sda=Pin(5), freq=400000)

# LC-Display init
DISPLAY_I2C_ADDR = 0x3F #DEFAULT_I2C_ADDR = 0x27
lcd = I2cLcd(i2c, DISPLAY_I2C_ADDR, 4, 20)
lcd.backlight_on()

# oled-Display init
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# buzzer init
buzzer = BUZZER(Pin(15))
buzzer.init()

def falschekarte(uid):
    print("Falsche Karte: " + str(uid))
    lcd.clear()
    lcd.putstr("Falsche Karte:\n" + str(uid))
    oled.fill(0)
    oled.text('Falsche Karte:', 0, 20)
    oled.text(str(uid), 0, 40)
    oled.show()
    buzzer.wrong()

def schlossoeffnen():
    print("Autorisierung erfolgreich!")
    lcd.clear()
    lcd.putstr("Autorisierung\nerfolgreich!")
    oled.fill(0)
    oled.text('Autorisierung', 0, 20)
    oled.text('erfolgreich!', 0, 40)
    oled.show()
    buzzer.blues()

def kartebitte():
    lcd.clear()
    lcd.putstr("Karte bitte\nanlegen!")
    oled.fill(0)
    oled.text('Karte', 0, 20)
    oled.text('bitte!', 0, 40)
    oled.show()

try:
    kartebitte()
    while True:
#                             sck, mosi, miso, rst,  cs(sda)
#                             D5   D6    D7    D2    D4
        rdr = MFRC522(14 , 12,   13,   4,   2)
        uid = ""
        (stat, tag_type) = rdr.request(rdr.REQIDL)
        if stat == rdr.OK:
            (stat, raw_uid) = rdr.anticoll()
            if stat == rdr.OK:
                uid = ("0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                if uid == "0xf5f810a6":
                    schlossoeffnen()
                else:
                    falschekarte(uid)
                sleep_ms(1000)
            kartebitte()

except KeyboardInterrupt:
    print("Bye")
