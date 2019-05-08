from time import sleep_ms
from machine import I2C, Pin, SPI

from lcd.esp8266_i2c_lcd import I2cLcd
from rfid.mfrc522 import MFRC522
from buzzer import BUZZER

#0,    2,   4,   5,   12,  13,  14, (15), 16 <-- Nutzbare GPIO-Pins
#(D3), D4,  D2,  D1,  D6,  D7,  D5, (D8), D0 <-- Bezeichnungen auf Board
#    , sda, rst,      mosi,miso,sck,    ,    <-- mfrc522 RFID-Modul
#                sda                    ,scl <-- I2C Display ssd1306
#                                   buz      <-- Buzzer
# D3 darf zum Zeitpunk des Starts nicht verbunden sein. Also nicht nutzbar.
# Die Leitung rst wird nicht benötigt.

# SPI init
sck = Pin(14, Pin.OUT)
mosi = Pin(12, Pin.OUT)
miso = Pin(13, Pin.OUT)
spi = SPI(baudrate=100000, polarity=0, phase=0, sck=sck, mosi=mosi, miso=miso)
sda = Pin(2, Pin.OUT)
rst = Pin(4, Pin.OUT)


# I2C-Bus init
i2c = I2C(scl=Pin(16), sda=Pin(5), freq=400000)

# LC-Display init
DISPLAY_I2C_ADDR = 0x3F
DEFAULT_I2C_ADDR = 0x27

lcd = None
try:
    lcd = I2cLcd(i2c, DISPLAY_I2C_ADDR, 4, 20)
    lcd.backlight_on()
except OSError:
    print("No LCD on I2C-Address 0x3F")

if lcd is None:
    try:
        lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)
        lcd.backlight_on()
    except OSError:
        print("No LCD on I2C-Address 0x27")


# buzzer init
buzzer = BUZZER(Pin(15))
buzzer.init()


# relais init
relais = Pin(4, Pin.OUT)
relais.off()


def falschekarte(uid):
    print("Falsche Karte: " + str(uid))
    if lcd:
        lcd.clear()
        lcd.putstr("Falsche Karte:\n" + str(uid))
    buzzer.wrong()

def schlossoeffnen():
    print("Autorisierung erfolgreich!")
    if lcd:
        lcd.clear()
        lcd.putstr("Autorisierung\nerfolgreich!")
    buzzer.blues()
    relais.on()
    sleep_ms(1000)
    relais.off()

def kartebitte():
    if lcd:
        lcd.clear()
        lcd.putstr("Karte bitte\nanlegen!")

valid_card_uids = [
    "0xf5f810a6" ,  #Zugangskarte Pascal
    "0x46edc659" ,  #Zugangskarte Kamil
]

try:
    kartebitte()
    while True:
        rdr = MFRC522(spi, sda, rst)
        uid = ""
        (stat, tag_type) = rdr.request(rdr.REQIDL)
        if stat == rdr.OK:
            (stat, raw_uid) = rdr.anticoll()
            if stat == rdr.OK:
                uid = ("0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                if uid in valid_card_uids:
                    schlossoeffnen()
                else:
                    falschekarte(uid)
                sleep_ms(1000)
            kartebitte()

except KeyboardInterrupt:
    print("Bye")

