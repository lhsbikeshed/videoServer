
""" receiving OSC with pyOSC
https://trac.v2.nl/wiki/pyOSC
example by www.ixi-audio.net based on pyOSC documentation

this is a very basic example, for detailed info on pyOSC functionality check the OSC.py file 
or run pydoc pyOSC.py. you can also get the docs by opening a python shell and doing
>>> import OSC
>>> help(OSC)
"""


import OSC
import time, threading
import socket
import sys
import subprocess
import os
import signal
import time

TCP_IP = '127.0.0.1'
TCP_PORT = 9998
TCP_PORT2 = 9999


# tupple with ip, port. i dont use the () but maybe you want -> send_address = ('127.0.0.1', 9000)
receive_address = '10.0.0.50', 12000


# OSC Server. there are three different types of server. 
s = OSC.OSCServer(receive_address) # basic
##s = OSC.ThreadingOSCServer(receive_address) # threading
##s = OSC.ForkingOSCServer(receive_address) # forking



# this registers a 'default' handler (for unmatched messages), 
# an /'error' handler, an '/info' handler.
# And, if the client supports it, a '/subscribe' & '/unsubscribe' handler
s.addDefaultHandlers()



# define a message-handler function for the server to call.
def feedFocus_handler(addr, tags, stuff, source):
    print "---"
    #   print "received new osc msg from %s" % OSC.getUrlStr(source)
    print "with addr : %s" % addr
    print "typetags %s" % tags
    print "data %s" % stuff
    print "---"
    for a in stuff:
        setCamera(a)

def setCamera(feedNum):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.connect((TCP_IP, TCP_PORT2))
    if feedNum == 1:
        s2.send("text place rgb 1 0.0 1.0 0.0 \n text place rgb 2 1.0 0.0 0.0 \n text place rgb 3 1.0 0.0 0.0 \n text place rgb 4 1.0 0.0 0.0 \n text place rgb 5 1.0 0.0 0.0 \n")
        s.send("stack 0 %s \n" % feedNum)
        s.send("image load 1 /home/videoserver/videoServer/images/screenOverlayMirror.png \n")
        s.send("text string 0 \n")
        s.send("text string 1 Pilot: \n")
    elif feedNum == 2:
        s2.send("text place rgb 1 1.0 0.0 0.0 \n text place rgb 2 0.0 1.0 0.0 \n text place rgb 3 1.0 0.0 0.0 \n text place rgb 4 1.0 0.0 0.0 \n text place rgb 5 1.0 0.0 0.0 \n")
        s.send("stack 0 %s \n" % feedNum)
        s.send("image load 1 /home/videoserver/videoServer/images/screenOverlay.png \n")
        s.send("text string 0 Tactical: \n")
        s.send("text string 1 \n")
    elif feedNum == 3:
        s2.send("text place rgb 1 1.0 0.0 0.0 \n text place rgb 2 1.0 0.0 0.0 \n text place rgb 3 0.0 1.0 0.0 \n text place rgb 4 1.0 0.0 0.0 \n text place rgb 5 1.0 0.0 0.0 \n")
        s.send("stack 0 %s \n" % feedNum)
        s.send("image load 1 /home/videoserver/videoServer/images/screenOverlayMirror.png \n")
        s.send("text string 0 \n")
        s.send("text string 1 Engineer: \n")
    elif feedNum == 4:
        s2.send("text place rgb 1 1.0 0.0 0.0 \n text place rgb 2 1.0 0.0 0.0 \n text place rgb 3 1.0 0.0 0.0 \n text place rgb 4 0.0 1.0 0.0 \n text place rgb 5 1.0 0.0 0.0 \n")
        s.send("stack 0 %s \n" % feedNum)
        s.send("image load 1 /home/videoserver/videoServer/images/screenOverlayMirror.png \n")
        s.send("text string 0 \n")
        s.send("text string 1 Cabin: \n")
    elif feedNum == 5:
        s2.send("text place rgb 1 1.0 0.0 0.0 \n text place rgb 2 1.0 0.0 0.0 \n text place rgb 3 1.0 0.0 0.0 \n text place rgb 4 1.0 0.0 0.0 \n text place rgb 5 0.0 1.0 0.0 \n")
        s.send("stack 0 %s \n" % feedNum)
        s.send("image load 1 /home/videoserver/videoServer/images/screenOverlay.png \n")
        s.send("text string 0 Captain: \n")
        s.send("text string 1 \n")
    s.close()
    s2.close()


# define a message-handler function for the server to call.
def screenFocus_handler(addr, tags, stuff, source):
    print "---"
    #   print "received new osc msg from %s" % OSC.getUrlStr(source)
    print "with addr : %s" % addr
    print "typetags %s" % tags
    print "data %s" % stuff
    print "---"
    for a in stuff:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        if a == 0:
            s.send("image load 0 \n")
            s.send("audio mixer source mute off 1 1 \n")
        elif a == 1:
            s.send("image load 0 /home/videoserver/videoServer/images/beginScreen.png \n")
            s.send("audio mixer source mute on 1 1 \n")
        elif a == 2:
            s.send("image load 0 /home/videoserver/videoServer/images/technicalDifficulties.png \n")
            s.send("audio mixer source mute on 1 1 \n")
        elif a == 3:
            s.send("image load 0 /home/videoserver/videoServer/images/endScreen.png \n")
            s.send("audio mixer source mute on 1 1 \n")
        s.close()



s.addMsgHandler("/video/focus", feedFocus_handler) # adding our function
s.addMsgHandler("/screen/focus", screenFocus_handler) # adding our function


# just checking which handlers we have added
print "Registered Callback-functions are :"
for addr in s.getOSCAddressSpace():
    print addr


# Start OSCServer
print "\nStarting OSCServer. Use ctrl-C to quit."
st = threading.Thread( target = s.serve_forever )
st.start()


try :
    while 1 :
        time.sleep(1)

except KeyboardInterrupt :
    print "\nClosing OSCServer."
    s.close()
    print "Waiting for Server-thread to finish"
    st.join() ##!!!
    os.killpg(outputPreview.pid, signal.SIGTERM)
    os.killpg(outputLive.pid, signal.SIGTERM)
    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.connect((TCP_IP, TCP_PORT))
    #s.send("quit\n")
    #s.close()
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.connect((TCP_IP, 9999))
    s2.send("quit\n")
    s2.close()
    time.sleep(2)
    os.killpg(snowmixPreview.pid, signal.SIGTERM)
    os.killpg(snowmixLive.pid, signal.SIGTERM)
    os.killpg(audioFeed.pid, signal.SIGTERM)
    os.killpg(pilotFeed.pid, signal.SIGTERM)
    os.killpg(tacticalFeed.pid, signal.SIGTERM)
    os.killpg(engineerFeed.pid, signal.SIGTERM)
    os.killpg(cabinFeed.pid, signal.SIGTERM)
    os.killpg(captainFeed.pid, signal.SIGTERM)
    print "Done"
        
