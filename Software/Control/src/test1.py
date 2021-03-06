#!/usr/bin/env python
import sys
import time
from MIC4Config import MIC4Config, bitSet
import socket


def checkDout(mc1):
    mc1.sReg.useDefault() 
    mc1.sReg.selectCol(0)
    mc1.sReg.setTEST(1)
    mc1.sReg.show()
    mc1.testReg(read=True)


def check_FDout(mc1, iTest=10):
#     setAllPixels(mc1, mask=1, pulse_en=0)
#     setAllPixels(mc1, mask=1, pulse_en=0)
#     setPixels(mc1,[(127,0,0,1),(127,1,0,1),(127,3,0,1),(127,3,0,1)])
#     sys.exit(0)

    mc1.setClocks(0,6,6)
    mc1.test_DAC8568_config()
    mc1.sReg.useDefault() 
    mc1.sReg.selectCol(0)
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

def testAutoMask(mc1):
    #mc1.maskedPixels.add((126,10))
    en_list = [(r,c) for r in range(24,32) for c in range(32)]
    mc1.maskedPixels.update([(r,c) for r in range(128) for c in range(64) if (r,c) not in en_list])
    print mc1.checkPixels()

#    print '*'*20,"MASK 1","*"*20
#    mc1.checkMasked(nTry=1)
#     print '*'*20,"MASK 2","*"*20
#     l2 = mc1.autoMaskNoisyPixels()
#     print "Masked:", l2
    #mc1.maskedPixels.add((31, 7))
    #r = mc1.checkMasked()
    #print r

def D_signal_checks(mc1):
    mc1.sendGRST_B()
#     mc1.setClocks(0,6,6)
#     mc1.sendD_PULSE()

def testRegister(mc1):
    mc1.test_DAC8568_config()
    mc1.setClocks(0,6,6)
    mc1.sReg.value = 0
#     mc1.sReg.value =0b100101
#    mc1.sReg.useDefault() 

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
#     mc1.sReg.setLVDS_TEST(0b1000)
    mc1.sReg.setTRX16(0b1000)
#     mc1.sReg.setTRX15_serializer(0b1000)
    mc1.sReg.show()
#     mc1.testReg(read=True)
    mc1.testReg(read=False)
#     mc1.setClocks(1,0,0)

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
    #mc1.setClocks(0,0,0)
#     sys.exit(1)
    mc1.test_DAC8568_config()

    mc1.setVhVl(1,0.7)

# # #     mc1.sReg.useDefault()
    mc1.sReg.value =  0
    mc1.sReg.setPDB(0)
#IHEP Col62-0
#    mc1.sReg.setPar('VCLIP' ,0.1,  0.833, 0b1001011001)
#    mc1.sReg.setPar('VCASN' ,0.325,  0.384, 0b100011110)
#    mc1.sReg.setPar('VCASP' ,0.37,  0.603, 0b110110000)
#    mc1.sReg.setPar('VReset',1.1,  1.084, 0b1100000111)
#    mc1.sReg.setPar('VCASN2',0.5,  0.502, 0b101100110)
#    mc1.sReg.setPar('VRef'  ,0.4,  0.406, 0b100011111)
#    mc1.sReg.setPar('IBIAS' ,0xc9)
#    mc1.sReg.setPar('IDB'   ,0x80)
#    mc1.sReg.setPar('ITHR'  ,0x80)
#    mc1.sReg.setPar('IRESET',0x80)
#    mc1.sReg.setPar('IDB2'  ,0x80)
#     mc1.sReg.selectCol(62)
#IHEP-1
#     mc1.sReg.setPar('VCLIP' ,0  , 0.689, 0x200)
#     mc1.sReg.setPar('VReset',1.1, 0.703, 0x200)
#     mc1.sReg.setPar('VCASN2',0.5, 0.693, 0x200)
#     mc1.sReg.setPar('VCASN' ,0.49, 0.697, 0x200)
#     mc1.sReg.setPar('VCASP' ,0.37, 0.692, 0x200)
#     mc1.sReg.setPar('VRef'  ,1.4, 0.701, 0x200) ## curDAC reference vol, default value 0.4 V
#     mc1.sReg.setPar('IBIAS' ,0x60) ## Chip 5: 0xff->0.594 V
#     mc1.sReg.setPar('IDB'   ,0xf0)
#     mc1.sReg.setPar('ITHR'  ,0x7f)
#     mc1.sReg.setPar('IRESET',0xff)
#     mc1.sReg.setPar('IDB2'  ,0xc0)
#     mc1.sReg.selectCol(62)
#IHEP-2 
#    mc1.sReg.setPar('VCLIP' ,0.1,  0.833, 0b1001011001)
#    mc1.sReg.setPar('VCASN' ,0.325,  0.384, 0b100011110)
#    mc1.sReg.setPar('VCASP' ,0.37,  0.603, 0b110110000)
#    mc1.sReg.setPar('VReset',1.1,  1.084, 0b1100000111)
#    mc1.sReg.setPar('VCASN2',0.5,  0.502, 0b101100110)
#    mc1.sReg.setPar('VRef'  ,0.8,  0.406, 0b100011111)
#    mc1.sReg.setPar('IBIAS' ,0xc9)
#    mc1.sReg.setPar('IDB'   ,0x40)
#    mc1.sReg.setPar('ITHR'  ,0x10)
#    mc1.sReg.setPar('IRESET',0xff)
#    mc1.sReg.setPar('IDB2'  ,0x80)

#IHEP-chip#7
#    mc1.sReg.setPar('VCLIP' ,0.1,  1.423, 0x3ff)
#    mc1.sReg.setPar('VCASN' ,0.4,  1.419, 0x3ff)  #VCASN: 394mV
#    mc1.sReg.setPar('VCASP' ,0.37, 1.422, 0x3ff)  #VCASP: 367.6mV
#    mc1.sReg.setPar('VReset',1.1,  1.43, 0x3ff)   
#    mc1.sReg.setPar('VCASN2',0.5,  1.416, 0x3ff)
#    mc1.sReg.setPar('VRef'  ,0.4,  1.424, 0x3ff)  #VREF_Current_DAC:397.8mV
#    mc1.sReg.setPar('IBIAS' ,0xc9) #IBIAS_IHEP_40n:325.6mV
#    mc1.sReg.setPar('IDB'   ,0x30) #IDB:41.4mV
#    mc1.sReg.setPar('ITHR'  ,0x10) #IHEP_IFOL_2n:10mV
#    mc1.sReg.setPar('IRESET',0xff) #IHEP_IRESET_40p:3.3mV
#    mc1.sReg.setPar('IDB2'  ,0x80) #IHEP_IDB2:129.8mV

#IHEP-SIM-chip#7
#    mc1.sReg.setPar('VCLIP' ,0.1,  1.423, 0x3ff)
#    mc1.sReg.setPar('VCASN' ,0.4, 1.419, 0x3ff)
#    mc1.sReg.setPar('VCASP' ,0.37, 1.422, 0x3ff)
#    mc1.sReg.setPar('VReset',1.1,  1.43, 0x3ff)
#    mc1.sReg.setPar('VCASN2',0.5,  1.416, 0x3ff)
#    mc1.sReg.setPar('VRef'  ,0.4,  1.424, 0x3ff) 
#    mc1.sReg.setPar('IBIAS' ,0xc9)
#    mc1.sReg.setPar('IDB'   ,0x90) #IDB:87.2mV
#    mc1.sReg.setPar('ITHR'  ,0x10)
#    mc1.sReg.setPar('IRESET',0x80)
#    mc1.sReg.setPar('IDB2'  ,0xff) #IHEP_IDB2:216.6mV

    mc1.sReg.selectCol(12)
    mc1.sReg.selectVolDAC(4)
    mc1.sReg.selectCurDAC(3)



# PLAC 
    mc1.sReg.setPar('VCLIP' ,0. , 0.689, 0x200)

    mc1.sReg.setPar('VReset',1.2, 0.703, 0x200)
    mc1.sReg.setPar('VCASN2',0.5, 0.693, 0x200)
    mc1.sReg.setPar('VCASN' ,0.4, 0.689, 0x200)
    mc1.sReg.setPar('VCASP' ,0.6, 0.694, 0x200)
    mc1.sReg.setPar('VRef'  ,0.4, 0.701, 0x200)
    mc1.sReg.setPar('IBIAS' ,0xff) ## Chip 5: 0xff->0.594 V

    mc1.sReg.setPar('IDB'   ,0xf0)
    mc1.sReg.setPar('ITHR'  ,0x8f)

    mc1.sReg.setPar('IRESET',0x80)
    mc1.sReg.setPar('IDB2'  ,0x80)



#     mc1.sReg.setPar('VCLIP' ,0,  0.833, 0b1001011001)
#     mc1.sReg.setPar('VCASN' ,0.4,  0.384, 0b100011110)
#     mc1.sReg.setPar('VCASP' ,0.5,  0.603, 0b110110000)
#     mc1.sReg.setPar('VReset',1.2,  1.084, 0b1100000111)
#     mc1.sReg.setPar('VCASN2',0.5,  0.502, 0b101100110)
#     mc1.sReg.setPar('VRef'  ,0.4,  0.406, 0b100011111)
#     mc1.sReg.setPar('IBIAS' ,0xc9)
#     mc1.sReg.setPar('IDB'   ,0x80)
#     mc1.sReg.setPar('ITHR'  ,0x80)
#     mc1.sReg.setPar('IRESET',0x80)
#     mc1.sReg.setPar('IDB2'  ,0x80)


# SUB=-3V Chip #5 bias1
#    mc1.sReg.setPar('VCLIP' ,0.37,  0.833, 0b1001011001)
#    mc1.sReg.setPar('VCASN' ,0.76,  0.384, 0b100011110)
#    mc1.sReg.setPar('VCASP' ,0.6,  0.603, 0b110110000)
#    mc1.sReg.setPar('VReset',1.43,  1.084, 0b1100000111)
#    mc1.sReg.setPar('VCASN2',0.8,  0.502, 0b101100110)
#    mc1.sReg.setPar('VRef'  ,0.4,  0.406, 0b100011111)
#    mc1.sReg.setPar('IBIAS' ,0xff)
#    mc1.sReg.setPar('IDB'   ,0x80)
#    mc1.sReg.setPar('ITHR'  ,0x80)
#    mc1.sReg.setPar('IRESET',0x80)
#    mc1.sReg.setPar('IDB2'  ,0x80)



# SUB=-3V Chip #5 bias2
#    mc1.sReg.setPar('VCLIP' ,0.47, 0.833, 0b1001011001)
#    mc1.sReg.setPar('VCASN' ,0.9,  0.384, 0b100011110)
#    mc1.sReg.setPar('VCASP' ,0.6,  0.603, 0b110110000)
#    mc1.sReg.setPar('VReset',1.43, 1.084, 0b1100000111)
#    mc1.sReg.setPar('VCASN2',0.9,  0.502, 0b101100110)
#    mc1.sReg.setPar('VRef'  ,0.4,  0.406, 0b100011111)
#    mc1.sReg.setPar('IBIAS' ,0xff)
#    mc1.sReg.setPar('IDB'   ,0x80)##(chip#5,0x80->72mV, 0x90->77.6mV, 0xc0->93.6mV, 0xe0->103.8mV, 0xff->112.9mV)
#    mc1.sReg.setPar('ITHR'  ,0x80)
#    mc1.sReg.setPar('IRESET',0x80)
#    mc1.sReg.setPar('IDB2'  ,0x80)


# SUB=-4V Chip #5 bias1
#     mc1.sReg.setPar('VCLIP' ,0.47, 0.833, 0b1001011001)
#     mc1.sReg.setPar('VCASN' ,1,  0.384, 0b100011110)
#     mc1.sReg.setPar('VCASP' ,0.6,  0.603, 0b110110000)
# #    mc1.sReg.setPar('VReset', 0x3ff)##(chip#5, 0x3ff->1.389V)
#     mc1.sReg.setPar('VReset',1.389, 1.389, 0x3ff)
#     mc1.sReg.setPar('VCASN2',1.1,  0.502, 0b101100110)
#     mc1.sReg.setPar('VRef'  ,0.4,  0.406, 0b100011111)
#     mc1.sReg.setPar('IBIAS' ,0xff)
#     mc1.sReg.setPar('IDB'   ,0xe0) 
#     mc1.sReg.setPar('ITHR'  ,0x80)
#     mc1.sReg.setPar('IRESET',0x80)
#     mc1.sReg.setPar('IDB2'  ,0x80)




# SUB=-5V Chip #5 not find a working point
#    mc1.sReg.setPar('VCLIP' ,0.5,  0.833, 0b1001011001)
#    mc1.sReg.setPar('VCASN' ,0.6,  0.384, 0b100011110)
#    mc1.sReg.setPar('VCASP' ,0.7,  0.603, 0b110110000)
#    mc1.sReg.setPar('VReset',1.43,  1.084, 0b1100000111)
#    mc1.sReg.setPar('VCASN2',1,    0.502, 0b101100110)
#    mc1.sReg.setPar('VRef'  ,0.4,  0.406, 0b100011111)
#    mc1.sReg.setPar('IBIAS' ,0xff)
#    mc1.sReg.setPar('IDB'   ,0x80)
#    mc1.sReg.setPar('ITHR'  ,0x80)
#    mc1.sReg.setPar('IRESET',0x80)
#    mc1.sReg.setPar('IDB2'  ,0x80)











    mc1.sReg.setLVDS_TEST(0b1100)
    mc1.sReg.setTRX16(0b1000)
    mc1.sReg.setTRX15_serializer(0b1100)
   # mc1.sReg.setTEST(1)


    mc1.sReg.show()
    mc1.testReg(read=True)
# #     mc1.setClocks(1,6,6)

    time.sleep(2)
    mc1.sendA_PULSE()




def check_DOUT(mc1):
    mc1.setClocks(0,1,3)

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

def setPixelsInSuperblock(mc1, row, col, pulse_en=1, mask=0):
    if row>15 or col>7:
        print "Invalid row (>15) or col(>7):", row, col
        print 'aborting...'
        return
    mc1.setClocks(0,6,6) # from 250 MHz clock
    mc1.test_DAC8568_config()
    mc1.pCfg.clk_div = 16 # from 100 MHz clock
    mc1.pCfg.pixels = [(row*8+i, col*8+j, mask, pulse_en) for i in range(8) for j in range(8)]
    print mc1.pCfg.pixels
#     mc1.pCfg.applyConfig()



# def setPixels(mc1,pxiels):
#     mc1.setClocks(0,6,6) # from 250 MHz clock
#     mc1.test_DAC8568_config()
#     mc1.pCfg.clk_div = 16 # from 100 MHz clock
#     mc1.pCfg.pixels = pxiels
#     mc1.pCfg.applyConfig()
# 
# def setAllPixels(mc1,pulse_en=0, mask=0):
#     mc1.setClocks(0,6,6) # from 250 MHz clock
#     mc1.test_DAC8568_config()
#     mc1.pCfg.clk_div = 16 # from 100 MHz clock
#     for r in range(128):
#         print "turning off row", r
#         mc1.pCfg.pixels = [(r,i,mask,pulse_en) for i in range(64)]
#         mc1.pCfg.applyConfig()
# 
# def setPixelsInRow(mc1, row, pulse_en=1, mask=0):
#     mc1.setClocks(0,6,6) # from 250 MHz clock
#     mc1.test_DAC8568_config()
#     mc1.pCfg.clk_div = 16 # from 100 MHz clock
#     mc1.pCfg.pixels = [(row,i,mask,pulse_en) for i in range(64)]
#     mc1.pCfg.applyConfig()
# 
# def setLastRow(mc1, pulse_en=1, mask=0):
#     mc1.setClocks(0,6,6) # from 250 MHz clock
#     mc1.test_DAC8568_config()
#     mc1.pCfg.clk_div = 16 # from 100 MHz clock
#     mc1.pCfg.pixels = [(127,i,mask,pulse_en) for i in range(64)]
#     mc1.pCfg.applyConfig()

def busySigal(mc1):
    mc1.setClocks(0,6,6) # from 250 MHz clock
    mc1.test_DAC8568_config()
    mc1.pCfg.clk_div = 16 # from 100 MHz clock
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

def runFD_check(mc1):
    mc1.s.settimeout(0.1)
    mc1.setVhVl(1.0,0.7)
    with open('test_here.dat','w') as fout1:
        for i in range(100):
            mc1.sendA_PULSE()
            fd = 0
            try:
                l1 = mc1.getFDAddresses()
                if l1:
                    fd = l1.index((127,12)) >= 0 and 1 or 0
                    if len(l1)>1: print "more than 1 addresses"
            except socket.timeout as e:
                print "caught the exception:", e
            print i, fd
            fout1.write('{0:d} {1:d}'.format(i, fd))
def testChip(mc1):
#     mc1.setClocks(1,6,6)
#    mc1.sendD_PULSE()
#    mc1.sendA_PULSE()
#    mc1.sendGRST_B()
    mc1.setPixels([(120,30,0,1)])
    mc1.test_DAC8568_config()
#     mc1.sendD

if __name__ == '__main__':
    mc1 = MIC4Config()
#     mc1.host = '192.168.2.1'
    mc1.connect()
#     mc1.resetChip()
#     mc1.setClocks(0,0,0)
#     mc1.setOptions(1,1,strobe_b=0, strobe_opt=1, data_opt=1)
#    mc1.test_DAC8568_config()
#     mc1.setup()
#     mc1.setVhVl(1.5,0.7)

#    mc1.clk_div = 7
#    mc1.setup()
#    testAutoMask(mc1)

#    testChip(mc1)
#    mc1.setPixels([(0,0,0,1),(127,3,0,1)])
#    mc1.setPixels([(127,9,1,0),(127,3,0,1)])

#    mc1.setPixels([(127,12,0,1)])
#    mc1.setPixels([(7,0,1,0),(8,0,0,1)])
#     test_AOUT(mc1)
#     sys.exit()

#    mc1.setPixelsInRow(127, mask=0, pulse_en=1)
#    mc1.setPixels([(127,i,0,1) for i in range(32,64)])



#    mc1.test_DAC8568_config()
#    mc1.clk_div = 6
#    mc1.setup()
#    checkDout(mc1)
#     mc1.setPixelsInRow(127, mask=0, pulse_en=0)

#     for i in range(121):
#         mc1.setPixelsInRow(i, mask=0, pulse_en=0)
#         time.sleep(0.5)
#         print mc1.getFDAddresses(50)

#     mc1.setPixels([(i+32*k,j,0,1) for i in range(7) for j in range(32) for k in range(4)])


#    mc1.setPixels([(i+120,j,1,0) for i in range(7) for j in range(32,64)])

#    mc1.setPixels([(127,12,0,1)])


#    mc1.setPixels([(120+i,j,1,0) for i in range(8) for j in range(32)])

#    mc1.setPixels([(80+i,j,1,0) for i in range(8) for j in range(32)])
#    mc1.setPixels([(88+i,j,0,1) for i in range(8) for j in range(32)])

#    mc1.resetChip()
#    mc1.setPixels([(88,14,0,1)])
#    mc1.setPixels([(31,7,1,0)])
#    mc1.setPixels([(16,29,1,0)])
#    mc1.setPixels([(17,22,1,0)])
#    mc1.setPixels([(23,15,1,0)])
#    mc1.setPixels([(17,6,1,0)])
#    mc1.setPixels([(17,23,1,0)])
#    mc1.setPixels([(16,17,1,0)])
#    mc1.setPixels([(16,5,1,0)])
#    mc1.setPixels([(16,2,1,0)])
#     time.sleep(0.5)

#    mc1.setPixels([(17,3,0,1),(35,1,0,1),(70,7,0,1)])

#    mc1.setPixels([(2,2,1,0),(8,0,1,0),(16,3,0,1),(20,4,1,0),(33,1,0,1),(48,2,1,0),(64,7,0,1),(88,6,1,0),(112,5,0,1)])
#    mc1.setPixels([(127,0,0,1),(127,31,0,1)])

#     mc1.setPixels([(15, 10,1,0)])

#    mc1.setPixels([(120,52,1,0),(123,35,1,0)])
 #   mc1.setPixels([(120,8,1,0),(127,12,0,1)])
#    mc1.setPixels([(123, 52,1,0)])

#     mc1.setPixels([(8*i+i,i,1,1) for i in range(8)])


#     mc1.setPixels([(7,8,0,1)])
#     mc1.setPixels([(8,0,1,0),(8,1,0,1)])
#     mc1.setPixels([(8,1,1,1)])

#    setPixels(mc1, [(127,i,0,1) for i in range(32)])
#    test_AOUT(mc1)
# # #    setPixels(mc1, [(127,62,1,0),(127,12,0,1)])

#     setPixels(mc1, [(127,i,0,1) for i in range(32)])
#    mc1.setPixels([(127,62,0,1)])
#    test_AOUT(mc1)
#    time.sleep(2)
#    mc1.sendA_PULSE()
#     mc1.sendD_PULSE()
#    setPixels(mc1, [(127,62,1,0),(127,12,0,1)])

#    mc1.sendGRST_B()
#     mc1.setAllPixels(mask=1, pulse_en=0)
#     sys.exit(0)
#    mc1.setClocks(0,6,6)
    for i in range(4):
        mc1.setPixelsInSuperblock(15,i,mask=0, pulse_en=1)
#     mc1.setPixelsInSuperblock(0,0,mask=1, pulse_en=1)
#     mc1.setPixelsInSuperblock(1,0,mask=0, pulse_en=1)
#     mc1.setPixelsInSuperblock(1,0,mask=1, pulse_en=0)
#     mc1.setPixelsInSuperblock(1,1,mask=0, pulse_en=1)
#     mc1.setPixelsInSuperblock(1,2,mask=0, pulse_en=1)
#     mc1.setPixelsInSuperblock(0,1,mask=0, pulse_en=1)
#     mc1.setPixelsInSuperblock(1,1,mask=0, pulse_en=1)
#     mc1.setPixelsInSuperblock(0,2,mask=1, pulse_en=0)
#     mc1.setPixelsInSuperblock(1,1,mask=1, pulse_en=0)
#     mc1.setPixelsInSuperblock(1,0,mask=1, pulse_en=0)
#     mc1.setPixelsInSuperblock(1,2,mask=1, pulse_en=0)
#     mc1.setPixelsInSuperblock(1,0,mask=1, pulse_en=0)
#     mc1.setPixelsInSuperblock(2,0,mask=1, pulse_en=0)
#     mc1.setPixelsInSuperblock(3,0,mask=1, pulse_en=0)
#     mc1.setPixelsInSuperblock(6,5,mask=1, pulse_en=0)
#     mc1.setPixelsInSuperblock(5,5,mask=1, pulse_en=0)
#     mc1.setPixelsInSuperblock(4,5,mask=1, pulse_en=0)
#     mc1.setPixelsInSuperblock(3,5,mask=1, pulse_en=0)
#     mc1.setPixelsInSuperblock(6,4,mask=1, pulse_en=0)
#     mc1.setPixelsInSuperblock(5,4,mask=1, pulse_en=0)
#     mc1.setPixelsInSuperblock(4,4,mask=1, pulse_en=0)
#     mc1.setPixelsInSuperblock(3,4,mask=1, pulse_en=0)
#     mc1.setPixelsInSuperblock(6,6,mask=1, pulse_en=0)
#     mc1.setPixelsInSuperblock(5,6,mask=1, pulse_en=0)
#     mc1.setPixelsInSuperblock(4,6,mask=1, pulse_en=0)
#     mc1.setPixelsInSuperblock(3,6,mask=1, pulse_en=0)
#     time.sleep(5)

#     mc1.start_take_data(dataFileName='data_May15_noise_allPixels.dat')

#    for i in range(100):
#        mc1.sendD_PULSE()
#        print mc1.getFDAddresses(100,True)
#    mc1.sendGRST_B()
#    l1 = mc1.getFDAddresses(100,True)
#    print l1

#     print mc1.getFDAddresses(100,True)

#     mc1.sendGRST_B()
#     l1 = mc1.getFDAddresses(100,True)
#     print l1

#     mc1.wait()
#     time.sleep(20)
#     mc1.quit()
#     mc1.setPixelsInRow(126, mask=0, pulse_en=0)
#    mc1.sendA_PULSE()

#    mc1.sendD_PULSE()
#    mc1.readFD(readOnly=True)
#    l1=mc1.getFDAddresses(100,True)
#    print l1

#    l2 = [(16+i,j) for i in range(8) for j in range(32)]
#    l3 = [(16,26),(17,31),(16,29),(17,22),(23,15),(17,6),(17,23),(16,17),(16,5),(16,2)]
#    for px in l2:
#        if px in l1: continue
#        if px in l3: continue
#        print px
    
#    setAllPixels(mc1, mask=0, pulse_en=1)
#     sys.exit()
#     setLastRow(mc1, mask=0,pulse_en=1)
#     time.sleep(50)
#     mc1.empty_fifo()
#     testA(mc1)
#     test_AOUT(mc1)
#     testPixels(mc1)
#    lvds_test(mc1)
#     test_DOUT(mc1)
#     CheckValid(mc1)
#     busySigal(mc1)
#     checkDefaultDACinChip(mc1)
#     checkSysCLKchange(mc1)
#     loopCol(mc1)
#     checkCol(mc1)
#     test_AOUT_IHEP_loop(mc1)
#     test_AOUT_loop(mc1)

#     check_DOUT(mc1)
#     mc1.setClocks(0,6,6)
#     mc1.setClocks(1,6,6)
#     mc1.setClocks(0,6,6)
#     mc1.setClocks(1,6,6)
#     mc1.setClocks(0,6,6)
#     mc1.testStrobe(6,6)
#     mc1.setClocks(1,6,6)
#     mc1.setClocks(0,6,6)
#     mc1.setClocks(1,6,6)
#     testRegister(mc1)
#100    mc1.readFD_debug()
   # mc1.readFD()
#     mc1.readFD()

#     runFD_check(mc1)
# 
#     mc1.s.settimeout(0.2)
#    try:
#        l1 = mc1.getFDAddresses()
#        if l1:
#            print l1
#            print l1.index((127,12))
#     mc1.readFD(readOnly=True)
#     except socket.timeout as e:
#         print "caught the exception:", e
#     mc1.readFD(readOnly=False)
 
#     mc1.empty_fifo(500)
#     mc1.sendd_pulse()
#    sys.exit(0)
#    while True:
#      try:
#          time.sleep(1)
#           mc1.sendD_PULSE()
#          mc1.sendA_PULSE()
#      except KeyboardInterrupt:
#           break
#    turnOffAllPixels(mc1)

#     test_AOUT_IHEP(mc1)
#     mc1.checkLastReg()
#     mc1.readFIFO_test()
#     mc1.checkLastReg()
#     mc1.readFD()
#    a = 0
#    while a==0:
#        a = mc1.readFIFO_test()
#     mc1.empty_fifo(2000)
#    setupDOUT(mc1)
#     mc1.setClocks(1,10,10)
#     D_signal_checks(mc1)
#     check_FDout(mc1, 0)
