# roebot 2019
ip codesys PLC - 192.168.137.66
ip- e!cockpit plc : 192.168.137.65

Raspberry pi 4:
username : pi
password : roebot

Set up a virtual environment and install opencv:
-https://www.pyimagesearch.com/2018/09/26/install-opencv-4-on-your-raspberry-pi/

install openCV for python 
-pip install opencv-contrib-python

- ```run python script "roebotMachine.py"```
- in virtual environment
run -python roebotMachine.py --ip "ip adress of pi"

the ip adress is for videostreaming server


For videostream in e!cockpit GUI:

1.Edit camera.htm: change to correct ip of raspberry pi
2.transfer the file to wago PLC with WinSCP https://winscp.net/eng/index.php by ssh to the wago plc ip- 192.168.137.65
username- root and password wago.watch youtube video:https://www.youtube.com/watch?v=4QdesMXA1XQ


