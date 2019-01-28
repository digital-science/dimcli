#!/bin/bash
# simple script to run iPython preloaded with this libray
# prerequisites: chmod u+x run-shell.sh

clear

echo "=================="
echo "Opening iPython with dimcli pre-loaded..."
echo "=================="
ipython shellprofile.py --no-simple-prompt --no-confirm-exit -i