#! /bin/bash
# Get the absolute path of the directory of this file
MY_PATH="`dirname \"$0\"`"              # relative
MY_PATH="`( cd \"$MY_PATH\" && pwd )`"  # absolutized and normalized
# Create a pid file
echo $BASHPID
echo $BASHPID > /var/run/plantos-server.pid
# Start the web server
$MY_PATH/main.py &
trap "kill %1" SIGHUP SIGINT SIGTERM EXIT
wait %1
