#!/bin/bash
# simple script to run iPython preloaded with this libray
# prerequisites: chmod u+x run-shell.sh

clear

echo "=================="
echo "Opening iPython with dimcli pre-loaded..."
echo "import dimcli"
echo "dimcli.login()"
echo "dsl = dimcli.Dsl()"
echo "=================="
ipython shellprofile.py --no-simple-prompt --no-confirm-exit -i