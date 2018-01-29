#!/usr/bin/env python
# -*- coding: utf-8 -*-

## @package sr_ctrl
# This file is used to configure TMIIa  Shift Register module.
#
# data_in is the input data of TMIIa Shift Register module,
# div is division factor of clock frequency(f_out=f_in/2^div),
# trig is start signal of configuration.

from command import *
import socket
import time

## Shift_register write and read function.
#
# @param[in] s Socket that is already open and connected to the FPGA board.
# @param[in] data_to_send 170-bit value to be sent to the external SR.
# @param[in] clk_div Clock frequency division factor: (/2**clk_div).  6-bit wide.
# @return Value stored in the external SR that is read back.
# @return valid signal shows that the value stored in external SR is read back.
def shift_register_rw(s, data_to_send, clk_div):
    div_reg = ((clk_div & 0x3f) | (1<<6)) << 200
    data_reg = data_to_send & ((1<<200)-1)

    cmd = Cmd()

    val = div_reg | data_reg
    cmdstr = ""
    for i in xrange(13):
        cmdstr += cmd.write_register(i, (val >> i*16) & 0xffff)

    cmdstr += cmd.send_pulse(0x01)

    print [hex(ord(w)) for w in cmdstr]

    s.sendall(cmdstr)

    return
    # read back
    time.sleep(1)
    cmdstr = ""
    for i in xrange(11):
        cmdstr += cmd.read_status(10-i)
    s.sendall(cmdstr)
    retw = s.recv(4*11)
    print [hex(ord(w)) for w in retw]
    ret_all = 0
    for i in xrange(11):
        ret_all = ret_all | int(ord(retw[i*4+2])) << ((10-i) * 16 + 8) | int(ord(retw[i*4+3])) << ((10-i) * 16)
    ret = ret_all & ((1<<170)-1)
    valid = (ret_all & (1 <<170)) >> 170
    print "%x" % ret
    print valid
    return ret
    return valid

def test(s):
    print("testing...")

    div = 8
    fifo_out = 1
    #dx = 0xabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcde
    dx = 0xffffffffffffffffffffffffffffffffffffffffffffffffff
    #dx = 1<<200
    dxc = dx
    print('{0:x}'.format(dxc))

    cmd = Cmd()
    cmdStr = ''
    cmdStr += cmd.write_register(1, (div<<1)+fifo_out)
    for i in range(13):
        din = 0xffff & dxc
        cmdStr += cmd.write_register(0, din)
        cmdStr += cmd.send_pulse(0x4)

        ### shift dxc
        dxc = dxc>>16
        print('{1:d} {0:x} {2:x}'.format(dxc, i, din))

    #time.sleep(2)
    ### send data to register and read them back
    #cmdStr += cmd.write_register(1, (div<<1)+fifo_out)
    cmdStr += cmd.send_pulse(0x1)
    #cmdStr += self.cmd.read_datafifo(200)

    print([ord(x) for x in cmdStr])
    print(len([ord(x) for x in cmdStr]))
    print(cmdStr)
    s.sendall(cmdStr)

def All_plse(s):
    pls = (1<<7)|(1<<6)|(1<<5)
    #pls = 1<<4
    pls = 0xffff & pls
    cmd = Cmd()
    cmdStr = ''
    cmdStr += cmd.send_pulse(pls)
    s.sendall(cmdStr)

def pixel_config(s):
    pls = 1<<2
    pls = 0xffff & pls
    data = 0xffff & 0x6
    addr = 0
    aval = [0xf0f00fff, 0xeab000af]
    cmd = Cmd()
    cmdStr =''
    cmdStr += cmd.write_register(0, data)
    cmdStr += cmd.write_memory(addr, aval)
    s.sendall(cmdStr)
    time.sleep(1)
    cmdStr = ''
    cmdStr += cmd.send_pulse(pls)
    s.sendall(cmdStr)

if __name__ == "__main__":
    host = '192.168.2.3'
    port = 1024
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((host,port))

    data_in=123456
    div=7
    All_plse(s)
    #shift_register_rw(s, data_in, div)
    #test(s)
    #pixel_config(s)

    s.close()
