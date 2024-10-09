#!/bin/sh

# これを参照し，マインクラフトサーバーの更新を行うスクリプトに変更する

install_dir="/home/steamusr/Steam/steamapps/common/Satisfactory"
service="satisfactory-dedicated.service"

date +"%Y/%m/%d %p %I:%M:%S"
echo "Checking for updates..."

# Check version differences
if [ "$OLD_Build" -eq "$NEW_Build" ]; then
    echo "No game updates available."
elif [ "$OLD_Build" -gt "$NEW_Build" ]; then
    echo "The game has a new BuildID ${NEW_Build}. Service will be restarted."
    systemctl stop $service
    systemctl start $service
    systemctl status $service
else
    echo "error."
fi