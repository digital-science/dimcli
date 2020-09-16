#!/bin/bash
# simple script to automate the steps involved in running tests
# prerequisites: chmod u+x run-gsheets-tests.sh

clear

echo "=================="
echo "CALLING [test_export_gsheets] in 1 second..."
echo "=================="
sleep 1
python -m dimcli.tests.test_export_gsheets
sleep 2

echo ""
echo "=================="
echo "Completed."
echo "=================="