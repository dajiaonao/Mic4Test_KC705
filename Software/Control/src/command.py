from __future__ import print_function
from ctypes import *
import os

class Cmd(object):
    soname = os.path.dirname(os.path.realpath(__file__))+"/build/command.so"
    nmax = 20000

    def __init__(self):
        self.cmdGen = cdll.LoadLibrary(self.soname)
        self.buf = create_string_buffer(self.nmax)

    def send_pulse(self, mask):
        cfun = self.cmdGen.cmd_send_pulse
        buf = addressof(self.buf)
        n = cfun(byref(c_void_p(buf)), c_uint(mask))
        return self.buf.raw[0:n]

    def read_status(self, addr):
        cfun = self.cmdGen.cmd_read_status
        buf = addressof(self.buf)
        n = cfun(byref(c_void_p(buf)), c_uint(addr))
        return self.buf.raw[0:n]

    def write_memory(self, addr, aval):
        cfun = self.cmdGen.cmd_write_memory
        buf = addressof(self.buf)
        nval = len(aval)
        n = cfun(byref(c_void_p(buf)), c_uint(addr), (c_uint32 * nval)(*aval), c_size_t(nval))
        return self.buf.raw[0:n]

    def read_memory(self, addr, val):
        cfun = self.cmdGen.cmd_read_memory
        buf = addressof(self.buf)
        n = cfun(byref(c_void_p(buf)), c_uint(addr), c_uint(val))
        return self.buf.raw[0:n]

    def write_register(self, addr, val):
        cfun = self.cmdGen.cmd_write_register
        buf = addressof(self.buf)
        n = cfun(byref(c_void_p(buf)), c_uint(addr), c_uint(val))
        return self.buf.raw[0:n]

    def read_register(self, addr):
        cfun = self.cmdGen.cmd_read_register
        buf = addressof(self.buf)
        n = cfun(byref(c_void_p(buf)), c_uint(addr))
        return self.buf.raw[0:n]

    def read_datafifo(self, val):
        cfun = self.cmdGen.cmd_read_datafifo
        buf = addressof(self.buf)
        n = cfun(byref(c_void_p(buf)), c_uint(val))
        return self.buf.raw[0:n]

    def write_memory_file(self, file_name):
        cfun = self.cmdGen.cmd_write_memory_file
        buf = addressof(self.buf)
        n = cfun(byref(c_void_p(buf)), c_char_p(file_name))
        return self.buf.raw[0:n]

if __name__ == "__main__":
    cmd = Cmd()
    ret = cmd.write_register(1, 0x5a5a)
    print([hex(ord(s)) for s in ret])

