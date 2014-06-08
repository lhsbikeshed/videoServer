#!/bin/sh

NAME=CamFeeds

. /lib/lsb/init-functions
. /etc/default/rcS


case "$1" in 
  start)
        log_daemon_msg "Starting $NAME this will take 30 seconds"
        # need to name the session
        screen -S feedPilot  -d -m /home/videoserver/videoServer/feedScripts/input2feed-PilotCam
        sleep 5
        screen -S feedTactical  -d -m /home/videoserver/videoServer/feedScripts/input2feed-TacticalCam
        sleep 5
        screen -S feedEngineer  -d -m /home/videoserver/videoServer/feedScripts/input2feed-EngineerCam
        sleep 5
        screen -S feedCabin  -d -m /home/videoserver/videoServer/feedScripts/input2feed-CabinCam
        sleep 5
        screen -S feedCaptain  -d -m /home/videoserver/videoServer/feedScripts/input2feed-CaptainCam
        sleep 5
        screen -S snowmixPreview  -d -m /home/videoserver/Snowmix-0.4.3/src/snowmix '/home/videoserver/videoServer/snowmixIni/preview-basis'
        screen -S snowmixLive  -d -m /home/videoserver/Snowmix-0.4.3/src/snowmix '/home/videoserver/videoServer/snowmixIni/live-basis'
        sleep 5
        screen -S screenPreview  -d -m /home/videoserver/videoServer/outputScripts/output2screenPreview
        screen -S feedAudio  -d -m /home/videoserver/videoServer/feedScripts/audio2Live
        screen -S oscServer  -d -m /usr/bin/python2.7 '/home/videoserver/videoServer/oscServer/oscServer.py'
        #screen -S splitLive  -d -m /home/videoserver/videoServer/outputScripts/liveVideoSplitter
        #sleep 2	
        #screen -S liveLocal  -d -m /home/videoserver/videoServer/outputScripts/output2screenLive
        #sleep 2	
        #screen -S liveStream  -d -m /home/videoserver/videoServer/outputScripts/streamLive.sh 'ustream'
        log_end_msg 0
        ;;
  stop)
        log_daemon_msg "Stopping $NAME" "$NAME"
        screen -S feedPilot  -X quit
        screen -S feedTactical  -X quit
        screen -S feedEngineer  -X quit
        screen -S feedCabin  -X quit
        screen -S feedCaptain  -X quit
        screen -S snowmixPreview  -X quit
        screen -S snowmixLive  -X quit
        screen -S screenPreview  -X quit
        screen -S oscServer  -X quit
        screen -S feedAudio  -X quit
        #screen -S splitLive  -X quit
        #screen -S liveLocal  -X quit
        #screen -S liveStream  -X quit
        log_end_msg 0
        ;;
  *)
        log_success_msg "Usage: $0 {start|stop}"
        exit 1
        ;;
esac

exit 0

