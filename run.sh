#!/bin/bash

# cd this directory
python3 exec_updater.py
cd now_server
chmod 700 bedrock_server
./bedrock_server
