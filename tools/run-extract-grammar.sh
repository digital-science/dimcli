#!/bin/bash
# simple script to run iPython preloaded with this libray
# prerequisites: chmod u+x run-shell.sh

clear

echo "=================="
echo "Opening iPython and extracting latest grammar info..."
echo "import dimcli"
echo "dimcli.login()"
echo "dsl = dimcli.Dsl()"
echo "data = dsl.query('describe schema').json"
echo "with open('dimcli/core/dsl_grammar_language_NEW.py', 'w') as f:"
echo "    f.write('GRAMMAR_DICT = ' + str(data))"
echo "=================="

ipython shellgrammar.py --no-simple-prompt --no-confirm-exit -i