#!/bin/bash
# simple script to automate the steps involved in running tests
# prerequisites: chmod u+x run-tests.sh

clear

echo "=================="
echo "CALLING [test_one] in 1 second..."
echo "=================="
sleep 1
python -m dimcli.tests.test_one
sleep 2


echo ""
echo "=================="
echo "Completed."
echo "=================="