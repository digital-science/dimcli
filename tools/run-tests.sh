#!/bin/bash
# simple script to automate the steps involved in running tests
# prerequisites: chmod u+x run-tests.sh

clear

echo "=================="
echo "CALLING [test_login] in 1 second..."
echo "=================="
sleep 1
python -m dimcli.tests.test_login
sleep 2

echo "=================="
echo "CALLING [test_grammar] in 1 second..."
echo "=================="
sleep 1
python -m dimcli.tests.test_grammar
sleep 2

echo "=================="
echo "CALLING [test_queries] in 1 second..."
echo "=================="
sleep 1
python -m dimcli.tests.test_queries
sleep 2

echo "=================="
echo "CALLING [test_dataframes] in 1 second..."
echo "=================="
sleep 1
python -m dimcli.tests.test_dataframes
sleep 2

echo "=================="
echo "CALLING [test_functions] in 1 second..."
echo "=================="
sleep 1
python -m dimcli.tests.test_functions
sleep 2

echo ""
echo "=================="
echo "Completed."
echo "=================="