#!/usr/bin/python
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

templatePath = "/home/solexious/Dropbox/shipshared/cert.svg"

pilotName = ""
tacticalName = ""
engineerName = ""
captainName = ""
gmName = ""
teamName = ""
groundCrewName = ""
locationName = ""
startEpoch = 0

receive_address = '10.0.0.50', 12000
s = OSC.OSCServer(receive_address) # basic
s.addDefaultHandlers()

# define a message-handler function for the server to call.
def death(addr, tags, stuff, source):
    generateCerts()
    
    
def win(addr, tags, stuff, source):
    generateCerts()


def getNames(addr, tags, stuff, source):
    global pilotName
    global tacticalName
    global engineerName
    global captainName
    global gmName
    global teamName
    global groundCrewName
    
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


def generateCerts():
    global pilotName
    global tacticalName
    global engineerName
    global captainName
    global gmName
    global teamName
    global groundCrewName
    
    
    # Pilot cert
    with open("out.txt", "wt") as fout:
      with open(templatePath, "rt") as fin:
          for line in fin:
              fout.write(line.replace('%PLAYER_NAME%', pilotName))
              fout.write(line.replace('%TEAM_NAME%', teamName))
              fout.write(line.replace('%PLAYER_ROLE%', 'Pilot'))
              fout.write(line.replace('%DATE%', 'Orange'))
              fout.write(line.replace('%LOCATION%', locationName))
              fout.write(line.replace('%LENGTH%', 'Orange'))
              fout.write(line.replace('%STORY_LINE%', 'Orange'))
              fout.write(line.replace('%END_RESULT%', 'Orange'))
              fout.write(line.replace('%CAPTAIN_NAME%', 'Orange'))
              fout.write(line.replace('%GROUND_CREW_NAMES%', 'Orange'))
    
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
