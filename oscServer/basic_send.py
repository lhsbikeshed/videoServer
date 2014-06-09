
""" sending OSC with pyOSC
https://trac.v2.nl/wiki/pyOSC
example by www.ixi-audio.net based on pyOSC documentation
"""
import OSC
import time, random

"""
note that if there is nobody listening in the other end we get an error like this
    OSC.OSCClientError: while sending: [Errno 111] Connection refused
so we need to have an app listening in the receiving port for this to work properly

this is a very basic example, for detailed info on pyOSC functionality check the OSC.py file 
or run pydoc pyOSC.py. you can also get the docs by opening a python shell and doing
>>> import OSC
>>> help(OSC)
"""

## the most basic ##
client = OSC.OSCClient()
msg = OSC.OSCMessage()
msg.setAddress("/game/setNames")
msg.append("Charles Yarnold")
msg.append("Russ Garret")
msg.append("TimRTerrible")
msg.append("Tom Wyatt")
msg.append("Thomas Greer")
msg.append("Fuzzy Love buckets")
msg.append("Clare Greenhalgh, Someone Else")
msg.append("Loading Bar")
client.sendto(msg, ('127.0.0.1', 12010)) # note that the second arg is a tupple and not two arguments

time.sleep(5)

## the most basic ##
client = OSC.OSCClient()
msg = OSC.OSCMessage()
msg.setAddress("/game/reset")
client.sendto(msg, ('127.0.0.1', 12010)) # note that the second arg is a tupple and not two arguments

time.sleep(5)

## the most basic ##
client = OSC.OSCClient()
msg = OSC.OSCMessage()
msg.setAddress("/game/gameWin")
client.sendto(msg, ('127.0.0.1', 12010)) # note that the second arg is a tupple and not two arguments
