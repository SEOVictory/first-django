#!/bin/sh

cd "$(git rev-parse --show-toplevel)"
CWD=$(pwd)
PYTHON=$(which python)
if [ $PYTHON != "$CWD/tutorial/bin/python" ]; then
    echo "Wrong Working Directory"
    exit 1
fi

VENV_DIR="./tutorial"
PEP8='pep8'

if [ $($PEP8 --version) != '0.6.1' ]; then
    echo "WARNING: pep8 version not '0.6.1.'"
fi

PEP8_RESULT=0
TMP_FILE=$(tempfile)
find . -iname "*.py" | \
grep -v $VENV_DIR | \
while read ln; do
    pep8 --filename="*.py" --show-pep8  --show-source "$ln" | \
        grep . >> $TMP_FILE
done
grep . $TMP_FILE
RESULT=$?
if [ $RESULT -eq 0 ]; then
    PEP8_RESULT=1
fi
rm $TMP_FILE

cd addressbook
python manage.py test
TEST_RESULT=$?

exit $(( $TEST_RESULT + $PEP8_RESULT ))