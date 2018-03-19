#!/usr/bin/env python
import sys
from MIC4Config import MIC4Config, bitSet

def testRegister(mc1):
    mc1.sReg.useDefault()
    print('{0:b}'.format(mc1.sReg.getConf()))
    mc1.sReg.test()
    mc1.configReg()

if __name__ == '__main__':
    mc1 = MIC4Config()

#     #mc1.sReg.useDefault()
#     mc1.sReg.value = 123456
# #     mc1.sReg.selectCol(23)
#     mc1.sReg.show()
#     sys.exit(0)

    mc1.connect()
    #mc1.test()
#     mc1.setClocks(1,10,10)
#     mc1.test_DAC8568_config()
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
    mc1.sReg.value = 0
#     mc1.sReg.useDefault()
#     mc1.sReg.useVolDAC(5, 0x1ff)
#     mc1.sReg.useVolDAC(4, 0x20)
#     mc1.sReg.setPar('VCASN',  0x3ff)
#     mc1.sReg.setPar('VCASN2', 0x3ff)
#     mc1.sReg.setPar('VCASP',  0x3ff)
#     mc1.sReg.setPar('VReset', 0x3ff)
#     mc1.sReg.setPar('VCLIP',  0x3ff)
#     mc1.sReg.setPar('VRef',   0x3ff)
    mc1.sReg.selectVolDAC(0)

#     mc1.sReg.useVolDAC(1, 0x3ff)
#     mc1.sReg.useVolDAC(0, 0x2ff)
#     mc1.sReg.setPar('VRef', 0x2ff)
#     mc1.sReg.setPar('VCASN2', 0x3ff)
#     mc1.sReg.selectVolDAC(5)
#     mc1.sReg.useAllZero()


    ## reverse
#     test_valueBit  = bitSet([i for i in range(200)],True)
#     mc1.sReg.value = test_valueBit.setValueTo(mc1.sReg.value, mc1.sReg.value)

#     print bin(mc1.sReg.value)
#     for i,j in enumerate(reversed(bin(mc1.sReg.value)[2:])):
#         if int(j)!=0: print i,j, 199-i
    mc1.sReg.show()
    mc1.sReg.value = mc1.sReg.value >> 1
    mc1.testReg(read=True)
    #x = mc1.shift_register_rw(0xabcdeabcdeabcdeabcde, 8)
    #print(x)
    #sys.exit(0)

    
    #print(mc1.T())
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
