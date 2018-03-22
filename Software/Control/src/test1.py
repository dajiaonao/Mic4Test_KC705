#!/usr/bin/env python
import sys
import time
from MIC4Config import MIC4Config, bitSet

def testRegister(mc1):
    mc1.sReg.useDefault()
    print('{0:b}'.format(mc1.sReg.getConf()))
    mc1.sReg.test()
    mc1.configReg()


def loopCol(mc1):
    for i in range(32):
        print 'Col:', i
        mc1.sReg.useDefault()
        mc1.sReg.selectCol(i)
        mc1.testReg(read=True)

        time.sleep(1)
        mc1.sendA_PULSE()
        time.sleep(2)

def testPixels(mc1):
#     mc1.setClocks(1,5,5)
#     mc1.test_DAC8568_config()
#     mc1.sReg.value = 0
# #     mc1.sReg.value = 1
#     mc1.sReg.useDefault()
#     mc1.sReg.selectCol(1)
# # 
#     mc1.sReg.show()
# #     mc1.sReg.value = mc1.sReg.value >> 1
#     mc1.testReg(read=True)

    mc1.pCfg.clk_div = 10
#     mc1.pCfg.setAll(1,0)
#     mc1.pCfg.pixels = [(127,0,0,1)]# for i in range(64)]
    mc1.pCfg.pixels = [(127,i,0,1) for i in range(64)]
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
#     mc1.setClocks(1,1,1)
#     mc1.test_DAC8568_config()
#     mc1.pCfg.clk_div = 20
#     mc1.pCfg.pixels = [(1,1,1,0),(1,1,0,1)]
#     mc1.pCfg.applyConfig()
#     mc1.pCfg.setAll(1,0)
#     sys.exit(0)

#     mc1.empty_fifo()
#     sys.exit(0)
#     mc1.sendGRST_B()
#     mc1.sendA_PULSE()
#     mc1.sendD_PULSE()
# 
    ### --- CAUTION: all channel open, for TEST ONLY
#     mc1.sReg.vChanbits.outputLevel = -1
#     mc1.sReg.value = mc1.sReg.vChanbits.setValueTo(0x3f, mc1.sReg.value)

#     mc1.sReg.selectVolDAC(1)
#     mc1.sReg.selectCurDAC(1) 
#     mc1.sReg.value = 1<<124
    mc1.sReg.value = (1<<199) +1
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
    for i,j in enumerate(reversed(bin(mc1.sReg.value)[2:])):
        if int(j)!=0: print i,j, 199-i
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
#     testA(mc1)
#     testPixels(mc1)
    loopCol(mc1)

