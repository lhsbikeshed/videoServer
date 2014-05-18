#!/bin/sh

NAME=CamFeeds

. /lib/lsb/init-functions
. /etc/default/rcS


case "$1" in 
  start)
        log_daemon_msg "Starting $NAME" "$NAME"
        # need to name the session
        screen -S feedPilot  -d -m su -c /home/videoserver/videoServer/input2feed-PilotCam
        screen -S feedTactical  -d -m su -c /home/videoserver/videoServer/input2feed-TacticalCam
        screen -S feedEngineer  -d -m su -c /home/videoserver/videoServer/input2feed-EngineerCam
        screen -S feedCabin  -d -m su -c /home/videoserver/videoServer/input2feed-CabinCam
        screen -S feedCaptain  -d -m su -c /home/videoserver/videoServer/input2feed-CaptainCam
        log_end_msg 0
        ;;
  stop)
        log_daemon_msg "Stopping $NAME" "$NAME"
        screen -S feedPilot  -X quit
        screen -S feedTactical  -X quit
        screen -S feedEngineer  -X quit
        screen -S feedCabin  -X quit
        screen -S feedCaptain  -X quit
        screen -S irccat -X quit
        log_end_msg 0
        ;;
  *)
        log_success_msg "Usage: $0 {start|stop}"
        exit 1
        ;;
esac

exit 0

