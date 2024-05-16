#!/bin/bash

# cd this directory 
python3 exec_update.py
cd now_server
chmod 700 bedrock_server
./bedrock_server
