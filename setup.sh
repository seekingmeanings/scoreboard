#!/bin/bash

ups() {
  echo "some mistake (this tool is to dumb to debug itself"
  exit 69
}


if [ ! -d env ]; then
  echo "installing system dependencies"
  wait 3
  sudo apt install python3-smbus i2c-tools python3 python3-pip || ups

  echo "\n\n\n\n\nsetting up environment"
  python3 -m venv --system-site-pachages env || ups

  echo "going into the environment"
  source env || ups

  echo "installing python dependencies"
  pip install -r requirements.txt || ups

  echo "install (probably) successful"
else
  echo "environment already built, delete ./env/ and run again"
  echo "to reinstall"
fi

