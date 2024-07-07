#!/bin/sh

# Load .env
unamestr=$(uname)
if [ "$unamestr" = 'Linux' ]; then
  export $(grep -v '^#' .env | xargs -d '\n')
elif [ "$unamestr" = 'FreeBSD' ] || [ "$unamestr" = 'Darwin' ]; then
  export $(grep -v '^#' .env | xargs -0)
fi

echo "Start parsing data"
python3 main.py