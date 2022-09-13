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

if [[ "$1" == "--help" ]]; then
    echo $HELP
    exit 0
fi

scriptdir=`pwd`
cd ../src/dip

flaskdebug = " --debug"

if [[ "$1" == "prod" ]]; then
    flaskdebug=""
    shift
fi

if [[ "$1" == "" ]]; then
    flaskport="5000"
else
    flaskport="$1"
    shift
fi

flask$flaskdebug run --port $flaskport &
pid=$!
sleep 1
python3 "$scriptdir/browser.py" http://127.0.0.1:$flaskport
trap "kill $pid" SIGINT
echo "flask runs as process $pid"
wait "$pid"
