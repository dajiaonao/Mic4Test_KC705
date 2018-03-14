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

    #mc1.sReg.useDefault()
    mc1.sReg.value = 123456
#     mc1.sReg.selectCol(23)
    mc1.sReg.show()
    sys.exit(0)

    mc1.connect()
    #mc1.test()
    mc1.setClocks(1,10,10)
#    mc1.test_DAC8568_config()
#     mc1.sendGRST_B()
#     mc1.sendA_PULSE()
#     mc1.sendD_PULSE()
# 
#     mc1.sReg.useDefault()
#     mc1.sReg.selectVolDAC(0) 
#     mc1.sReg.selectCurDAC(1) 
#     mc1.testReg()
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
