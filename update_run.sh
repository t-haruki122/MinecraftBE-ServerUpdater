#!/bin/bash
#cron exec as root

# change to your path
PATH=/path/to/your/dir
# change to your service name
SERVICE=serviceName.service
# change to your server dir name
SERVER_DIR_NAME=now_server

# Check if SERVICE variable is set
if [ -z "$SERVICE" ]; then
    echo "Error: SERVICE variable is not set."
    exit 1
fi

# check if need to update
cd $PATH
UPD=$(/usr/bin/python3 exec_updater.py 0 | /usr/bin/tail -n 1)

if [ "$UPD" -eq 1 ]; then
    # stop service
    echo "[BDS_UPD_SHELL] stop service: $SERVICE"
    /usr/bin/systemctl stop $SERVICE

    # update server
    echo "[BDS_UPD_SHELL] update server"
    /usr/bin/python3 exec_updater.py
    /usr/bin/chmod +rw $SERVER_DIR_NAME
    /usr/bin/chmod +x $SERVER_DIR_NAME/bedrock_server

    # start service
    echo "[BDS_UPD_SHELL] start service: $SERVICE"
    /usr/bin/systemctl start $SERVICE
else
    echo "[BDS_UPD_SHELL] no need to update"
fi