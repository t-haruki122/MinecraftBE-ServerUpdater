#!/bin/bash
#cron exec as root

# change to your path
PATH=/path/to/your/dir
# change to your service name
SERVICE=serviceName.service
# change to your server dir name
SERVER_DIR_NAME=now_server

# Override echo to include [BDS_UPD_SHELL] and timestamp
echo() {
    builtin echo "[BDS_UPD_SHELL] $(/bin/date '+%Y-%m-%d %H:%M:%S') // $*"
}

# Check if PATH variable is valid
if [ ! -d "$PATH" ]; then
    echo "Error: PATH variable is not a valid directory."
    exit 1
fi

# check if need to update
cd $PATH
UPD=$(/usr/bin/python3 exec_updater.py 0 | /usr/bin/tail -n 1)

if [ "$UPD" -eq 1 ]; then
    # stop service
    echo "stop service: $SERVICE"
    /usr/bin/systemctl stop $SERVICE

    # update server
    echo "update server"
    /usr/bin/python3 exec_updater.py
    /usr/bin/chmod +rw $SERVER_DIR_NAME
    /usr/bin/chmod +x $SERVER_DIR_NAME/bedrock_server

    # start service
    echo "start service: $SERVICE"
    /usr/bin/systemctl start $SERVICE
else
    echo "no need to update"
fi