# template-v2.0 for exploit scripts by fa1c4
# usage: python exp.py [REMOTE|GDB|NULL]
'''
binary information ...
exploitation path ...
'''
from pwn import *


# define the context
binary_name = './challenge'
libc_name = './libc.so.6' if args.REMOTE \
        else ''
elf = ELF(binary_name, checksec=True) if binary_name else None
libc = ELF(libc_name, checksec=False) if libc_name else None
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

# define the io object
if args.REMOTE:
    io = remote('challenge.ctf.games', 30269)
elif args.GDB:
    io = gdb.debug(binary_name, gdbscript="""
        brva 0x2333
        c
    """, aslr=False)
else:
    io = process(binary_name)


# exploiting code
pass

# interact with the shell
io.interactive()
