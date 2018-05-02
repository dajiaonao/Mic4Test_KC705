#!/usr/bin/env python
# -*- coding: utf-8 -*-

## @package MIC4Config
# Control module for the Topmetal-S 1mm Electrode single-chip test.
#

from __future__ import print_function
import copy
from command import *
import threading
import socket
import time
import sys

## Manage Topmetal-S 1mm chip's internal register map.
# Allow combining and disassembling individual registers
# to/from long integer for I/O
#

PowerOfTwo = lambda n: n and (not (n&(n-1))) ## taken from https://www.geeksforgeeks.org/find-position-of-the-only-set-bit/

def looksLikeHeader(i, l, h=0xbc, level=1):
    if l[i] != h: return False
    if level>0:
        if i>0 and l[i-1]>16: return False
        N = len(l)
        if i+1<N and not PowerOfTwo(l[i+1]): return False
        if i+2<=N and not PowerOfTwo(l[i+2]): return False

    return True

def n2N(n):
    j = 0
    while n>>j: j+=1
    return j-1

def findHeader(list1):
    n = len(list1)
    nF = 48
    headers = []
    for i in range(min(nF, n)):
        j = i
        while j<n:
#             print("--->",j,n,list1[j])
            if not looksLikeHeader(j,list1,level=0): j=n
            elif j+nF<n: j+=nF
            else: break
        if j!=n: headers.append(i)
    if len(headers) ==0: return -1
    header = headers[0]
    if len(headers) >1:
        headers2 = []
        for hi in headers:
            j = hi
            while j<n:
                if not looksLikeHeader(j,list1,level=1): j=n
                elif j+nF<n: j+=nF
                else: break
            if j!=n: headers2.append(hi)
        if len(headers2) != 0:
            header = headers2[0]
        elif len(headers2)>1:
            print("More Than 1 Header:", headers, "Using the first!!!1")
    return header

def parseFD(dlist):
    has_non_zero = [x for x in dlist[1:] if x!=0]

    if has_non_zero:
        print('*'*20)
        print(bin(dlist[0]))
        vx = 0
        nbit = 0
        for dx in dlist[1:-1]:
            vx |= dx<<nbit
            nbit += 8
            if nbit>=23:
                x1 = vx & 0x7fffff
                bC = x1>>20
                bR = (x1>>16)&0xf
                pC = (x1>>8)&0xff
                pR = x1&0xff
                flag = '' if PowerOfTwo(pR) and PowerOfTwo(pC) else 'X' 
                print(bin(x1),': {0:0>3b} {1:0>4b} {2:0>8b} {3:0>8b} => {4:>3d} {5:>2d} {6}'.format(bC, bR, pC, pR, bR*8+n2N(pR), bC*8+n2N(pC), flag))
                vx = vx >> 23
                nbit -= 23
        print(dlist[-1])
        print('*'*20)
    else:
        print('------- All 0, ignored -------')

### stackoverflow.com/questions/15869158/python-socket-listening
class DataSaver(threading.Thread):
    def __init__(self, conn, saveName='test_data_out.dat'):
        super(DataSaver, self).__init__()
        self.conn = conn
        self.data = ""
        self.saveName = saveName
        self.isDebug = False
    def run(self):
        with open(self.saveName, 'a') as fout:
            while True:
                print("testing....")
                self.data = self.conn.recv(1024)
                if self.isDebug: print(self.data)
                fout.write(self.data)
                self.data = ""

class MIC4Config():
    cmd = Cmd()

    def __init__(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sReg = MIC4Reg(0)
        self.dac = DAC8568(self.cmd)
        self.pCfg = PixelConfig(self.cmd, self.s)
        self.host = '192.168.2.3'

    def connect(self):
        port = 1024
        self.s.connect((self.host,port))

    def empty_fifo(self, nWord=1):
        cmdstr = ""
        cmdstr += self.cmd.read_datafifo(nWord)
        self.s.sendall(cmdstr)
        retw = self.s.recv(4*nWord)

        print([hex(ord(w)) for w in retw])
        print(len(retw))


    def shift_register_rw(self, data_to_send, clk_div, read=True):
        div_reg = (clk_div & 0x3f) | (1<<6)
#         div_reg = (clk_div & 0x3f)
#         div_reg = 0xff
        data_reg = data_to_send & ((1<<200)-1)
        print(bin(div_reg))

        val = div_reg | (data_reg<<8)
        cmdstr = ""
        for i in xrange(13):
            cmdstr += self.cmd.write_register(i, (val >> i*16) & 0xffff)
        cmdstr += self.cmd.send_pulse(0x01)
        self.s.sendall(cmdstr)

        # read back
        ret_all = None
        if read:
            nWord = 6
            time.sleep(1)
            cmdstr = ""
            cmdstr += self.cmd.read_datafifo(nWord)
            self.s.sendall(cmdstr)

            nByte = 4*(nWord+1)
            retw = self.s.recv(nByte)
            print([hex(ord(w)) for w in retw])
            print(len(retw))

            ret_all = 0
            for i in range(len(retw)):
                ret_all |= ord(retw[i])<<(nByte-i)*8
            ret_all = ret_all>>8
            
            print("Sent: %x" % data_to_send)
            print("Get : %x" % ret_all)
            c = data_to_send^ret_all
            if c!=0: print("Diff: %x" % c)
            else: print("Get == Sent")

        return ret_all

    def readFIFO_test(self, nWord=6):
        cmdstr = ""
        cmdstr += self.cmd.read_datafifo(nWord)
        self.s.sendall(cmdstr)

        nByte = 4*(nWord+1)
        retw = self.s.recv(nByte)
        print([hex(ord(w)) for w in retw])
        print(len(retw))

        ret_all = 0
        for i in range(len(retw)):
            ret_all |= ord(retw[i])<<(nByte-i)*8
        ret_all = ret_all>>8
        
        print("Get : %x" % ret_all)
        return ret_all


    def checkLastReg(self):
        cmdstr = ''
        cmdstr += self.cmd.read_register(0)
        self.s.sendall(cmdstr)
        retw = self.s.recv(4)
        print([hex(ord(w)) for w in retw])

    def readFD_debug(self):
        self.checkLastReg()
        cmdstr = ''
        cmdstr += self.cmd.send_pulse(1<<10)
        self.s.sendall(cmdstr)
        self.checkLastReg()

    def testRead(self, nWord=240):
        cmdstr = ""
        cmdstr += self.cmd.read_datafifo(nWord-1)
        self.s.sendall(cmdstr)

    def readFD(self, readOnly=True):
        cmdstr = ''
        cmdstr += self.cmd.write_register(0, 0)
        self.s.sendall(cmdstr)

        cmdstr = ''
        cmdstr += self.cmd.read_register(0)
        if not readOnly:
            cmdstr += self.cmd.send_pulse(1<<10)
        self.s.sendall(cmdstr)
        retw = self.s.recv(6)
        print("config:",[hex(ord(w)) for w in retw])
#         return 0

        nWord = 240 # 20 frames, each has 48 byte
        time.sleep(1)
        cmdstr = ""
        cmdstr += self.cmd.read_datafifo(nWord-1)
        self.s.sendall(cmdstr)

        nByte = 4*nWord
        retw = self.s.recv(nByte)

#         dataLS = []

        dx = [ord(w) for w in retw]
        idx =0

        nF = 48
        hd = findHeader(dx)
        print(dx)
        if hd>=0:
            while hd+nF<len(dx):
#                 print(hd, hd+nF, len(dx))
                parseFD(dx[hd:hd+nF])
                hd+=nF
        else:
            iN = 0
            while iN+nF<len(dx):
#                 print(dx[iN:iN+nF])
                iN+=nF
                parseFD(dx[iN:iN+nF])

#         data_t = None
#         for i in dx:
#             if i==0xbc:
#                 print('\n',idx,': ')
#                 idx+=1
# #                 if data_t: print(len(data_t))
#                 data_t = []
#             if data_t is not None: data_t.append(i)
#             if data_t and len(data_t) == 48:
#                 parseFD(data_t)
#             print(hex(i),end=' ')
#         print('\n')

#         print([hex(ord(w)) for w in retw])
#         print(len(retw))

        ret_all = 0
        for i in range(len(retw)):
#             print(bin(ord(retw[i])))
            ret_all |= ord(retw[i])<<(nByte-i)*8
#         print(ret_all)
        return ret_all

    def testReg(self, div=None, info=None, read=True):
        '''Test writing the register configure file'''
        if div is None: div = 10
        fifo_out = 1
        if info is None:
            #self.sReg.useDefault()
            print(self.sReg.value)
            info = self.sReg.getConf()
        rw = self.shift_register_rw(info, div, read)
        return rw


    def T(self):
        addr = 0
        n = 1

        cmdStr = ''
        cmdStr += self.cmd.send_pulse(1<<4)
        cmdStr += self.cmd.read_memory(addr,n)
        print("string:",cmdStr)
        print("string:",[ord(x) for x in cmdStr])

        self.s.sendall(cmdStr)
#         retw = self.s.recv(4)
        time.sleep(3)
        retw = self.s.recv(100)
        #retw = ord(self.s.recv(50))
        #retw = 0
        print("read (",len(retw),'):', [ord(x) for x in retw])

        ret = 0
        nword = len(retw)
        for i in range(nword):
            ret |= ord(retw[i])<<((nword-1-i)*8)
        print('N clock:', ret)

        return retw

    def setClocks(self, strobe_b, lt_div, clk_div):
        wd = 0
        wd |= (strobe_b&0x1) << 12
        wd |= (lt_div&0x3f) << 6
        wd |= (clk_div&0x3f)
        print(bin(wd))
        self.s.sendall(self.cmd.write_register(18, wd))

    def testStrobe(self, lt_div, clk_div):
        wd0 = 0
        wd0 |= (lt_div&0x3f) << 6
        wd0 |= (clk_div&0x3f)
        wd = 0
        wd |= 0x1 << 12
        wd |= (lt_div&0x3f) << 6
        wd |= (clk_div&0x3f)
        print(bin(wd))
        self.s.sendall(self.cmd.write_register(18, wd)+self.cmd.write_register(18, wd0)+self.cmd.write_register(18, wd))

    def sendGRST_B(self):
        self.s.sendall(self.cmd.send_pulse(0x20))
    def sendA_PULSE(self):
        self.s.sendall(self.cmd.send_pulse(0x40))
    def sendD_PULSE(self):
        self.s.sendall(self.cmd.send_pulse(0x80))
     
    def test_pixel_config(self):
        xyz = self.pCfg.get_test_vector()
        print(xyz)
        self.s.sendall(xyz)

    def setVhVl(self, vH=1.5, vL=0.5):
        ### Configure DAC8568
        cmdStr = ''
        val = 1.
        cmdStr += self.dac.turn_on_2V5_ref()			#turn on internal reference voltage
        cmdStr += self.dac.set_voltage(2, vH) # VPLUSE_HIGH
        cmdStr += self.dac.set_voltage(4, vL) # VPULSE_LOW
        self.s.sendall(cmdStr)
        ### 


    def test_DAC8568_config(self):
        ### Configure DAC8568
        cmdStr = ''
        val = 1.
        cmdStr += self.dac.turn_on_2V5_ref()			#turn on internal reference voltage
        #cmdStr += self.dac.set_voltage(2, 2)
        #for i in range(8):
        #    cmdStr += self.dac.set_voltage(i, val)
        cmdStr += self.dac.set_voltage(0, 1.2) # LT_VREF
#        cmdStr += self.dac.set_voltage(2, 1.5) # VPLUSE_HIGH
        cmdStr += self.dac.set_voltage(2, 1.5) # VPLUSE_HIGH

        cmdStr += self.dac.set_voltage(3, 1.2) # LVDS_REF
        cmdStr += self.dac.set_voltage(4, 0.5) # VPULSE_LOW
        #cmdStr += self.dac.set_voltage(6, 1.63) # DAC_REF
        cmdStr += self.dac.set_voltage(6, 1.2) # DAC_REF
#         cmdStr += self.dac.set_voltage(6, 0.6) # DAC_REF
#        cmdStr += self.dac.set_voltage(0, 2.5)
#        cmdStr += self.dac.set_voltage(1, 0)
#        cmdStr += self.dac.set_voltage(2, 0)
#        cmdStr += self.dac.set_voltage(3, 0)
#        cmdStr += self.dac.set_voltage(4, 0)
#        cmdStr += self.dac.set_voltage(5, 0)
#        cmdStr += self.dac.set_voltage(6, 0)
        self.s.sendall(cmdStr)
        ### 


class bitSet():
    def __init__(self,bits=[], reverse=False):
        self.value0 = 0
        self.value = 0
        self.reverse = reverse
        self.setBits(bits)
        self.outputLevel = 0
    def setBits(self, bits):
        self.bits = bits
        self.mask = 0
        for i in bits: self.mask |= 1<<i

    def parse(self, v):
        '''Set own value to v, using own bit map'''
        self.value0 = v
        self.value = 0
        nBits = len(self.bits)
        for i in range(nBits):
            v1 = (v>>i)&1
            j = i if not self.reverse else nBits-i-1
            if self.outputLevel <0:
                print('setting bit', self.bits, 'to', v1)
            self.value |= v1<<self.bits[j]

    def setTo(self, r):
        '''Set own value to the variable r, and return the new value of r'''
#         print(r, self.mask, self.value)
        return (r & ~self.mask)|(self.value & self.mask)
    def setValueTo(self, v, r):
        self.parse(v)
        return self.setTo(r)

    def test(self):
        self.setBits([0,4,8,12])
        for i in range(20):
            self.parse(i)
            print ('-----')
            print('{0:b} {1:b}'.format(i,self.mask))
            print('{0:b} {1:b}'.format(i,self.value))
            print('{0:b} {1:b}'.format(i,self.setTo(0xffff)))
    def getValue(self, v0, vMax=None, vMin=None):
        v = 0
        temp1 = reversed(self.bits) if self.reverse else self.bits
        for i,k in enumerate(temp1):
            # test bit k and set bit i
            v |= (((v0>>k) & 0x1) << i)

        # normalize using the given range
        if vMax is not None:
            vMn = 0 if vMin is None else vMin
            v = vMn+v*(vMax-vMn)/((1<<(len(self.bits)))-1)
        return v

class MIC4Reg(object):
    VCLIPBits  = bitSet([193,188,186,182,180,178,174,172,170,166],True) ### DATA<59:50>
    VResetBits = bitSet([137,141,143,147,149,152,155,157,161,163],True) ## DATA<49:40>
    VCASN2Bits = bitSet([128,124,122,118,116,114,110,108,106,102],True) # DATA<39:30>
    VCASNBits  = bitSet([194,189,187,183,181,179,175,173,171,167],True) # DATA<29:20>
    VCASPBits  = bitSet([136,140,142,146,148,151,154,156,160,162],True) # DATA<19:10>
    VRefBits   = bitSet([130,125,123,119,117,115,111,109,107,103],True) # DATA<9:0>
    IBIASBits  = bitSet([69,68,67,66,65,64,73,72],True) # Input_IBIAS<7:0> 
    IDBBits    = bitSet([94,93,92,91,90,89,99,98],True) # Input_IDB<7:0>
    ITHRBits   = bitSet([54,55,56,57,58,59,48,49],True) # Input_ITHR<7:0>
    IRESETBits = bitSet([40,39,38,37,36,35,45,44],True) # Input_IHEP_IRESET<7:0>
    IDB2Bits   = bitSet([81,82,83,84,85,86,76,77],True) # Input_IHEP_IDB2<7:0>

    vChanbits = bitSet([191,190,139,138,127,126],True) ### MONI_SEL<8:3>
    cChanbits = bitSet([96 ,50 ,63 ,80 ,41 ,51 ,62], True) ### MONI_SEL<2:0>, MONI_SEL_IHEP<3:0>
    selColbits = bitSet([23+(64-i) for i in range(64,53-1,-1)]+[42,43,46,47,52,53,60,61,70,71,74,75,78,79,87,88,95,97,100,101,104,105,112,113,120,121,129,131,132,133,134,135,144,145,150,153,158,159,164,165,168,169,176,177,184,185,192,195,196,197,198,199], True) ### COL_SEL, 64 bits 


    ### Voltage and current DAC list
    VList = [('VREF_Current_DAC','VRef'),('VCASN2','VCASN2'),('VReset','VReset'),('VCASP','VCASP'),('VCASN','VCASN'),('VCLIP','VCLIP')]
    IList = [('IBIAS_IHEP_40n','IBIAS'),('IHEP_IFOL_2n','ITHR'),('IHEP_IRESET_40p','IRESET'),('IHEP_IDB2','IDB2'),('IBIAS','IBIAS'),('ITHR','ITHR'),('IDB','IDB')]


    def __init__(self, value=0):
        self.value = value
    def selectVolDAC(self, chan):
        if chan>5:
            print("only 6 channels avaliable. Your input:", chan)
            return False
            ## raise error
        self.value = self.vChanbits.setValueTo((1<<chan)&0x3f, self.value)
        return True
    def selectCurDAC(self, chan):
        self.value = self.cChanbits.setValueTo((1<<chan)&0x7f, self.value)
    def selectCol(self, n):
        self.value = self.selColbits.setValueTo((1<<n)&0xffffffffffffffff, self.value)

    def setPDB(self, v):
        self.setBit(21,v)
    def setTEST(self, v):
        self.setBit(22,v)

    def setBit(self,n,v):
        mask = 1<<n
        self.value = (self.value & ~mask)|((v<<n) & mask)

    def show(self):
        print("Current configuration:")

        # Voltage DAC
        print ('-'*20)
        for i,k in enumerate(self.VList):
            flag = '+' if ((1<<i)&self.vChanbits.value0)!=0 else 'O'
            print(flag, k[0]+':','code={0:b}'.format(self.getPar(k[1])))

        # Current DAC
        print ('-'*20)
        for i,k in enumerate(self.IList):
            flag = '+' if ((1<<i)&self.cChanbits.value0)!=0 else 'O'
            print(flag, k[0]+':','code={0:b}'.format(self.getPar(k[1])))

        # select Collumn
        print('-'*10, len(self.selColbits.bits),'in total', '-'*10)
        for i,j in enumerate(reversed(self.selColbits.bits)):
            if (self.value & (1<<j))!=0:
                print('COL', i, 'Selected')

        # Other: TEST, PDB, LVDS_TEST, TRX16, TRX15_serializer
        print('-'*10,'Other','-'*10)
        print('TEST     :',(self.value>>22)&0x1)
        print('PDB      :',(self.value>>21)&0x1)
        print('TRX5_seri:',(self.value>>20)&0x1)
        print('TRX6_seri:',(self.value>>19)&0x1)
        print('TRX7_seri:',(self.value>>18)&0x1)
        print('TRX8_seri:',(self.value>>17)&0x1)
        print('TRX16    :',(self.value>>13)&0xf)
        print('LVDS_Test:',(self.value>>9)&0xf)

        # show bits that are set to 1
        temp_bits = [str(i) for i in range(200) if (self.value >> i)&0x1 != 0]
        print(','.join(temp_bits))

    def getPar(self,parname, vMax=None, vMin=None):
        try:
            x = getattr(self, parname+'Bits')
            if x:
                v = x.getValue(self.value, vMax, vMin)
                return v
        except AttributeError as e:
            print(e)
            sys.exit(1)

    def setPar(self, parname, v, refValue=None, refCode=None):
        try:
            x = getattr(self, parname+'Bits')
            if x:
                if refValue is not None:
                    c0 = (1<<len(x.bits))-1 if refCode is None else refCode
                    v = int(v*c0/refValue)
                self.value = x.setValueTo(v, self.value)
        except AttributeError as e:
            print(e)
            sys.exit(1)

    def setLVDS_TEST(self, v):
        n = 9
        mask = 0xf<<n
        self.value = (self.value & ~mask)|((v<<n) & mask)
    def setTRX16(self, v):
        n = 13
        mask = 0xf<<n
        self.value = (self.value & ~mask)|((v<<n) & mask)
    def setTRX15_serializer(self, v):
        n = 17
        mask = 0xf<<n
        self.value = (self.value & ~mask)|((v<<n) & mask)

    def useVolDAC(self, i, val):
        if self.selectVolDAC(i):
            self.setPar(self.VList[i][1], val)

    def useAllZero(self):
        self.value =  0
        self.setLVDS_TEST(0b1000)
        self.setTRX16(0b1000)
        self.setTRX15_serializer(0b1000)
        self.setPDB(0)
        self.setTEST(0)
        self.setPar('VCLIP', 0x0)
        self.setPar('VReset',0x0)
        self.setPar('VCASN2',0x0)
        self.setPar('VCASN', 0x0)
        self.setPar('VCASP', 0x0)
        self.setPar('VRef',  0x0)
        self.setPar('IBIAS', 0x0)
        self.setPar('IDB',   0x0)
        self.setPar('ITHR',  0x0)
        self.setPar('IRESET',0x0)
        self.setPar('IDB2',  0x0)
        self.selectVolDAC(0)
        self.selectCurDAC(0)

    def useDefaultIHEP(self):
        self.value =  0
        self.setLVDS_TEST(0b0000)
        self.setTRX16(0b1000)
        self.setTRX15_serializer(0b1000)
        self.setPDB(0)
        self.setTEST(0)
        self.setPar('VCLIP',0,0.075,0b0000101001)
        self.setPar('VReset',1.1, 0.484,0b0101010101)
        self.setPar('VCASN2',0.5, 0.57, 0b0110011001)
        self.setPar('VCASN',0.49, 0.381,0b0100010001)
        self.setPar('VCASP',0.37,1.040,0b1011101110)
        self.setPar('VRef',0.4, 0.4, 0b100011111)
#         self.setPar('VRef',0b0000010001)
        self.setPar('IBIAS',0x80)
        self.setPar('IDB',0x80)
        self.setPar('ITHR',0x80)
        self.setPar('IRESET',0x80)
        self.setPar('IDB2',0x80)
        # self.setPar('XYZ',0x80) ### test the exception handling
        self.selectVolDAC(5)
        self.selectCurDAC(0)

    def useDefault(self):
        self.value =  0
        self.setLVDS_TEST(0b0000)
        self.setTRX16(0b1000)
        self.setTRX15_serializer(0b1000)
        self.setPDB(0)
        self.setTEST(0)
        self.setPar('VCLIP',0,0.075,0b0000101001)
        self.setPar('VReset',1.1, 0.484,0b0101010101)
        self.setPar('VCASN2',0.5, 0.57, 0b0110011001)
        self.setPar('VCASN',0.4, 0.381,0b0100010001)
        self.setPar('VCASP',0.6,1.040,0b1011101110)
        self.setPar('VRef',0.4, 0.4, 0b100011111)
#         self.setPar('VRef',0b0000010001)
        self.setPar('IBIAS',0x80)
        self.setPar('IDB',0x80)
        self.setPar('ITHR',0x80)
        self.setPar('IRESET',0x80)
        self.setPar('IDB2',0x80)
        # self.setPar('XYZ',0x80) ### test the exception handling
        self.selectVolDAC(5)
        self.selectCurDAC(0)

    def getConf(self):
        ### if it's not clear what does this class is supposed to provide
        return self.value

    def test(self):
        pass
    def simpleCheck(self):
        dic1 = []
        dic1 += self.VCLIPBits.bits
        dic1 += self.VResetBits.bits
        dic1 += self.VCASN2Bits.bits
        dic1 += self.VCASNBits.bits
        dic1 += self.VCASPBits.bits
        dic1 += self.VRefBits.bits
        dic1 += self.IBIASBits.bits
        dic1 += self.IDBBits.bits
        dic1 += self.ITHRBits.bits
        dic1 += self.IRESETBits.bits
        dic1 += self.IDB2Bits.bits
        dic1 += self.vChanbits.bits
        dic1 += self.cChanbits.bits
        dic1 += self.selColbits.bits

        print(sorted(dic1))
        j = 0
        for i in range(200):
            if i not in dic1:
                print(j,':',i)
                j+=1


class PixelConfig():
    '''For pixel config'''
    def __init__(self, cmd, s):
        self.cmd = cmd
        self.s = s
        self.clk_div = 0
        self.pixels = [] ##(row[15:8], col[7:2], mask[1], pulse[0])
        self.isTest = False

    def setPixel(self, row, col, pulse, mask):
        pass

    def getConfList(self, list0=None):
        list1 = list0
        if list0 is None: list1 = self.pixels
        print("List1:", list1)

        listA = []
        w = None
        for x in list1:
            print(x)
            if w is None:
#                 w = ((x[0]&0x7ff)<<8)|((x[1]&0x3ff)<<2)|((x[2]&0x1)<<1)|(x[3]&0x1)
#                 w = w << 16
                w = self.getCode(x) << 16
            else:
#                 w |= ((x[0]&0x7ff)<<8)|((x[1]&0x3ff)<<2)|((x[2]&0x1)<<1)|(x[3]&0x1)
                w |= self.getCode(x) 
                listA.append(w)
                w = None
        if w is not None:
            x = list1[-1]
#             w |= ((x[0]&0x7ff)<<8)|((x[1]&0x3ff)<<2)|((x[2]&0x1)<<1)|(x[3]&0x1)
            w |= self.getCode(x) 
            listA.append(w)
            w = None

        if self.isTest:
            for w in listA: print(bin(w))
            return
        print(listA)
        return listA

    def getCode(self, x):
        return (x[0]&0x7ff)|((x[1]&0x3ff)<<7)|((x[2]&0x1)<<14)|((x[3]&0x1)<<13)

    def setAll2(self, mask, pulse):
        w = None
        for row in range(128):
            listA = []
            for col in range(64):
                ### do something
                if w is None:
                    w = self.getCode((row,col,mask, pulse)) << 16
#                     w = ((row&0x7ff)<<8)|((col&0x3ff)<<2)|((mask&0x1)<<1)|(pulse&0x1)
#                     w = w << 16
                else:
#                     w |= ((row&0x7ff)<<8)|((col&0x3ff)<<2)|((mask&0x1)<<1)|(pulse&0x1)
                    w |= self.getCode((row,col,mask, pulse))
                    listA.append(w)
                    w = None
            if self.isTest:
                print(listA[:10])
                continue
            self.applyConfig(listA)

    def setAll(self, mask, pulse):
        listA = []
        w = None
        for row in range(128):
            for col in range(64):
                ### do something
                if w is None:
                    w = ((row&0x7ff)<<8)|((col&0x3ff)<<2)|((mask&0x1)<<1)|(pulse&0x1)
                    w = w << 16
                else:
                    w |= ((row&0x7ff)<<8)|((col&0x3ff)<<2)|((mask&0x1)<<1)|(pulse&0x1)
                    listA.append(w)
                    w = None
        if self.isTest:
            print(listA[:10])
            return
        self.applyConfig(listA)

    def applyConfig(self, confList=None):
        confList1 = self.getConfList() if confList is None else confList
        print(confList1)

        data0 = (self.clk_div & 0x3f)
        addr = 0
        pls = 1<<2
        pls = 0xffff & pls

        print("Sending the configuration signal")
        cmdStr =''
        cmdStr += self.cmd.write_register(17, data0)
        cmdStr += self.cmd.write_memory(addr, confList1)
        self.s.sendall(cmdStr)
        time.sleep(1)
        print("Sending the load signal")
        cmdStr = ''
        cmdStr += self.cmd.send_pulse(pls)
        self.s.sendall(cmdStr)

## Command generator for controlling DAC8568
#
class DAC8568(object):
    '''used to generate the control string for DAC8568. 
    '''
 
    def __init__(self, cmd):
        self.cmd = cmd
    def DACVolt(self, x):
        '''Convert voltage to a 16'b number'''
        print("V=",x)
        #return int(x / 5. * 65536.0)    #calculation
        return int(x / 2.5 * 65536.0)    #calculation
    def write_spi(self, val):
        print(bin(val))
        ret = ""          # 32 bits, send two times, each for a half, starting with the higher one
        ret += self.cmd.write_register(16, (val >> 16) & 0xffff)
        ret += self.cmd.send_pulse(0x2)
        ret += self.cmd.write_register(16, val & 0xffff)
        ret += self.cmd.send_pulse(0x2)
        return ret
    def turn_on_2V5_ref(self):
        return self.write_spi(0x08000001)
    def set_voltage(self, ch, v):
        # 32 bit, first 8 is constent, next 4'b for channel, then the 16'b for voltage. Last 4'b is 0.
        # There is some issues, might overwrite some values in the current way. FIXME!
        return self.write_spi((0x03 << 24) | ((ch&0xf) << 20) | (self.DACVolt(v) << 4))
 
def mainTest():
    host = '192.168.2.3'
    port = 1024
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((host,port))

    cmd = Cmd()
    dac8568 = DAC8568(cmd)
    s.sendall(dac8568.turn_on_2V5_ref())
    s.sendall(dac8568.set_voltage(6, 1.2))

    # enable SDM clock
    s.sendall(cmd.write_register(9, 0x01))

    x2gain = 2
    bufferTest = True
    sdmTest = True

    tms1mmReg = TMS1mmReg()
    tms1mmReg.set_power_down(0, 0)
    tms1mmReg.set_power_down(3, 0)

    if bufferTest:
        tms1mmReg.set_k(0, 0) # 0 - K1 is open, disconnect CSA output
        tms1mmReg.set_k(1, 1) # 1 - K2 is closed, allow BufferX2_testIN to inject signal
        tms1mmReg.set_k(4, 0) # 0 - K5 is open, disconnect SDM loads
        tms1mmReg.set_k(6, 1) # 1 - K7 is closed, BufferX2 output to AOUT_BufferX2
    if x2gain == 2:
        tms1mmReg.set_k(2, 1) # 1 - K3 is closed, K4 is open, setting gain to X2
        tms1mmReg.set_k(3, 0)
    else:
        tms1mmReg.set_k(2, 0)
        tms1mmReg.set_k(3, 1)
    if sdmTest:
        tms1mmReg.set_k(4, 0)
        tms1mmReg.set_k(5, 1)
    else:
        tms1mmReg.set_k(5, 0)

    tms1mmReg.set_k(6, 1) # 1 - K7 is closed, BufferX2 output to AOUT_BufferX2
    tms1mmReg.set_k(7, 1) # 1 - K8 is closed, connect CSA out to AOUT1_CSA
    tms1mmReg.set_dac(0, tms1mmReg.dac_volt2code(1.38)) # VBIASN R45
    tms1mmReg.set_dac(1, tms1mmReg.dac_volt2code(1.55)) # VBIASP R47
    tms1mmReg.set_dac(2, tms1mmReg.dac_volt2code(1.45)) # VCASN  R29
    tms1mmReg.set_dac(3, tms1mmReg.dac_volt2code(1.35)) # VCASP  R27
    # tms1mmReg.set_dac(4, dac_volt2code(1.58)) # VDIS   R16, use external DAC
    s.sendall(dac8568.set_voltage(4, 1.58))
    tms1mmReg.set_dac(5, tms1mmReg.dac_volt2code(2.68)) # VREF   R14

    data_to_send = tms1mmReg.get_config_vector()
    print("Sent: 0x%0x" % (data_to_send))

    div=7
    shift_register_rw(s, (data_to_send), div)

    s.close()

def testReg():
    r1 = MIC4Reg()
#     r1.setPar('VRef',0xfe)
#     r1.setPar('VRef',1.4,1.5)
    r1.setPar('VRef',1.4,2.,0xff)
    r1.show()

def testPConf():
    c1 = PixelConfig(None, None)
    c1.isTest = True
#     c1.setAll(1,0)
    c1.pixels.append((127,0,1,0))
    print(c1.pixels)
    c1.getConfList()
#     c1.applyConfig()

def testDataSave():
    mc1 = MIC4Config()
    mc1.connect()
    print("JJJJJ")

    ### create connection
#     host = '192.168.2.3'
#     port = 1024
#     s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#     s.connect((host,port))

    ### setup the device
    mc1.test_DAC8568_config()
    mc1.setClocks(0,6,6)
    mc1.sReg.useDefault() 
    mc1.sReg.show()
    mc1.testReg(read=True)

    ### Start listening
    c = DataSaver(mc1.s)
    c.isDebug = True
    c.start()

    print("testing XXJ")

    ### Send A-Pulse
    mc1.sendD_PULSE()
    mc1.testRead(5)
#     mc1.readFD(readOnly=False)
#     mc1.rea

    print("testing Y")

    ### Finish and close
#     c.close()
    mc1.s.close()

if __name__ == "__main__":
#     testReg()
#     testPConf()
    testDataSave()
