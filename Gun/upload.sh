#!/bin/bash
ampy --port /dev/ttyUSB1 put boot.py
ampy --port /dev/ttyUSB1 put ir_com.py
ampy --port /dev/ttyUSB1 put ir_main.py main.py 
ampy --port /dev/ttyUSB1 put ir_rx
ampy --port /dev/ttyUSB1 put ir_tx