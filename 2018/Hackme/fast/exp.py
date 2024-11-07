'''
calculation program
'''

from pwn import *
from numpy import int32


url, port = "node5.buuoj.cn", 25556
# filename = "2018_neko"
# elf = ELF(filename)
context(arch="amd64", os="linux", log_level="debug")
# context(arch="i386", os="linux")

io = remote(url, port)

i32 = lambda x: int32(int(x))

def pwn():
    io.sendlineafter(b'the game.\n', b'Yes I know')
    ans = b''
    res = b''
    for i in range(10000):
        n1, op, n2 = io.recvuntil(b'=', drop=True).strip().split(b' ')
        io.recvline()
        if op == b'+':
            ans = str(i32(n1) + i32(n2)).encode()
        elif op == b'-':
            ans = str(i32(n1) - i32(n2)).encode()
        elif op == b'*':
            ans = str(i32(n1) * i32(n2)).encode()
        else:
            ans = str(int(float(n1) / int(n2))).encode()
        
        res += (ans + b' ')

    io.sendline(res)


if __name__ == "__main__":
    pwn()
    io.interactive()
