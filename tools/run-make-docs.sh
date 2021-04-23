#!/bin/bash
# build the docs in local and copy to /docs
# PS push to git not included

clear

echo "=================="
echo "Building docs.."
echo "=================="

cd docsrc
make html