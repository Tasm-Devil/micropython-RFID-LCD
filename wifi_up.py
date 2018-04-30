import network
#import machine
#import ssd1306

#i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
#oled = ssd1306.SSD1306_I2C(128, 64, i2c)

sta_if = network.WLAN(network.STA_IF)

if not sta_if.isconnected():
	#oled.fill(0)
	#oled.text('connecting...', 0, 0)
	#oled.show()
	sta_if.active(True)
	sta_if.connect('SSID', 'password')
	while not sta_if.isconnected():
		pass
#oled.fill(0)
#oled.text('Connected!', 0, 0)
#oled.text('IP:', 0, 10) 
#oled.text(sta_if.ifconfig()[0], 0, 20)
#oled.show()
