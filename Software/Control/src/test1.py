#!/usr/bin/env python
import sys
import time
from MIC4Config import MIC4Config, bitSet

def check_FDout(mc1, iTest=10):
#     setAllPixels(mc1, mask=1, pulse_en=0)
#     setAllPixels(mc1, mask=1, pulse_en=0)
#     setPixels(mc1,[(127,0,0,1),(127,1,0,1),(127,3,0,1),(127,3,0,1)])
#     sys.exit(0)

    mc1.setClocks(0,6,6)
    mc1.test_DAC8568_config()
    mc1.sReg.useDefault() 
#     mc1.sReg.setTEST(1)
    mc1.sReg.show()
    mc1.testReg(read=True)
    sys.exit(0)

    i = 0
    while i!=iTest:
        print i, 'event'
        i += 1
        try:
            mc1.sendD_PULSE()
        except KeyboardInterrupt:
            break


def D_signal_checks(mc1):
    mc1.sendGRST_B()
#     mc1.setClocks(0,6,6)
#     mc1.sendD_PULSE()

def testRegister(mc1):
    mc1.test_DAC8568_config()
    mc1.setClocks(0,6,6)
#     mc1.sReg.value = 1
#     mc1.sReg.value =0b100101
    mc1.sReg.useDefault() 
#     mc1.sReg.selectVolDAC(1)
#     mc1.sReg.useVolDAC(1, 0x3ff)
#     mc1.sReg.setLVDS_TEST(0b1000)
#     mc1.sReg.setTRX16(0b1000)
#     mc1.sReg.setTRX15_serializer(0b1000)
    mc1.sReg.show()
    mc1.testReg(read=True)
#     mc1.testReg(read=False)

def lvds_test(mc1):
    mc1.test_DAC8568_config()
    mc1.sReg.value = 0
    mc1.sReg.setLVDS_TEST(0b1000)
    mc1.sReg.setTRX16(0b1000)
    mc1.sReg.setTRX15_serializer(0b1000)
    mc1.sReg.show()
#     mc1.testReg(read=True)
    mc1.testReg(read=False)
    mc1.setClocks(1,8,8)

def checkDefaultDACinChip(mc1):
    mc1.sReg.value = 0
    mc1.sReg.useDefault()
    mc1.sReg.selectVolDAC(0)
    mc1.sReg.show()
    mc1.testReg(read=True)

def CheckValid(mc1):
    mc1.setClocks(1,6,6)
    mc1.sendD_PULSE()
#     mc1.sendGRST_B()

def checkSysCLKchange(mc1):
    mc1.setClocks(1,6,6)
    mc1.sReg.value = 1
    mc1.sReg.show()
    mc1.testReg(read=True)
#     mc1.setClocks(1,10,10)

def test_AOUT_IHEP(mc1):
#     mc1.test_DAC8568_config()
#     mc1.sReg.useDefault()
    mc1.sReg.value =  0
    mc1.sReg.setPDB(0)
    mc1.sReg.setPar('VCLIP',0,0.075,0b0000101001)
    mc1.sReg.setPar('VReset',1.1, 0.484,0b0101010101)
    mc1.sReg.setPar('VCASN2',0.5, 0.57, 0b0110011001)
    mc1.sReg.setPar('VCASN',0.49, 0.381,0b0100010001)
    mc1.sReg.setPar('VCASP',0.37,1.040,0b1011101110)
    mc1.sReg.setPar('VRef',0.4, 0.4, 0b100011111)
    mc1.sReg.setPar('IBIAS',0x80)
    mc1.sReg.setPar('IDB',0x80)
    mc1.sReg.setPar('ITHR',0x80)
    mc1.sReg.setPar('IRESET',0x80)
    mc1.sReg.setPar('IDB2',0x80)
    mc1.sReg.selectVolDAC(5)
    mc1.sReg.selectCurDAC(0)
    mc1.sReg.selectCol(0)

    mc1.sReg.show()
    mc1.testReg(read=True)
#     mc1.setClocks(1,6,6)

    time.sleep(1)
    mc1.sendA_PULSE()


def test_AOUT_loop(mc1):
#     mc1.test_DAC8568_config()

    for i in range(32):
        mc1.sReg.value =  0
        mc1.sReg.setPDB(0)
        mc1.sReg.setPar('VCLIP' ,1.0,  0.833, 0b1001011001)
        mc1.sReg.setPar('VCASN' ,0.4,  0.384, 0b100011110)
        mc1.sReg.setPar('VCASP' ,0.5,  0.603, 0b110110000)
        mc1.sReg.setPar('VReset',1.1,  1.084, 0b1100000111)
        mc1.sReg.setPar('VCASN2',0.5,  0.502, 0b101100110)
        mc1.sReg.setPar('VRef'  ,0.4,  0.406, 0b100011111)
        mc1.sReg.setPar('IBIAS' ,0xff)
        mc1.sReg.setPar('IDB'   ,0x80)
        mc1.sReg.setPar('ITHR'  ,0xff)
        mc1.sReg.setPar('IRESET',0x80)
        mc1.sReg.setPar('IDB2'  ,0x80)
        mc1.sReg.selectVolDAC(5)
        mc1.sReg.selectCurDAC(6)
        mc1.sReg.selectCol(i)

        mc1.sReg.show()
        mc1.testReg(read=True)

        print '-'*10,"On pixel", i,'-'*10
        time.sleep(1)
        mc1.sendA_PULSE()

def test_AOUT_IHEP_loop(mc1):
    for i in range(32,64):
        mc1.sReg.value =  0
        mc1.sReg.setPDB(0)
        mc1.sReg.setPar('VCLIP',0,0.075,0b0000101001)
        mc1.sReg.setPar('VReset',1.1, 0.484,0b0101010101)
        mc1.sReg.setPar('VCASN2',0.5, 0.57, 0b0110011001)
        mc1.sReg.setPar('VCASN',0.49, 0.381,0b0100010001)
        mc1.sReg.setPar('VCASP',0.37,1.040,0b1011101110)
        mc1.sReg.setPar('VRef',0.4, 0.4, 0b100011111)
        mc1.sReg.setPar('IBIAS',0x80)
        mc1.sReg.setPar('IDB',0x80)
        mc1.sReg.setPar('ITHR',0x80)
        mc1.sReg.setPar('IRESET',0x80)
        mc1.sReg.setPar('IDB2',0x80)
        mc1.sReg.selectVolDAC(5)
        mc1.sReg.selectCurDAC(6)
        mc1.sReg.selectCol(i)

        mc1.sReg.show()
        mc1.testReg(read=True)

        print "On pixel", i
        time.sleep(1)
        mc1.sendA_PULSE()

def test_AOUT(mc1):
    mc1.setClocks(0,6,6)
#     sys.exit(1)
    mc1.test_DAC8568_config()
# # #     mc1.sReg.useDefault()
    mc1.sReg.value =  0
    mc1.sReg.setPDB(0)
    mc1.sReg.setPar('VCLIP' ,0.1,  0.833, 0b1001011001)
    mc1.sReg.setPar('VCASN' ,0.4,  0.384, 0b100011110)
    mc1.sReg.setPar('VCASP' ,0.5,  0.603, 0b110110000)
    mc1.sReg.setPar('VReset',1.1,  1.084, 0b1100000111)
    mc1.sReg.setPar('VCASN2',0.5,  0.502, 0b101100110)
    mc1.sReg.setPar('VRef'  ,0.4,  0.406, 0b100011111)
    mc1.sReg.setPar('IBIAS' ,0xc9)
    mc1.sReg.setPar('IDB'   ,0x80)
    mc1.sReg.setPar('ITHR'  ,0xff)
    mc1.sReg.setPar('IRESET',0x80)
    mc1.sReg.setPar('IDB2'  ,0x80)
    mc1.sReg.selectVolDAC(3)
    mc1.sReg.selectCurDAC(0)
    mc1.sReg.selectCol(0)

    mc1.sReg.show()
    mc1.testReg(read=True)
# #     mc1.setClocks(1,6,6)

#     time.sleep(1)
#     mc1.sendA_PULSE()


def check_DOUT(mc1):
    mc1.setClocks(0,6,6)

def test_DOUT(mc1):
    mc1.setClocks(1,5,5)
    mc1.test_DAC8568_config()
    mc1.sReg.value = 1
#     mc1.sReg.setLVDS_TEST(0b1000)
#     mc1.sReg.setTRX16(0b1000)
#     mc1.sReg.setTRX15_serializer(0b1000)
    mc1.sReg.show()
    mc1.testReg(read=True)
    sys.exit(0)

    print "start in 2 s"
    time.sleep(2)
    for i in range(21):
        mc1.setClocks(1,6,20-i)
        print "i=",i
        time.sleep(10)

#     time.sleep(1)
#     mc1.sendD_PULSE()

def setupDOUT(mc1):
    mc1.setClocks(1,6,6)
    mc1.test_DAC8568_config()
    mc1.sReg.useDefault()
#     mc1.sReg.value =  0x1f
# #     mc1.sReg.setTRX16(0b1000)
# #     mc1.sReg.setTRX15_serializer(0b1000)
    mc1.sReg.show()
#     mc1.testReg(read=True)
    mc1.testReg(read=False)
# 
#     mc1.checkLastReg()
#     for i in range(100):
#         print i
#         mc1.readFIFO_test(6)
# 
#     sys.exit(1)
    mc1.readFD()
    mc1.checkLastReg()

def checkCol(mc1):
    i = 0 if len(sys.argv)<2 else int(sys.argv[1])
    if i<32:
        mc1.sReg.useDefault()
    else:
        mc1.sReg.useDefaultIHEP()
    mc1.sReg.selectCol(i)
    mc1.sReg.setPDB(0)
    mc1.sReg.show()
    mc1.testReg(read=True)

    time.sleep(1)
    mc1.sendA_PULSE()
    time.sleep(2)


def loopCol(mc1):
#     for i in range(32):
    for i in range(32,64):
        print 'Col:', i
        if i<32:
            mc1.sReg.useDefault()
        else:
            mc1.sReg.useDefaultIHEP()
        mc1.sReg.selectCol(i)
        mc1.testReg(read=True)

        time.sleep(1)
        mc1.sendA_PULSE()
        time.sleep(2)

def setPixels(mc1,pxiels):
    mc1.setClocks(1,8,8) # from 250 MHz clock
    mc1.test_DAC8568_config()
    mc1.pCfg.clk_div = 18 # from 100 MHz clock
    mc1.pCfg.pixels = pxiels
    mc1.pCfg.applyConfig()

def setAllPixels(mc1,pulse_en=0, mask=0):
    mc1.setClocks(1,8,8) # from 250 MHz clock
    mc1.test_DAC8568_config()
    mc1.pCfg.clk_div = 18 # from 100 MHz clock
    for r in range(128):
        print "turning off row", r
        mc1.pCfg.pixels = [(r,i,mask,pulse_en) for i in range(64)]
        mc1.pCfg.applyConfig()

def setLastRow(mc1, pulse_en=1, mask=0):
    mc1.setClocks(1,8,8) # from 250 MHz clock
    mc1.test_DAC8568_config()
    mc1.pCfg.clk_div = 18 # from 100 MHz clock
    mc1.pCfg.pixels = [(127,i,mask,pulse_en) for i in range(64)]
    mc1.pCfg.applyConfig()

def busySigal(mc1):
    mc1.setClocks(1,8,8) # from 250 MHz clock
    mc1.test_DAC8568_config()
    mc1.pCfg.clk_div = 18 # from 100 MHz clock
    mc1.pCfg.pixels = [(127,0,0,1)]# for i in range(64)]
#     mc1.pCfg.pixels = [(127,0,0,0),(127,0,0,1),(127,0,1,1),(127,0,1,0)]# for i in range(64)]
    mc1.pCfg.applyConfig()

def testPixels(mc1):
    mc1.test_DAC8568_config()
    sys.exit(1)
# #     mc1.sReg.value = 0
#     mc1.sReg.value = 1
    mc1.sReg.useDefault()
#     mc1.sReg.selectCol(0)
    mc1.sReg.setPDB(0)
    mc1.sReg.setTEST(1)
#  
# #     mc1.sReg.value |= (0x1<<199)
    mc1.sReg.show()
#     sys.exit(1)
# #     mc1.sReg.value = mc1.sReg.value >> 1
    mc1.testReg(read=True)
    mc1.setClocks(1,6,6)
    sys.exit(1)
# 
    mc1.pCfg.clk_div = 5
#     mc1.pCfg.setAll(1,0)
    mc1.pCfg.pixels = [(127,0,0,1)]# for i in range(64)]
#     mc1.pCfg.pixels = [(127,i,0,1) for i in range(64)]
    mc1.pCfg.applyConfig()
#     mc1.sendA_PULSE()

def testA(mc1):
#     #mc1.sReg.useDefault()
#     mc1.sReg.value = 123456
# #     mc1.sReg.selectCol(23)
#     mc1.sReg.show()
#     sys.exit(0)

#     print(mc1.T())
    #mc1.test()
    mc1.setClocks(1,5,5)
    mc1.test_DAC8568_config()
#     mc1.pCfg.clk_div = 20
#     mc1.pCfg.pixels = [(1,1,1,0),(1,1,0,1)]
#     mc1.pCfg.applyConfig()
#     mc1.pCfg.setAll(1,0)
#     sys.exit(0)

#     mc1.empty_fifo()
    mc1.sendGRST_B()
    mc1.sendA_PULSE()
    mc1.sendD_PULSE()
    sys.exit(0)
# 
    ### --- CAUTION: all channel open, for TEST ONLY
#     mc1.sReg.vChanbits.outputLevel = -1
#     mc1.sReg.value = mc1.sReg.vChanbits.setValueTo(0x3f, mc1.sReg.value)

#     mc1.sReg.selectVolDAC(1)
#     mc1.sReg.selectCurDAC(1) 
#     mc1.sReg.value = 1<<124
    mc1.sReg.value = 1
#     mc1.sReg.useDefault()
#     mc1.sReg.selectCol(0)
#     mc1.sReg.setPar('IBIAS' ,0xff)
#     mc1.sReg.setPar('IDB'   ,0xff)
#     mc1.sReg.setPar('ITHR'  ,0xff)
#     mc1.sReg.setPar('IRESET',0xff)
#     mc1.sReg.setPar('IDB2'  ,0xff)
#     mc1.sReg.selectCurDAC(5)
#     mc1.sReg.setLVDS_TEST(0b1000)
#     mc1.sReg.setTRX16(0b1000)
#     mc1.sReg.setTRX15_serializer(0b1000)

#     mc1.sReg.useVolDAC(0, 0x000)
#     mc1.sReg.useVolDAC(4, 0x20)
#     mc1.sReg.setPar('VCASN',  0x3ff)
#     mc1.sReg.setPar('VCASN2', 0x3ff)
#     mc1.sReg.setPar('VCASP',  0x3ff)
#     mc1.sReg.setPar('VReset', 0x3ff)
#     mc1.sReg.setPar('VCLIP',  0x3ff)
#     mc1.sReg.setPar('VRef',   0x3ff)
#     mc1.sReg.setPDB(1)
#     mc1.sReg.selectVolDAC(0)

#     mc1.sReg.useVolDAC(1, 0x3ff)
#     mc1.sReg.useVolDAC(0, 0x2ff)
#     mc1.sReg.setPar('VRef', 0x2ff)
#     mc1.sReg.setPar('VCASN2', 0x3ff)
#     mc1.sReg.selectVolDAC(5)
#     mc1.sReg.useAllZero()


    ## reverse
#     test_valueBit  = bitSet([i for i in range(200)],True)
#     mc1.sReg.value = test_valueBit.setValueTo(mc1.sReg.value, mc1.sReg.value)

    print bin(mc1.sReg.value)
#     for i,j in enumerate(reversed(bin(mc1.sReg.value))[2:]):
#         if int(j)!=0: print i,j, 199-i
    mc1.sReg.show()
#     mc1.sReg.value = mc1.sReg.value >> 1
    mc1.testReg(read=True)
    #x = mc1.shift_register_rw(0xabcdeabcdeabcdeabcde, 8)
    #print(x)
    #sys.exit(0)

    
    #for i in range(1):
    #    print mc1.T()
#     bs1 = bitSet()
#     bs1.test()
    #mc1.test_pixel_config()
    #mc1.pCfg.get_test_vector()
#    testRegister(mc1)
    #mc1.sReg.useDefault()
    #mc1.sReg.simpleCheck()
#     print('{0:b}'.format(mc1.sReg.getConf()))
#     mc1.sReg.test()
if __name__ == '__main__':
    mc1 = MIC4Config()
    mc1.connect()
    mc1.sendA_PULSE()
#     setPixels(mc1, [(127,0,0,1)])
#     setLastRow(mc1, mask=0,pulse_en=1)
#     time.sleep(50)
#     mc1.empty_fifo()
#     testA(mc1)
#     testPixels(mc1)
#     lvds_test(mc1)
#     test_DOUT(mc1)
#     CheckValid(mc1)
#     busySigal(mc1)
#     checkDefaultDACinChip(mc1)
#     checkSysCLKchange(mc1)
#     loopCol(mc1)
#     checkCol(mc1)
#     test_AOUT_IHEP_loop(mc1)
#     test_AOUT_loop(mc1)
#     test_AOUT(mc1)
#     mc1.sendGRST_B()
#     mc1.sendD_PULSE()
#     turnOffAllPixels(mc1)
#     test_AOUT_IHEP(mc1)
#     testRegister(mc1)
#     mc1.checkLastReg()
#     mc1.readFIFO_test()
#     mc1.checkLastReg()
#     mc1.readFD()
#     a = 0
#     while a==0:
#         a = mc1.readFIFO_test()
#         mc1.empty_fifo()
#     setupDOUT(mc1)
#     mc1.setClocks(1,6,6)
#     mc1.readFD_debug()
#     D_signal_checks(mc1)
#     check_FDout(mc1, 1)
