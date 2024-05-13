#!/bin/bash

ups() {
  echo "some mistake (this tool is to dumb to debug itself"
  exit 69
}

venv=".venv"

if [ ! -d env ]; then
  echo "installing system dependencies"
  wait 3
  sudo apt update -y
  sudo apt install python3-smbus i2c-tools python3 || ups

  echo
  echo
  echo "setting up environment"
  python3 -m venv --system-site-packages ${venv} || ups

  echo
  echo "going into the environment"
  #source env || ups

  echo
  echo "installing python dependencies"
  ${venv}/bin/pip install -r requirements.txt || ups

  echo
  echo
  echo "install (probably) successful"
else
  echo "environment already built, delete ${venv} and run again"
  echo "to reinstall"
fi

