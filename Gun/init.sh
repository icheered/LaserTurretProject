
# echo "Starting"
# echo "Erasing memory"
# esptool.py --port /dev/ttyUSB0 erase_flash

# echo "Writing memory"
# esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 esp8266-20170108-v1.8.7.bin


echo "Uploading files"

echo "Uploading boot.py"
ampy --port /dev/ttyUSB9 --baud 115200 put src/boot.py boot.py
echo "Uploading main.py"
ampy --port /dev/ttyUSB9 --baud 115200 put src/__main.py __main.py

echo "Making directories"
ampy --port /dev/ttyUSB9 --baud 115200 mkdir ir_rx
ampy --port /dev/ttyUSB9 --baud 115200 mkdir ir_tx

echo "Uploading NEC files.py"
ampy --port /dev/ttyUSB15 --baud 115200 put src/ir_tx/nec.py ir_tx/nec.py
ampy --port /dev/ttyUSB14 --baud 115200 put src/ir_rx/nec.py ir_rx/nec.py

echo "Uploading init files.py"
ampy --port /dev/ttyUSB9 --baud 115200 put src/ir_tx/__init__.py ir_tx/__init__.py
ampy --port /dev/ttyUSB9 --baud 115200 put src/ir_rx/__init__.py ir_rx/__init__.py