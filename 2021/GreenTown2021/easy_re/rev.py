flag = [
    0xF5, 0x8C, 0x8D, 0xE4, 0x9F, 0xA5, 0x28, 0x65, 0x30, 0xF4, 
    0xEB, 0xD3, 0x24, 0xA9, 0x91, 0x1A, 0x6F, 0xD4, 0x6A, 0xD7, 
    0x0B, 0x8D, 0xE8, 0xB8, 0x83, 0x4A, 0x5A, 0x6E, 0xBE, 0xCB, 
    0xF4, 0x4B, 0x99, 0xD6, 0xE6, 0x54, 0x7A, 0x4F, 0x50, 0x14,
    0xE5, 0XEC
]
key = [
    0x93, 0xE0, 0xEC, 0x83, 0xE4, 0xC6, 0x1D, 0x00, 0x00, 0x92,
    0xDE, 0xB5, 0x12, 0x84, 0xF7, 0x2D, 0x56, 0xB1, 0x47, 0xE2, 
    0x69, 0xB4, 0x8A, 0x95, 0xBA, 0x72, 0x62, 0x08, 0x93, 0xF9, 
    0xCC, 0x2D, 0xA9, 0xE2, 0xD0, 0x65, 0x4B, 0x78, 0x68, 0x24, 
    0xD7, 0x91 
]


if __name__ == '__main__':
    for i in range(len(flag)):
        flag[i] ^= key[i]
        print(chr(flag[i]), end='')
    
    print('')

    # flag{c5e0f5f6-f79e-5b9b-988f-28f046117802}
    