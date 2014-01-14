#!/bin/sh

VENV_DIR="./tutorial"
PEP8='pep8'

if [ $($PEP8 --version) != '0.6.1' ]; then
    echo "WARNING: pep8 version not '0.6.1.'"
fi

find . -iname "*.py" | \
grep -v $VENV_DIR | \
while read ln; do
    pep8 --filename="*.py" --show-pep8  --show-source "$ln"
done
