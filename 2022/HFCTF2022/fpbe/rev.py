from z3 import *


# Define Z3 variables for x0, x1, x2, and x3
x0 = Int('x0')
x1 = Int('x1')
x2 = Int('x2')
x3 = Int('x3')

# Create a Z3 solver instance
solver = Solver()

# Define the equations
solver.add(x2 * 0xFB88 + x3 * 0x6DC0 + x1 * 0x71FB + x0 * 0xCC8E == 0xBE18A1735995)
solver.add(x3 * 0xF1BF + x2 * 0x6AE5 + x1 * 0xADD3 + x0 * 0x9284 == 0xA556E5540340)
solver.add(x3 * 0xDD85 + x2 * 0x8028 + x1 * 0x652D + x0 * 0xE712 == 0xA6F374484DA3)
solver.add(x3 * 0x822C + x2 * 0xCA43 + x1 * 0x7C8E + x0 * 0xF23A == 0xB99C485A7277)

# Check if the system is satisfiable
if solver.check() == sat:
    model = solver.model()
    print("x0 =", model[x0])
    print("x1 =", model[x1])
    print("x2 =", model[x2])
    print("x3 =", model[x3])
    x0_str = model[x0].as_long().to_bytes(4, 'little').decode()
    x1_str = model[x1].as_long().to_bytes(4, 'little').decode()
    x2_str = model[x2].as_long().to_bytes(4, 'little').decode()
    x3_str = model[x3].as_long().to_bytes(4, 'little').decode()
    # flag_content = x0_str + x1_str + x2_str + x3_str
    flag_content = x3_str + x2_str + x1_str + x0_str

    print("HFCTF{{{}}}".format(flag_content))
else:
    print("No solution found.")
