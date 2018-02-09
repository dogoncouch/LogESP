#!/bin/bash

# MIT License
# 
# Copyright (c) 2017 Dan Persons <dpersonsdev@gmail.com>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# 


usage() {
    echo "Usage: ${0##*/} [-hv] <directory> <command>"
    echo
    echo "Optional arguments:"
    echo "  -h                      Print this help message"
    echo "  -v                      Print the version number"
    echo "  -r                      Restart daemons"
    echo "  -k                      Stop daemons"
    echo "  -b <ldsi-base>          Set the LDSI base directory"
    echo "  -e <env-base>           Set a virtual environment"
}

while getopts ":hvrkb:e:" o; do
    case "${o}" in
        h)
            usage
            exit 0
            ;;
        v)
            VERSIONCHECK=1
            ;;
        r)
            RESTARTING=1
            ;;
        k)
            KILLING=1
            ;;
        b)
            LDSIBASE=${OPTARG}
            ;;
        e)
            ENVBASE=${OPTARG}
            ;;
    esac
done
shift $((OPTIND-1))

if [ $RESTARTING ]; then
    LDSIPROCLIST=`ps aux | grep 'daemons.core.main' | awk '{print $2}'`
    read LDSIPROC WASTE <<< ${LDSIPROCLIST}
    kill -1 ${LDSIPROC}
    exit 0
fi

if [ $KILLING ]; then
    LDSIPROCLIST=`ps aux | grep 'ldsi-start.sh' | awk '{print $2}'`
    read LDSIPROC WASTE <<< ${LDSIPROCLIST}
    kill ${LDSIPROC}
    exit 0
fi

if [ $ENVBASE ]; then
    if [ -d ${ENVBASE} ]; then
        echo "Loading virtual environment at ${ENVBASE}"
        source ${ENVBASE}/bin/activate
    else
        echo "Directory ${ENVBASE} not found."
        exit 1
    fi
fi

if [ $LDSIBASE ]; then
    echo "Changing directory to ${LDSIBASE}"
    cd "${LDSIBASE}"
else
    cd `dirname $0`
fi

if [ $VERSIONCHECK ]; then
    VERSION=`python manage.py shell -c "import ldsi; print(ldsi.__version__)"`
    echo "${0##*/}-$VERSION"
    exit 0
fi

echo Starting daemons...

while :; do
    python manage.py shell -c "import daemons.core ; daemons.core.main()"
done
