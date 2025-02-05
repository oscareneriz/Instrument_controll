#------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------
#THIS SCRIPT WILL MAKE THE INSTALL AUTOMATIC ONLY PLACE THE ISUI_MASTER FOLDER IN DOCUMENTS UN-ZIP IT AND RENAME IN AS ISUI.
#AFTER THAT •	ONCE THAT IS DONE GO TO THE DESKTOP RIGHT CLICK ON THE DESKTOP ICONS ISUI.DESKTOP, CLICK ON PROPERTIES, CLICK 
#ON PERMISIONS AND CHECK THE BOX THAT SAYS ALLOW EXECUTE FILE AS PROGRAM. TO FINISH RUN IT AND ACCEPT THAT YOU WANT TO RUN IT
#------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------

#!/bin/bash
#The ISUI folder should already be in Documents and called ISUI

#To update the instrument Ubuntu:
sudo apt-get update

#Update and get pip and viertual environment:
python3 -m pip install --user --upgrade pip
python3 -m pip install --user virtualenv
sudo apt-get install python3-venv

#Makes an environment in ISGUI:
python3 -m venv /home/dnascript/Documents/ISUI/venv

#Activates the environment:
cd /home/dnascript/Documents/ISUI
source venv/bin/activate

#In the environment:

pip3 install pyserial jsonmerge
git clone https://github.com/NativeDesign/python-tmcl.git
cd python-tmcl
python3 setup.py install
pip3 install --upgrade pip
pip3 install PyQt5==5.14.2

cp /home/dnascript/Documents/ISUI/Install/ISUI.desktop /home/dnascript/Desktop
cd /home/dnascript/Documents/ISUI
pip3 install openpyxl
pip3 install libusb
pip3 install labjackpython
