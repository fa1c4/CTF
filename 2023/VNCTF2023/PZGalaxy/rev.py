enc = ['¦', 'p', ':', 'Ü', '\x92', 'Ã', '\x97', 'ó', '\x1A', 'ß', '\b', 'Ö', 'A', ' ', '5', '\x90', '{', '\x06', 'Ô', '÷', 's', '_', '\x1D', ':', 'I', 'L', 'C', 'X', 'Ñ', '¹', 'O', '\x99', '\x85', '3', 'à', 'i', '|']

# RC4 algorithm
def rc4(key, data):
    S = list(range(256))
    j = 0
    out = []
    key = [ord(c) for c in key]  # Convert the key to a list of ASCII values
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    i = j = 0
    for char in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        out.append(chr(ord(char) ^ S[(S[i] + S[j]) % 256]))
    return ''.join(out)

# Decrypt the flag
# brute force the key with 8 length where first four digits are known
key_pre = '2023'
for i in range(10000):
    key = key_pre + str(i).zfill(4)
    try:
        flag = rc4(key, enc)
        if 'flag' in flag.lower():  # Check case-insensitively
            print(f"Key found: {key}")
            print(f"Decrypted flag: {flag}")
            break
    except Exception as e:
        print(f"Error with key {key}: {e}")
