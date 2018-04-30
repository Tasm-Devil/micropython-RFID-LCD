# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)

# Set new IP-address
#import network
#wlan = network.WLAN(network.STA_IF)
#wlan.ifconfig(('192.168.1.82', '255.255.255.0', '192.168.1.2', '192.168.1.2'))
#print('network config:', wlan.ifconfig())

# Start web-REPL-Interface
import gc
#import webrepl
#webrepl.start()
gc.collect()
