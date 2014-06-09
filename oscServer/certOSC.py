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

receive_address = '127.0.0.1', 12010
s = OSC.OSCServer(receive_address) # basic
s.addDefaultHandlers()

# define a message-handler function for the server to call.
def death_handler(addr, tags, stuff, source):

    print "---"
    #   print "received new osc msg from %s" % OSC.getUrlStr(source)
    print "with addr : %s" % addr
    print "typetags %s" % tags
    print "data %s" % stuff
    print "---"
    
    for a in stuff:
        generateCerts(a)
    
    
def win_handler(addr, tags, stuff, source):

    print "---"
    #   print "received new osc msg from %s" % OSC.getUrlStr(source)
    print "with addr : %s" % addr
    print "typetags %s" % tags
    print "data %s" % stuff
    print "---"
    
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
    
    print "---"
    #   print "received new osc msg from %s" % OSC.getUrlStr(source)
    print "with addr : %s" % addr
    print "typetags %s" % tags
    print "data %s" % stuff
    print "---"
    
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
        svgNamePilot = svgNamePilot.replace(" ", "")
        with open(svgNamePilot, "wt") as fout:
          with open(templatePath, "rt") as fin:
              for line in fin:
                  line = line.replace('%PLAYER_NAME%', pilotName)
                  line = line.replace('%TEAM_NAME%', teamName)
                  line = line.replace('%PLAYER_ROLE%', 'Pilot')
                  line = line.replace('%DATE%', today.strftime('%d/%m/%y'))
                  line = line.replace('%LOCATION%', locationName)
                  line = line.replace('%LENGTH%', str(missionLength))
                  line = line.replace('%STORY_LINE%', 'many hardships')
                  line = line.replace('%END_RESULT%', endResult)
                  line = line.replace('%CAPTAIN_NAME%', captainName)
                  line = line.replace('%GROUND_CREW_NAMES%', groundCrewName)
                  fout.write(line)
        
        # Tactical cert
        svgNameTactical = svgPath + tacticalName + "-" + teamName + "-" + today.strftime('%d-%m-%y') + ".svg"
        svgNameTactical = svgNameTactical.replace(" ", "")
        with open(svgNameTactical, "wt") as fout:
          with open(templatePath, "rt") as fin:
              for line in fin:
                  line = line.replace('%PLAYER_NAME%', tacticalName)
                  line = line.replace('%TEAM_NAME%', teamName)
                  line = line.replace('%PLAYER_ROLE%', 'Tactical')
                  line = line.replace('%DATE%', today.strftime('%d/%m/%y'))
                  line = line.replace('%LOCATION%', locationName)
                  line = line.replace('%LENGTH%', str(missionLength))
                  line = line.replace('%STORY_LINE%', 'many hardships')
                  line = line.replace('%END_RESULT%', endResult)
                  line = line.replace('%CAPTAIN_NAME%', captainName)
                  line = line.replace('%GROUND_CREW_NAMES%', groundCrewName)
                  fout.write(line)
        
        # Engineer cert
        svgNameEngineer = svgPath + engineerName + "-" + teamName + "-" + today.strftime('%d-%m-%y') + ".svg"
        svgNameEngineer = svgNameEngineer.replace(" ", "")
        with open(svgNameEngineer, "wt") as fout:
          with open(templatePath, "rt") as fin:
              for line in fin:
                  line = line.replace('%PLAYER_NAME%', engineerName)
                  line = line.replace('%TEAM_NAME%', teamName)
                  line = line.replace('%PLAYER_ROLE%', 'Engineer')
                  line = line.replace('%DATE%', today.strftime('%d/%m/%y'))
                  line = line.replace('%LOCATION%', locationName)
                  line = line.replace('%LENGTH%', str(missionLength))
                  line = line.replace('%STORY_LINE%', 'many hardships')
                  line = line.replace('%END_RESULT%', endResult)
                  line = line.replace('%CAPTAIN_NAME%', captainName)
                  line = line.replace('%GROUND_CREW_NAMES%', groundCrewName)
                  fout.write(line)
                  
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
s.addMsgHandler("/game/reset", reset_handler) # adding our function
s.addMsgHandler("/game/setNames", getNames_handler) # adding our function


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
