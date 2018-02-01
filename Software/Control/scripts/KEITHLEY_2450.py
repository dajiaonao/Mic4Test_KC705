#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import time
import socket
import platform
import subprocess
import numpy as np
hostname = '192.168.2.100'                  #wire network hostname
port = 5025                                 #host tcp port number
#-------------------------------------------------------------------#
## main function: used to test the resistor of the load
def main():
    ss.send("*IDN?\n".encode())                                         #command terminated with '\n'
    print("Instrument ID: %s"%ss.recv(50))
    ss.send("*RST\n".encode())                                          #command terminated with '\n'
    ss.send(":SOUR:FUNC VOLT\n".encode())
    ss.send("SENS:CURR:RANG 1E-3\n".encode())                           #set the current range 10mA
    ss.send("DISP:DIG 6\n".encode())                                    #display digital the max is 6
    ss.send("OUTP ON\n".encode())                                       #open output 
    for i in range(100, 110):                                           #voltage range 0-200
        step = i * 0.1                                                  #voltage step 100mV
        ss.send((":SOUR:VOLT %f\n"%step).encode())                      #set output voltage
        time.sleep(2.1)                                                 #delay 100ms
        ss.send(":READ?\n".encode())                                    #read current of the output
        print("Output current: %s"%ss.recv(100))                        #receive output current value
    ss.close()                                                          #close socket
    print("Ok!")
#-------------------------------------------------------------------#
if __name__ == "__main__":
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      #init local socket handle
    ss.connect((hostname, port))                                #connect to the instrument 
    main()                                                      #execute main function

