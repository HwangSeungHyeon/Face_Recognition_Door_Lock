#!/bin/bash
echo "run venv"
source /home/pi/keras/bin/activate
echo "run script"
python3 /home/pi/Face_Recognition_Door_Lock/Function.py
read reply
