#!/usr/bin/env python
# -*- coding: utf-8 -*-

## @package MIC4Config
# Control module for the Topmetal-S 1mm Electrode single-chip test.
#

from __future__ import print_function
import copy
from command import *
import socket
import time
import sys

## Manage Topmetal-S 1mm chip's internal register map.
# Allow combining and disassembling individual registers
# to/from long integer for I/O
#

class MIC4Config():
    cmd = Cmd()

    def __init__(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sReg = MIC4Reg(0)
        self.dac = DAC8568(self.cmd)
        self.pCfg = PixelConfig(self.cmd, self.s)

    def connect(self):
        host = '192.168.2.3'
        port = 1024
        self.s.connect((host,port))

    def configReg(self):
        div = 1
        fifo_out = 1
        dxc = self.sReg.getConf()
        print('{0:x}'.format(dxc))

        cmdStr = ''
        for i in range(13):
            din = 0xffff & dxc
            cmdStr += self.cmd.write_register(0, din)
            cmdStr += self.cmd.send_pulse(3)

            ### shift dxc
            dxc = dxc>>16
            print('{1:d} {0:x} {2:x}'.format(dxc, i, din))

        ### send data to register and read them back
        cmdStr += self.cmd.write_register(1, (div<<1)+fifo_out)
        cmdStr += self.cmd.send_pulse(0)
        cmdStr += self.cmd.read_datafifo(200)
        self.s.sendall(cmdStr)

        ### read back
        rw = self.s.recv(25, socket.MSG_WAITALL)
        return rw

    def shift_register_rw(self, data_to_send, clk_div, read=True):
        div_reg = ((clk_div & 0x3f) | (1<<6)) << 200
        data_reg = data_to_send & ((1<<200)-1)

        val = div_reg | data_reg
        cmdstr = ""
        for i in xrange(13):
            cmdstr += self.cmd.write_register(i, (val >> i*16) & 0xffff)
        cmdstr += self.cmd.send_pulse(0x01)
        self.s.sendall(cmdstr)

        # read back
        ret = 0
        if read:
            nWord = 7
            time.sleep(0.2)
            cmdstr = ""
            cmdstr += self.cmd.read_datafifo(nWord)
            self.s.sendall(cmdstr)

            retw = s.recv(4*nWord, socket.MSG_WAITALL)
            print([hex(ord(w)) for w in retw])
            print(len(retw))

            for i in xrange(nWord):
                ret = ret | ( int(ord(retw[i*4+2])) << ((nWord+1-i) * 16 + 8) |
                              int(ord(retw[i*4+3])) << ((nWord+1-i) * 16))
            ret = ret & ((1<<200)-1) 
        return ret

        ret_all = 0
        for i in xrange(7):
            ret_all = ret_all | int(ord(retw[i*4+2])) << ((10-i) * 16 + 8) | int(ord(retw[i*4+3])) << ((10-i) * 16)
        ret = ret_all & ((1<<200)-1)
        valid = (ret_all & (1 <<200)) >> 200
        print("%x" % data_to_send)
        print("%x" % ret)
        print(valid)
        return valid

    def testReg(self, div=None, info=None, read=True):
        '''Test writing the register configure file'''
        if div is None: div = 7
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
        retw = self.s.recv(4)
        #retw = ord(self.s.recv(50))
        #retw = 0
        print("read (",len(retw),'):', [ord(x) for x in retw])

        return retw

    def setClocks(self, strobe_b, lt_div, clk_div):
        wd = 0
        wd |= (strobe_b&0x1) << 12
        wd |= (lt_div&0x3f) << 6
        wd |= (clk_div&0x3f)
        print(bin(wd))
        self.s.sendall(self.cmd.write_register(2, wd))

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

    def test_DAC8568_config(self):
        ### Configure DAC8568
        cmdStr = ''
        val = 1.
        cmdStr += self.dac.turn_on_2V5_ref()			#turn on internal reference voltage
        #cmdStr += self.dac.set_voltage(2, 2)
        #for i in range(8):
        #    cmdStr += self.dac.set_voltage(i, val)
        cmdStr += self.dac.set_voltage(0, 1.2) # LT_VREF
        cmdStr += self.dac.set_voltage(2, 1.4) # VPLUSE_HIGH
        cmdStr += self.dac.set_voltage(3, 1.2) # LVDS_REF
        cmdStr += self.dac.set_voltage(4, 0.8) # VPULSE_LOW
        #cmdStr += self.dac.set_voltage(6, 1.63) # DAC_REF
        cmdStr += self.dac.set_voltage(6, 1.2) # DAC_REF
#        cmdStr += self.dac.set_voltage(0, 2.5)
#        cmdStr += self.dac.set_voltage(1, 0)
#        cmdStr += self.dac.set_voltage(2, 0)
#        cmdStr += self.dac.set_voltage(3, 0)
#        cmdStr += self.dac.set_voltage(4, 0)
#        cmdStr += self.dac.set_voltage(5, 0)
#        cmdStr += self.dac.set_voltage(6, 0)
        self.s.sendall(cmdStr)
        ### 


    def test(self):
        print("testing...")

        div = 1
        fifo_out = 1
        dx = 0xabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcde
        dxc = dx
        print('{0:x}'.format(dxc))

        cmdStr = ''
        for i in range(13):
            din = 0xffff & dxc
            cmdStr += self.cmd.write_register(0, din)
            cmdStr += self.cmd.send_pulse(3)

            ### shift dxc
            dxc = dxc>>16
            print('{1:d} {0:x} {2:x}'.format(dxc, i, din))

        ### send data to register and read them back
        cmdStr += self.cmd.write_register(1, (div<<1)+fifo_out)
        cmdStr += self.cmd.send_pulse(0)
#        cmdStr += self.cmd.read_datafifo(200)

        print([ord(x) for x in cmdStr])
        print(len([ord(x) for x in cmdStr]))
        print(cmdStr)
        self.s.sendall(cmdStr)

        ### read back
#         ret = self.s.recv(25, socket.MSG_WAITALL)
#         print rw

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
            ## raise error
        self.value = self.vChanbits.setValueTo((1<<chan)&0x3f, self.value)
    def selectCurDAC(self, chan):
        self.value = self.cChanbits.setValueTo((1<<chan)&0x3f, self.value)
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

    def getPar(self,parname, vMax=None, vMin=None):
        try:
            x = getattr(self, parname+'Bits')
            if x:
                v = x.getValue(self.value, vMax, vMin)
                return v
        except AttributeError as e:
            print(e)
            sys.exit(1)

    def setPar(self, parname, v):
        try:
            x = getattr(self, parname+'Bits')
            if x:
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

    def useDefault(self):
        self.value =  0
        self.setLVDS_TEST(0b1000)
        self.setTRX16(0b1000)
        self.setTRX15_serializer(0b1000)
        self.setPDB(0)
        self.setTEST(0)
        self.setPar('VCLIP',0b0000101001)
        self.setPar('VReset',0b0101010101)
        self.setPar('VCASN2',0b0110011001)
        self.setPar('VCASN',0b0100010001)
        self.setPar('VCASP',0b1011101110)
        self.setPar('VRef',0b0100010001)
        self.setPar('IBIAS',0x80)
        self.setPar('IDB',0x80)
        self.setPar('ITHR',0x80)
        self.setPar('IRESET',0x80)
        self.setPar('IDB2',0x80)
        # self.setPar('XYZ',0x80) ### test the exception handling
        self.selectVolDAC(0)
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
    '''Auxilary class for pxiel config.'''
    def __init__(self, cmd, s):
        self.cmd = cmd
        self.s = s
        self.allAre = None

    def reset(self, state=None):
        self.allAre = state
        self.Pixels = []

        cmdStr = self.getConfigVector()
        self.s.sendall()

    def setPixel(self, x, y, pulse, mask):
        self.pixels.append((x+(y<<6),pulse+(mask<<1)))

    def getConfigVector(self, clk_div):
        ### address + config
        data0 = 0
        data0 |= (clk_div & 0x3f)

        n = 0
        data1 = 0
        if self.allAre is not None:
            for i in range():
                for j in range():
                    data1 = data1<<16

        cmdStr = ''
        cmdStr += self.cmd.write_register(0, data0)
        cmdStr += self.cmd.write_memory(0, data1, n)
        cmdStr += self.cmd.send_pulse(0x4)
    def get_test_vector(self):
        clk_div = 7
        data0 = 0
        data0 |= (clk_div & 0x3f)
 
        data1 = [i&0xffff for i in range(10)]
        print(data1)

        cmdStr = ''
        cmdStr += self.cmd.write_register(0, data0)
        cmdStr += self.cmd.write_memory(0, data1)
        print(cmdStr)

        self.s.sendall(cmdStr)

        cmdStr = ''
        time.sleep(1)
        cmdStr += self.cmd.send_pulse(0x4)
        print(cmdStr)
        self.s.sendall(cmdStr)
        return cmdStr
        

class MIC4Reg0(object):
    ## @var _defaultRegMap default register values
    _defaultRegMap = {
        'DAC'    : [0x75c3, 0x8444, 0x7bbb, 0x7375, 0x86d4, 0xe4b2], # from DAC1 to DAC6
        'PD'     : [1, 1, 1, 1], # from PD1 to PD4, 1 means powered down
        'K'      : [1, 0, 1, 0, 1, 0, 0, 0, 0, 0], # from K1 to K10, 1 means closed (conducting)
        'vref'   : 0x8,
        'vcasp'  : 0x8,
        'vcasn'  : 0x8,
        'vbiasp' : 0x8,
        'vbiasn' : 0x8
    }
    ## @var register map local to the class
    _regMap = {}

    def __init__(self):
        self._regMap = copy.deepcopy(self._defaultRegMap)

    def set_dac(self, i, val):
        self._regMap['DAC'][i] = 0xffff & val

    def set_power_down(self, i, onoff):
        self._regMap['PD'][i] = 0x1 & onoff

    def set_k(self, i, onoff):
        self._regMap['K'][i] = 0x1 & onoff

    def set_vref(self, val):
        self._regMap['vref'] = val & 0xf

    def set_vcasp(self, val):
        self._regMap['vcasp'] = val & 0xf

    def set_vcasn(self, val):
        self._regMap['vcasn'] = val & 0xf

    def set_vbiasp(self, val):
        self._regMap['vbiasp'] = val & 0xf

    def set_vbiasn(self, val):
        self._regMap['vbiasn'] = val & 0xf

    ## Get long-integer variable
    def get_config_vector(self):
        ret = ( self._regMap['vbiasn'] << 126 |
                self._regMap['vbiasp'] << 122 |
                self._regMap['vcasn']  << 118 |
                self._regMap['vcasp']  << 114 |
                self._regMap['vref']   << 110 )
        for i in xrange(len(self._regMap['K'])):
            ret |= self._regMap['K'][i] << (len(self._regMap['K']) - i) + 99
        for i in xrange(len(self._regMap['PD'])):
            ret |= self._regMap['PD'][i] << (len(self._regMap['PD']) - i) + 95
        for i in xrange(len(self._regMap['DAC'])):
            ret |= self._regMap['DAC'][i] << (len(self._regMap['DAC'])-1 - i)*16
        return ret

    dac_fit_a = 4.35861E-5
    dac_fit_b = 0.0349427
    def dac_volt2code(self, v):

        c = int((v - self.dac_fit_b) / self.dac_fit_a)
        if c < 0:     c = 0
        if c > 65535: c = 65535
        return c

    def dac_code2volt(self, c):
        v = c * self.dac_fit_a + self.dac_fit_b
        return v


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
        ret += self.cmd.write_register(0, (val >> 16) & 0xffff)
        ret += self.cmd.send_pulse(0x2)
        ret += self.cmd.write_register(0, val & 0xffff)
        ret += self.cmd.send_pulse(0x2)
        return ret
    def turn_on_2V5_ref(self):
        return self.write_spi(0x08000001)
    def set_voltage(self, ch, v):
        # 32 bit, first 8 is constent, next 4'b for channel, then the 16'b for voltage. Last 4'b is 0.
        # There is some issues, might overwrite some values in the current way. FIXME!
        return self.write_spi((0x03 << 24) | ((ch&0xf) << 20) | (self.DACVolt(v) << 4))
 
## Shift_register write and read function.
#
# @param[in] s Socket that is already open and connected to the FPGA board.
# @param[in] data_to_send 130-bit value to be sent to the external SR.
# @param[in] clk_div Clock frequency division factor: (/2**clk_div).  6-bit wide.
# @return Value stored in the external SR that is read back.
# @return valid signal shows that the value stored in external SR is read back.
def shift_register_rw(s, data_to_send, clk_div):
    div_reg = (clk_div & 0x3f) << 130
    data_reg = data_to_send & 0x3ffffffffffffffffffffffffffffffff

    cmd = Cmd()

    val = div_reg | data_reg
    cmdstr = ""
    for i in xrange(9):
        cmdstr += cmd.write_register(i, (val >> i*16) & 0xffff)

    cmdstr += cmd.send_pulse(0x01)

#    print([hex(ord(w)) for w in cmdstr])

    s.sendall(cmdstr)

    time.sleep(0.5)

    # read back
    cmdstr = ""
    for i in xrange(9):
        cmdstr += cmd.read_status(8-i)
    s.sendall(cmdstr)
    retw = s.recv(4*9)
#    print([hex(ord(w)) for w in retw])
    ret_all = 0
    for i in xrange(9):
        ret_all = ret_all | ( int(ord(retw[i*4+2])) << ((8-i) * 16 + 8) |
                              int(ord(retw[i*4+3])) << ((8-i) * 16))
    ret = ret_all & 0x3ffffffffffffffffffffffffffffffff
    valid = (ret_all & (1 << 130)) >> 130
    print("Return: 0x%0x, valid: %d" % (ret, valid))
    return ret

if __name__ == "__main__":

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
