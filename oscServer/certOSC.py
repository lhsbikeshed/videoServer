#!/usr/bin/python
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
def winTheGame(addr, tags, stuff, source):
    print "---"
    #   print "received new osc msg from %s" % OSC.getUrlStr(source)
    print "with addr : %s" % addr
    print "typetags %s" % tags
    print "data %s" % stuff
    print "---"
    
    with open("out.txt", "wt") as fout:
      with open("Stud.txt", "rt") as fin:
          for line in fin:
              fout.write(line.replace('A', 'Orange'))
    
    
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
    print "Done"
