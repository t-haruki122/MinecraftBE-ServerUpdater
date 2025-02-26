# Minecraft Bedrock Edition Dedicated Server Updater for Win & Linux

## Description
This python script can download (&replace) Dedicated Server of Minecraft Bedrock Edition.  
It has 4 options of version and 2 ones of downloading.  
**DO NOT use this for DoS purposes.**  

### version options:
0. Windows Release
1. Linux Release
2. Windows Preview
3. Linux Preview
### downloading options:
1. Downloading & Replacing : Download & Replace old server
2. Normal Downloading : Just download & UnZip server files  

On replacing mode, this script replace only 3 files.

1. worlds
2. allowlist.json
3. server.properties

You have to copy *resource packs* manually.  

Please change server folder name to `now_server`.  
If you’d not like to change it, please change variable `now_server_path` in `exec_updater.py`.

## Requirement
- Python3
- requests (Python Library)

## How to Use
### 1. Download this scripts
### 2. UnZip and move the files
Move `exec_updater.py` and `update_run.sh` to the directory which has server folder.  
NOT same directory as a file like server.properties.  
Like this:  
```
BDSroot
    ├─ now_server (This is server body)
    │  ├─ worlds
    │  ├─ bedrock_server
    │  └─ etc...
    ├─ exec_updater.py
    ├─ run.sh
    └─ update_run.sh
```
### 3. Change the server folder name
Change the server folder name to `now_server`
### 4. Execute the script
Linux:  
`python3 exec_update.py`

You may be able to use `run.sh` and `update_run.sh` if you use systemd and crontab.  

## Author
t-haruki122
