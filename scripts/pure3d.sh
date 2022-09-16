#!/bin/bash

HELP="""
Run Pure3D webapp

Usage

Run it from the /scripts directory in the repo.

./pure3d.sh test
./pure3d.sh
    Test mode

./pure3d.sh prod
    Production mode
"""

if [[ "$1" == "--help" ]]; then
    echo $HELP
    exit 0
fi

scriptdir=`pwd`
cd ../src/pure3d/control

flaskdebug=" --debug"
flasktest="test"

if [[ "$1" == "prod" ]]; then
    flaskdebug=""
    flasktest=""
    shift
elif [[ "$1" == "test" ]]; then
    flaskdebug=" --debug"
    flasktest="test"
    shift
fi

if [[ "$1" == "" ]]; then
    flaskport="5000"
else
    flaskport="$1"
    shift
fi

export flasktest
export flaskdebug
export flaskport

flask$flaskdebug run --port $flaskport &
pid=$!
sleep 1
python3 "$scriptdir/browser.py" http://127.0.0.1:$flaskport
trap "kill $pid" SIGINT
echo "flask runs as process $pid"
wait "$pid"
