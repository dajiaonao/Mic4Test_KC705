#!/usr/bin/env python

from MIC4Config import MIC4Config, bitSet

if __name__ == '__main__':
    mc1 = MIC4Config()
#     mc1.connect()
#     mc1.test()
#     bs1 = bitSet()
#     bs1.test()
    mc1.sReg.useDefault()
    mc1.sReg.simpleCheck()
#     print('{0:b}'.format(mc1.sReg.getConf()))
#     mc1.sReg.test()
