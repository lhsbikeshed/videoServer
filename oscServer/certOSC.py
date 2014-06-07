#!/usr/bin/python
import OSC
import time, threading
import socket
import sys
import subprocess
import os
import signal
import time
import datetime

TCP_IP = '127.0.0.1'
TCP_PORT = 9998
TCP_PORT2 = 9999

templatePath = "/home/solexious/Dropbox/shipshared/cert.svg"
svgPath = "/home/solexious/Dropbox/shipshared/certs/"

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
def death_handler(addr, tags, stuff, source):
    for a in stuff:
        generateCerts(a)
    
    
def win_handler(addr, tags, stuff, source):
    generateCerts("returned home triumphant!")


def getNames_handler(addr, tags, stuff, source):
    global pilotName
    global tacticalName
    global engineerName
    global captainName
    global gmName
    global teamName
    global groundCrewName
    global locationName
    
    print "---"
    #   print "received new osc msg from %s" % OSC.getUrlStr(source)
    print "with addr : %s" % addr
    print "typetags %s" % tags
    print "data %s" % stuff
    print "---"
    
    pilotName = stuff[0]
    tacticalName = stuff[1]
    engineerName = stuff[2]
    captainName = stuff[3]
    gmName = stuff[4]
    teamName = stuff[5]
    groundCrewName = stuff[6]
    locationName = stuff[7]
    
def reset_handler(addr, tags, stuff, source):
    global startEpoch
    
    startEpoch = int(time.time())


def generateCerts(endResult):
    global pilotName
    global tacticalName
    global engineerName
    global captainName
    global gmName
    global teamName
    global groundCrewName
    global locationName
    global startEpoch
    
    today = datetime.date.today()
    
    if startEpoch and pilotName:
        missionLength = int((int(time.time()) - startEpoch)/60)
        
        # Pilot cert
        svgNamePilot = svgPath + pilotName + "-" + teamName + "-" + today.strftime('%d-%m-%y') + ".svg"
        svgNamePilot.replace(" ", "")
        with open(svgNamePilot, "wt") as fout:
          with open(templatePath, "rt") as fin:
              for line in fin:
                  fout.write(line.replace('%PLAYER_NAME%', pilotName))
                  fout.write(line.replace('%TEAM_NAME%', teamName))
                  fout.write(line.replace('%PLAYER_ROLE%', 'Pilot'))
                  fout.write(line.replace('%DATE%', today.strftime('%d/%m/%y')))
                  fout.write(line.replace('%LOCATION%', locationName))
                  fout.write(line.replace('%LENGTH%', missionLength))
                  fout.write(line.replace('%STORY_LINE%', 'many hardships'))
                  fout.write(line.replace('%END_RESULT%', endResult))
                  fout.write(line.replace('%CAPTAIN_NAME%', captainName))
                  fout.write(line.replace('%GROUND_CREW_NAMES%', groundCrewName))
        
        # Tactical cert
        svgNameTactical = svgPath + tacticalName + "-" + teamName + "-" + today.strftime('%d-%m-%y') + ".svg"
        svgNameTactical.replace(" ", "")
        with open(svgNameTactical, "wt") as fout:
          with open(templatePath, "rt") as fin:
              for line in fin:
                  fout.write(line.replace('%PLAYER_NAME%', pilotName))
                  fout.write(line.replace('%TEAM_NAME%', teamName))
                  fout.write(line.replace('%PLAYER_ROLE%', 'Tactical'))
                  fout.write(line.replace('%DATE%', today.strftime('%d/%m/%y')))
                  fout.write(line.replace('%LOCATION%', locationName))
                  fout.write(line.replace('%LENGTH%', missionLength))
                  fout.write(line.replace('%STORY_LINE%', 'many hardships'))
                  fout.write(line.replace('%END_RESULT%', endResult))
                  fout.write(line.replace('%CAPTAIN_NAME%', captainName))
                  fout.write(line.replace('%GROUND_CREW_NAMES%', groundCrewName))
        
        # Engineer cert
        svgNameEngineer = svgPath + engineerName + "-" + teamName + "-" + today.strftime('%d-%m-%y') + ".svg"
        svgNameEngineer.replace(" ", "")
        with open(svgNameEngineer, "wt") as fout:
          with open(templatePath, "rt") as fin:
              for line in fin:
                  fout.write(line.replace('%PLAYER_NAME%', pilotName))
                  fout.write(line.replace('%TEAM_NAME%', teamName))
                  fout.write(line.replace('%PLAYER_ROLE%', 'Engineer'))
                  fout.write(line.replace('%DATE%', today.strftime('%d/%m/%y')))
                  fout.write(line.replace('%LOCATION%', locationName))
                  fout.write(line.replace('%LENGTH%', missionLength))
                  fout.write(line.replace('%STORY_LINE%', 'many hardships'))
                  fout.write(line.replace('%END_RESULT%', endResult))
                  fout.write(line.replace('%CAPTAIN_NAME%', captainName))
                  fout.write(line.replace('%GROUND_CREW_NAMES%', groundCrewName))
                  
    pilotName = ""
    tacticalName = ""
    engineerName = ""
    captainName = ""
    gmName = ""
    teamName = ""
    groundCrewName = ""
    startEpoch = 0
    
s.addMsgHandler("/scene/youaredead", death_handler) # adding our function
s.addMsgHandler("/game/gameWin", win_handler) # adding our function


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
