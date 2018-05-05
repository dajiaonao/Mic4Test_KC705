#!/usr/bin/env python
from MIC4Config import MIC4Config, bitSet
import time
import socket
# import platform
# import subprocess
# import numpy as np
import datetime


class SMU:
    def __init__(self):
        self.ss = None
        self.hostname = '192.168.2.100'                  #wire network hostname
        self.port = 5025                                 #host tcp port number
    def connect(self):
        self.ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      #init local socket handle
        self.ss.connect((self.hostname, self.port))                                #connect to the instrument 

    def setup(self):
        ss = self.ss
        ss.send("*IDN?\n".encode())                                         #command terminated with '\n'
        print("Instrument ID: %s"%ss.recv(50))

        ss.send("*RST\n".encode())                                          #command terminated with '\n'
        ss.send(":SOUR:FUNC CURR\n".encode())
        #ss.send(":SENS:FUNC 'VOLT'\n".encode())
        ss.send(":SENS:VOLT:RANGE 2\n".encode())
#         ss.send(":SENS:VOLT:RANGE AUTO\n".encode())
    #    ss.send(":SOUR:CURR:MODE FIXED\n".encode())
        ss.send(":SOUR:CURR:RANGE MIN\n".encode())
        ss.send(":SOUR:CURR:LEV 0\n".encode())
        ss.send(":SOUR:VOLT:PROT PROT2\n".encode())
        #ss.send(":FORM:ELEM VOLT\n".encode())
        ss.send("DISP:DIG 6\n".encode())                                    #display digital the max is 6

        count = 30
        cmd = ''
        cmd += ':TRACe:MAKE "voltMeasBuffer", 10000;'
        #cmd += ':SENSe:FUNCtion "VOLTage";'
        cmd += ':COUN %d;'%count
        cmd += '\n'

        ss.send(cmd.encode())                                       #open output 

        #Interactive()
        #return
        ss.send("OUTP ON\n".encode())                                       #open output 

    def takeMeasurements(self, N=20):
        ss = self.ss
        ss.send(":MEASure:VOLT:DC? 'voltMeasBuffer'\n".encode())                                    #Only the last measure will be returned
        v = "%s"%ss.recv(2048)                        #receive output current value
        ss.send("TRACe:DATA? 1,{0:d}".format(N)+", 'voltMeasBuffer', REL, READ;\n".encode())                                    #to get all the measuremnets
        v = "%s"%ss.recv(2048)                        #here are they
        ss.send("TRACe:CLEar 'voltMeasBuffer';\n".encode())                                    #to get all the measuremnets
        print v

        return v
#         print len(v), len(v.split(','))

#         if self.fout:
#             self.fout.write(v)

def setDACcode(mc1, i, code):
    mc1.setClocks(0,6,6)
    mc1.sReg.value = 0
    if i>9:
#         print "Current DAC!!!"
        mc1.sReg.useCurDAC(i%10, code)
    else:
        mc1.sReg.useVolDAC(i, code)
    mc1.sReg.show()
    mc1.testReg(read=True)
#     mc1.testReg(read=False)
#     time.sleep(0.3)

def scan_DAC(idv, codeRange, headInfo, outfilename):
    mc1 = MIC4Config()
    mc1.connect()

    smu1 = SMU()
    smu1.connect()
    smu1.setup()
    with open(outfilename, 'w') as fout1:
#         print codeRange[0],codeRange[1]+1
        for code in range(codeRange[0],codeRange[1]+1):
            setDACcode(mc1, idv, code)
            v = smu1.takeMeasurements()
            fout1.write('# '+headInfo+' {0:d} code={1:x}\n'.format(idv,code)+v+'\n')

def scan_all():
    for i in range(6):
        if i<3: continue
        scan_DAC(i, (0, 0x3ff), 'Vol', 'DAC_chip5_scan{0:d}.dat'.format(i))

#     for i in range(10,17):
#         print i
#         scan_DAC(i, (0, 0xff), 'Cur', 'DAC_chip5_scan{0:d}.dat'.format(i))

def test():
    scan_DAC(10, (0, 10), 'Vol', 'DAC_chip5_scan10.dat')

if __name__ == '__main__':
#     test()
    scan_all()
