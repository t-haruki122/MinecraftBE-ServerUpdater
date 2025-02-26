# Minecraft BDS (Bedrock Dedicated Server) Updater

## Description
This python script can download (&replace) BDS.  
**DO NOT use this for DoS purposes.**  

It has some options like below.  

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

You have to copy **resource packs** manually.  

Please change server folder name to `now_server`.  
If you’d not like to change it, please change variable `now_server_path` in `exec_updater.py`.

## Requirement
- Python3
- requests (Python Library)

## How to Use
### 1. Download this scripts
### 2. UnZip and move the files
Move `exec_updater.py` and `update_run.sh` to the directory which has server folder.  
Like this:  
```
BDSroot
    ├─ now_server (This is server body)
    │  ├─ worlds
    │  ├─ bedrock_server
    │  ├─ server.properties
    │  └─ etc...
    ├─ exec_updater.py
    ├─ run.sh
    └─ update_run.sh
```
### 3. Change the server folder name
Change the server folder name to `now_server`
### 4. Execute the script
Linux:  
`python3 exec_updater.py`

You may be able to use `run.sh` and `update_run.sh` if you use systemd and crontab.  

