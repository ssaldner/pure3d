#!/bin/bash

HELP="""
Run DIP website

Usage

Run it from the /scripts directory in the repo.

./dip.sh
    Prodcution mode

./dip.sh debug
    Debug mode
"""

cd ../src/dip

if [[ "$1" == "debug" ]]; then
    export FLASK_DEBUG=1
elif [[ "$1" != "" ]]; then
    echo $HELP
    echo ""
    echo "Error in calling this program!"
    echo "Wrong argument `$1`"
    exit 1
else
    export FLASK_DEBUG=0
fi

flask run &
pid=$!
sleep 1
python3 "$scriptdir/browser.py" http://127.0.0.1:5000
trap "kill $pid" SIGINT
echo "flask runs as process $pid"
wait "$pid"
