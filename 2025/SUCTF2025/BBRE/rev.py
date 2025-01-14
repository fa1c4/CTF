'''
reverse:
1. input 19 chars at main and processed by function2 (->function5 ->function3 ->function4) 
and then call function0 to copy the src(input) to dest
2. function0 copy 19 chars to 0xC(12) chars buffer (dest = byte ptr -0Ch) will hijack the return address to target function
here is function1 (check logic) with "congratulate" string, the address of func1 is 0x0040223D (19 - 12 - 4 == 3)
so only take least 3 bytes address here is 0x40223D
3. now only function2 logic remains to reverse, function3 and function4 logic is like generating permutation table and xor the input
just guess some crypto algorithms here, try with RC4 with key 'suctf' ... and get the readable result, so the first 16 bytes obtained
4. the 17 to 19 bytes is 0x40223D convert to chars
5. final bytes is just at function1 logic, directly reversing is enough
'''
from arc4 import ARC4


flag = ''

# stage 1 
key = b'suctf'
rc4 = ARC4(key)

encrypted = [0x65575A2F, 0x0CD698F14, 0x551A2993, 0x5EE44018]
encrypted = b''.join(e.to_bytes(4, 'little') for e in encrypted)
# print(encrypted)
# for char in encrypted:
#     print(hex(char)[2:], end=' ')
decrypted = rc4.decrypt(encrypted).decode()
# print(decrypted)
flag += decrypted

# stage 2
flag += chr(0x3D) + chr(0x22) + chr(0x40)

# stage 3
tmp = ''
keys = [0x41, 0x6D, 0x62, 0x4D, 0x53, 0x49, 0x4E, 0x29, 0x28]

for i in range(len(keys)):
    tmp += chr(keys[i] + i)

# print(tmp)
# AndPWNT0
flag += tmp

print(f'SUCTF{{{flag}}}')
