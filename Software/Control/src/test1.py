#!/usr/bin/env python

from MIC4Config import MIC4Config, bitSet

def testRegister(mc1):
    mc1.sReg.useDefault()
    print('{0:b}'.format(mc1.sReg.getConf()))
    mc1.sReg.test()
    mc1.configReg()

if __name__ == '__main__':
    mc1 = MIC4Config()
    mc1.connect()
    #mc1.test()
    #print(mc1.T())
    mc1.setClocks(1,2,4)
    mc1.sendGRST_B()
    mc1.sendA_PULSE()
    mc1.sendD_PULSE()
#     bs1 = bitSet()
#     bs1.test()
    #mc1.test_DAC8568_config()
    #mc1.test_pixel_config()
    #mc1.pCfg.get_test_vector()
#    testRegister(mc1)