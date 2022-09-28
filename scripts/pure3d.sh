#!/bin/bash

HELP="
Run Pure3D webapp, optionally start a browsing session as well.

Usage

Run it from the /scripts directory in the repo.

./pure3d.sh test
./pure3d.sh
    Test mode

./pure3d.sh prod
    Production mode

Options:

--browser
    Start a browsing session after starting the app.
"

flaskdebug=""
flasktest=""
flaskport="5000"
browse="x"

while [ ! -z "$1" ]; do
    if [[ "$1" == "--help" ]]; then
        printf "$HELP\n"
        exit 0
    fi
    if [[ "$1" == "prod" ]]; then
        flaskdebug=""
        flasktest=""
        shift
    elif [[ "$1" == "test" ]]; then
        flaskdebug=" --debug"
        flasktest="test"
        shift
    elif [[ "$1" == "--browse" ]]; then
        browse="v"
        shift
    else
        flaskport="$1"
        shift
        break
    fi
done

scriptdir="${0%/*}"
cd "$scriptdir/.."
repodir="`pwd`"
cd "src/pure3d/control"
printf "Working in repo $repodir\n"


export flasktest
export flaskdebug
export flaskport
export repodir

if [[ "$browse" == "v" ]]; then
    flask$flaskdebug run --port $flaskport &
    pid=$!
    sleep 1
    python3 "$repodir/scripts/browser.py" http://127.0.0.1:$flaskport
    trap "kill $pid" SIGINT
    echo "flask runs as process $pid"
    wait "$pid"
else
    flask$flaskdebug run --port $flaskport
fi
