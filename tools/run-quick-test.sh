#!/bin/bash
# simple script to automate the steps involved in running tests
# prerequisites: chmod u+x run-quick-test.sh

clear

echo "=================="
echo "CALLING [test_one] in 1 second..."
echo "=================="
sleep 1
python -m dimcli.tests.quicktest
sleep 2

clear 




echo ""
echo "=================="
echo "Completed."
echo "=================="