
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
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        s.send("stack 0 %s \n" % a)
        s.close()

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
        if a == 1:
            s.send("image load 0 /home/videoserver/videoServer/images/beginScreen.png \n")
            s.send("audio mixer source mute on 1 1 \n")
        if a == 2:
            s.send("image load 0 /home/videoserver/videoServer/images/technicalDifficulties.png \n")
            s.send("audio mixer source mute on 1 1 \n")
        if a == 3:
            s.send("image load 0 /home/videoserver/videoServer/images/endScreen.png \n")
            s.send("audio mixer source mute on 1 1 \n")
        s.close()

pilotFeed = 0
tacticalFeed = 0
engineerFeed = 0
cabinFeed = 0
captainFeed = 0
snowmixPreview = 0
snowmixLive = 0
outputPreview = 0
outputLive = 0
systemState = 0
audioFeed = 0

# define a message-handler function for the server to call.
def system_handler(addr, tags, stuff, source):
    global pilotFeed
    global tacticalFeed
    global engineerFeed
    global cabinFeed
    global captainFeed
    global snowmixPreview
    global snowmixLive
    global outputPreview
    global outputLive
    global systemState
    global audioFeed
    print "---"
    #   print "received new osc msg from %s" % OSC.getUrlStr(source)
    print "with addr : %s" % addr
    print "typetags %s" % tags
    print "data %s" % stuff
    print "---"
    for a in stuff:
        if a == 1 and systemState == 0:
            pilotFeed = subprocess.Popen('/home/videoserver/videoServer/feedScripts/input2feed-PilotCam', preexec_fn=os.setsid)
            tacticalFeed = subprocess.Popen('/home/videoserver/videoServer/feedScripts/input2feed-TacticalCam', preexec_fn=os.setsid)
            engineerFeed = subprocess.Popen('/home/videoserver/videoServer/feedScripts/input2feed-EngineerCam', preexec_fn=os.setsid)
            cabinFeed = subprocess.Popen('/home/videoserver/videoServer/feedScripts/input2feed-CabinCam', preexec_fn=os.setsid)
            captainFeed = subprocess.Popen('/home/videoserver/videoServer/feedScripts/input2feed-CaptainCam', preexec_fn=os.setsid)
            snowmixPreview = subprocess.Popen(['/home/videoserver/Snowmix-0.4.3/src/snowmix','/home/videoserver/videoServer/snowmixIni/preview-basis'], preexec_fn=os.setsid)
            snowmixLive = subprocess.Popen(['/home/videoserver/Snowmix-0.4.3/src/snowmix','/home/videoserver/videoServer/snowmixIni/live-basis'], preexec_fn=os.setsid)
            time.sleep(2)
            audioFeed = subprocess.Popen('/home/videoserver/videoServer/feedScripts/audio2Live', preexec_fn=os.setsid)
            time.sleep(2)
            os.killpg(audioFeed.pid, signal.SIGTERM)
            audioFeed = subprocess.Popen('/home/videoserver/videoServer/feedScripts/audio2Live', preexec_fn=os.setsid)
            time.sleep(2)
            outputPreview = subprocess.Popen('/home/videoserver/videoServer/outputScripts/output2screenPreview', preexec_fn=os.setsid)
            #outputLive = subprocess.Popen('/home/videoserver/videoServer/outputScripts/av_output2tcp_server2', preexec_fn=os.setsid)
            
            systemState = 1
            
        elif a == 0 and systemState == 1:
            os.killpg(outputPreview.pid, signal.SIGTERM)
            #os.killpg(outputLive.pid, signal.SIGTERM)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TCP_IP, TCP_PORT))
            s.send("quit\n")
            s.close()
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
            
            systemState = 0


def feedRestart_handler(addr, tags, stuff, source):
    global pilotFeed
    global tacticalFeed
    global engineerFeed
    global cabinFeed
    global captainFeed
    #   print "received new osc msg from %s" % OSC.getUrlStr(source)
    print "with addr : %s" % addr
    print "typetags %s" % tags
    print "data %s" % stuff
    print "---"
    for a in stuff:
        if a == 1:
            os.killpg(pilotFeed.pid, signal.SIGTERM)
            pilotFeed.wait()
            pilotFeed = subprocess.Popen('/home/videoserver/videoServer/feedScripts/input2feed-PilotCam', preexec_fn=os.setsid)
        elif a == 2:
            os.killpg(tacticalFeed.pid, signal.SIGTERM)
            tacticalFeed.wait()
            tacticalFeed = subprocess.Popen('/home/videoserver/videoServer/feedScripts/input2feed-TacticalCam', preexec_fn=os.setsid)
        elif a == 3:
            os.killpg(engineerFeed.pid, signal.SIGTERM)
            engineerFeed.wait()
            engineerFeed = subprocess.Popen('/home/videoserver/videoServer/feedScripts/input2feed-EngineerCam', preexec_fn=os.setsid)
        elif a == 4:
            os.killpg(cabinFeed.pid, signal.SIGTERM)
            cabinFeed.wait()
            cabinFeed = subprocess.Popen('/home/videoserver/videoServer/feedScripts/input2feed-CabinCam', preexec_fn=os.setsid)
        elif a == 5:
            os.killpg(captainFeed.pid, signal.SIGTERM)
            captainFeed.wait()
            captainFeed = subprocess.Popen('/home/videoserver/videoServer/feedScripts/input2feed-CaptainCam', preexec_fn=os.setsid)


s.addMsgHandler("/video/focus", feedFocus_handler) # adding our function
s.addMsgHandler("/screen/focus", screenFocus_handler) # adding our function
s.addMsgHandler("/system", system_handler) # adding our function
s.addMsgHandler("/feed/restart", feedRestart_handler) # adding our function


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
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send("quit\n")
    s.close()
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
        
