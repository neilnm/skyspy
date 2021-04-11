#!/bin/sh

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
echo $DIR

if apt-get update ; then
    echo "[OK]"
else
    echo "[FAIL]"
fi

if apt-get install librtlsdr-dev ; then
    echo "[OK]"
else
    echo "[FAIL]"
fi

if apt-get install libgeos-dev ; then
    echo "[OK]"
else
    echo "[FAIL]"
fi

if python3 -m pip install -r $DIR/skyspy_requirements.txt ; then
    echo "[OK]"
else
   echo "[FAIL]"
fi

if cd $DIR && git clone https://github.com/antirez/dump1090.git ; then
    echo "[OK]"
else
    echo "[FAIL]"
fi