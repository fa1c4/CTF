from z3 import *
import hashlib


a1 = Int('a1')
a2 = Int('a2')
a3 = Int('a3')
a4 = Int('a4')
a5 = Int('a5')
a6 = Int('a6')
a7 = Int('a7')
a8 = Int('a8')
a9 = Int('a9')
a10 = Int('a10')
a11 = Int('a11')
a12 = Int('a12')
a13 = Int('a13')
a14 = Int('a14')

solver = Solver()
solver.add(a1 * 88 + a2 * 67 + a3 * 65 - a4 * 5 + a5 * 43 + a6 * 89 + a7 * 25 + a8 * 13 - a9 * 36 + a10 * 15 + a11 * 11 + a12 * 47 - a13 * 60 + a14 * 29 == 22748)
solver.add(a1 * 89 + a2 * 7 + a3 * 12 - a4 * 25 + a5 * 41 + a6 * 23 + a7 * 20 - a8 * 66 + a9 * 31 + a10 * 8 + a11 * 2 - a12 * 41 - a13 * 39 + a14 * 17 == 7258)
solver.add(a1 * 28 + a2 * 35 + a3 * 16 - a4 * 65 + a5 * 53 + a6 * 39 + a7 * 27 + a8 * 15 - a9 * 33 + a10 * 13 + a11 * 101 + a12 * 90 - a13 * 34 + a14 * 23 == 26190)
# solver.add(a1 * 23 + a2 * 34 + a3 * 35 - a4 * 59 + a5 * 49 + a6 * 81 + a7 * 25 + (a8 << 7) - a9 * 32 + a10 * 75 + a11 * 81 + a12 * 47 - a13 * 60 + a14 * 29 == 37136)
solver.add(a1 * 23 + a2 * 34 + a3 * 35 - a4 * 59 + a5 * 49 + a6 * 81 + a7 * 25 + (a8 * (2 ** 7)) - a9 * 32 + a10 * 75 + a11 * 81 + a12 * 47 - a13 * 60 + a14 * 29 == 37136)
solver.add(a1 * 22 + a2 * 27 + a3 * 35 - a4 * 45 + a5 * 47 + a6 * 49 + a7 * 29 + a8 * 18 - a9 * 26 + a10 * 35 + a11 * 41 + a12 * 40 - a13 * 61 + a14 * 28 == 17298) 
solver.add(a1 * 12 + a2 * 45 + a3 * 35 - a4 * 9 - a5 * 42 + a6 * 86 + a7 * 23 + a8 * 85 - a9 * 47 + a10 * 34 + a11 * 76 + a12 * 43 - a13 * 44 + a14 * 65 == 19875) 
solver.add(a1 * 79 + a2 * 62 + a3 * 35 - a4 * 85 + a5 * 33 + a6 * 79 + a7 * 86 + a8 * 14 - a9 * 30 + a10 * 25 + a11 * 11 + a12 * 57 - a13 * 50 - a14 * 9 == 22784) 
solver.add(a1 * 8 + a2 * 6 + a3 * 64 - a4 * 85 + a5 * 73 + a6 * 29 + a7 * 2 + a8 * 23 - a9 * 36 + a10 * 5 + a11 * 2 + a12 * 47 - a13 * 64 + a14 * 27 == 9710) 
solver.add(a1 * 67 - a2 * 68 + a3 * 68 - a4 * 51 - a5 * 43 + a6 * 81 + a7 * 22 - a8 * 12 - a9 * 38 + a10 * 75 + a11 * 41 + a12 * 27 - a13 * 52 + a14 * 31 == 13376) 
solver.add(a1 * 85 + a2 * 63 + a3 * 5 - a4 * 51 + a5 * 44 + a6 * 36 + a7 * 28 + a8 * 15 - a9 * 6 + a10 * 45 + a11 * 31 + a12 * 7 - a13 * 67 + a14 * 78 == 24065) 
solver.add(a1 * 47 + a2 * 64 + a3 * 66 - a4 * 5 + a5 * 43 + a6 * 112 + a7 * 25 + a8 * 13 - a9 * 35 + a10 * 95 + a11 * 21 + a12 * 43 - a13 * 61 + a14 * 20 == 27687) 
solver.add(a1 * 89 + a2 * 67 + a3 * 85 - a4 * 25 + a5 * 49 + a6 * 89 + a7 * 23 + a8 * 56 - a9 * 92 + a10 * 14 + a11 * 89 + a12 * 47 - a13 * 61 - a14 * 29 == 29250) 
solver.add(a1 * 95 + a2 * 34 + a3 * 62 - a4 * 9 - a5 * 43 + a6 * 83 + a7 * 25 + a8 * 12 - a9 * 36 + a10 * 16 + a11 * 51 + a12 * 47 - a13 * 60 - a14 * 24 == 15317)

if (solver.check() == sat):
    print(solver.model())
else:
    print('No Solution for the equations')

'''
[a13 = 88,
 a3 = 10,
 a4 = 7,
 a10 = 108,
 a12 = 74,
 a1 = 119,
 a7 = 28,
 a6 = 43,
 a9 = 52,
 a14 = 33,
 a5 = 104,
 a8 = 91,
 a2 = 24,
 a11 = 88]

for i in range(13):
    code.append(ord(input1[i]) ^ ord(input1[i + 1]))
'''

code = [119, 24, 10, 7, 104, 43, 28, 91, 52, 108, 88, 74, 88, 33]
checkdata = [0 for i in range(len(code))]
index = [2, 1, 0, 3, 4, 5, 6, 7, 9, 8, 10, 11, 12, 13]
flag = ''

# permutation
for i in range(len(code)):
    checkdata[i] = code[index[i]]

# xor
for i in range(len(checkdata)-2, -1, -1):
    checkdata[i] ^= checkdata[i+1]

for i in range(len(checkdata)):
    flag += chr(checkdata[i])
print(flag)

flag_md5 = hashlib.md5(flag.encode()).hexdigest()
print(f'GWHT{{{flag_md5}}}')
