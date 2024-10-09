'''
<rev1.py>
1. reverse the blackjack logic, find that gamemessage is xor and decrypted by AES
2. decrypt the gamemessage, find that MZ in the binary data
3. export MZ... data as binary file

<rev2.py>
4. reverse the binary as .Net binary, find that x,y,z (array[0], array[1], array[2]) is flag related data
5. Z3 solve the included .Net binary logic to get x,y,z data (flag)


private static void Check1(ulong x, ulong y, ulong z, byte[] KeyStream)
{
    int num = -1;
    for (int i = 0; i < 320; i++)
    {
        x = (((x >> 29) ^ (x >> 28) ^ (x >> 25) ^ (x >> 23)) & 1UL) | (x << 1);
        y = (((y >> 30) ^ (y >> 27)) & 1UL) | (y << 1);
        z = (((z >> 31) ^ (z >> 30) ^ (z >> 29) ^ (z >> 28) ^ (z >> 26) ^ (z >> 24)) & 1UL) | (z << 1);
        bool flag = i % 8 == 0;
        if (flag)
        {
            num++;
        }
        KeyStream[num] = (byte)((long)((long)KeyStream[num] << 1) | (long)((ulong)((uint)(((z >> 32) & 1UL & ((x >> 30) & 1UL)) ^ ((((z >> 32) & 1UL) ^ 1UL) & ((y >> 31) & 1UL))))));
    }
}
'''

import z3


CheckStream = [101, 5, 80, 213, 163, 26, 59, 38, 19, 6,
				173, 189, 198, 166, 140, 183, 42, 247, 223, 24,
				106, 20, 145, 37, 24, 7, 22, 191, 110, 179,
				227, 5, 62, 9, 13, 17, 65, 22, 37, 5]

KeyStream = [0] * len(CheckStream)

xor_datas = [60, 100, 36, 86, 51, 251, 167, 108, 116, 245,
				207, 223, 40, 103, 34, 62, 22, 251, 227]

# Init the z3 solver
solver = z3.Solver()

# Define the variables, notice that x0, y0, z0 are variables to solve
# need to assign x, y, z to iterate the logic
x0 = z3.BitVec('x0', 64)
y0 = z3.BitVec('y0', 64)
z0 = z3.BitVec('z0', 64)
x, y, z = x0, y0, z0
num = -1
for i in range(320):
    x = (((x >> 29) ^ (x >> 28) ^ (x >> 25) ^ (x >> 23)) & 1) | (x << 1)
    y = (((y >> 30) ^ (y >> 27)) & 1) | (y << 1)
    z = (((z >> 31) ^ (z >> 30) ^ (z >> 29) ^ (z >> 28) ^ (z >> 26) ^ (z >> 24)) & 1) | (z << 1)
    
    if i % 8 == 0: 
        num += 1

    KeyStream[num] = 0xFF & ((KeyStream[num] << 1) | (((z >> 32) & 1 & ((x >> 30) & 1)) ^ ((((z >> 32) & 1) ^ 1) & ((y >> 31) & 1))))

# add the constraints
for i in range(40):        
    solver.add(KeyStream[i] == CheckStream[i])

# Check the solver
if solver.check() == z3.sat:
    model = solver.model()
    x_val = model[x0].as_long()
    y_val = model[y0].as_long()
    z_val = model[z0].as_long()
    print('x:', x_val)
    print('y:', y_val)
    print('z:', z_val)
    xyz_data = [x_val, y_val, z_val]
    bytes_data = [0] * 3 * 4
    for i in range(3):
        for j in range(4):
            bytes_data[i * 4 + j] = (xyz_data[i] >> (j * 8)) & 0xFF 
    
    for i in range(len(xor_datas)):
        xor_datas[i] ^= bytes_data[i % len(bytes_data)]

    flag = ''.join([chr(c) for c in xor_datas])
    print('flag{{{}}}'.format(flag))
    # flag{Y0u_@re_G3meM3s7er!}
else:
    print('Failed to solve the equation')
