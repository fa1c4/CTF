'''
main logic is in .init.function which uses pown (RSA) algorithm to encrypt flag
flag encrypted data is at .data addr: 0x0000564C3A802020
'''

from Crypto.Util.number import inverse

e = 23531
n = 2343464867 # 2343464867 = 42821 * 54727
p = 42821
q = 54727
phi = (p - 1) * (q - 1)
d = inverse(e, phi)

table = [
    440402232, 664451175, 394078569, 242108149, 1361453560, 
    781635187, 75805846, 1933660014, 75805846, 29521129, 
    75805846, 1669187426, 353663562, 535398750, 535398750, 
    -2044001813, 2002388685, 242108149, 242108149, 1047143526, 
    50375533, 1516751890, 873889281, -2044001813, 50375533, 
    75805846, -2044001813, 50375533, 300931661, 1361453560, 
    242108149, 394078569, 781635187, 353663562, 1516751890, 
    781635187, 2021659725, 1516891499
]

flag = b''
for i in range(len(table)):
    flag += bytes([pow(table[i] & 0xFFFFFFFF, d, n)])

print(flag.decode())