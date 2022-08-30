#!/bin/bash

HELP="""
Run PILOT website

Usage

Run it from the /scripts directory in the repo.

./pilot.sh name
    Run named pilot in debug mode.
"""

scriptdir=`pwd`
cd ../pilots
pilotdir=`pwd`

if [[ "$1" == "" ]]; then
    echo $HELP
    echo ""
    echo "Error in calling this program!"
    echo "Missing pilot name"
    exit 1
fi

pilotname="$1"

if [[ ! -d "$pilotname" ]]; then
    echo "Pilot '$pilotname' does not exist"
    exit 1
fi

cd "$pilotname"
export FLASK_DEBUG=1
flask run &
pid=$!
sleep 1
python3 "$scriptdir/browser.py" http://127.0.0.1:5000
trap "kill $pid" SIGINT
echo "flask runs as process $pid"
wait "$pid"
