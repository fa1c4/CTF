from Crypto.Cipher import AES
import base64


# 0 ~ 7 bytes
multi2_checking_values = [ 
    0xC6, 0x70, 0xCC, 0x66, 0x68, 0x60, 0xC2, 0x70 
]

bytes_0to7 = ''
for i in range(8):
    bytes_0to7 += chr(multi2_checking_values[i] // 2)

print('0 ~ 7:', bytes_0to7)

# 8 ~ 15 bytes
xorkey = 'XorrLord'
xor_checking_values = [
    59, 9, 0x14, 0x45, 0x79, 0x56, 0x13, 0x5C
]
bytes_8to15 = ''

for i in range(8):
    bytes_8to15 += chr(xor_checking_values[i] ^ ord(xorkey[i]))

print('8 ~ 15:', bytes_8to15)

# 16 ~ 23 bytes | change table base64
ori_table = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/' 
changing_table = 'CDEFGHIJKLMNOPQRSTUVWXYZABabcdefghijklmnopqrstuvwxyz0123456789+/'
b64_enc = 'OzHhPjSzPjK'
table_mapping = str.maketrans(changing_table, ori_table)
b64_enc_ori = b64_enc.translate(table_mapping)
# print(b64_enc_ori)
b64_enc_ori += "=" * ((4 - len(b64_enc_ori) % 4) % 4)
bytes_16to23 = base64.b64decode(b64_enc_ori).decode()

print('16 ~ 23:', bytes_16to23)

# 24 ~ 31 AES ECB
AES_key = b'AesMasterAesMast'
aes_checking_values = [
    0x8C, 0xCD, 0x9E, 0x5, 0x11, 0xE2, 0xA0, 0x1D, 
    0xB0, 0xCD, 0x63, 0x7A, 0xB1, 0x37, 0x8A, 0x10
]
aes_checking_values = bytes(aes_checking_values)

cipher = AES.new(AES_key, AES.MODE_ECB)
# bytes_24to31 = cipher.decrypt(aes_checking_values).hex()
bytes_24to31 = cipher.decrypt(aes_checking_values).decode()[:8]

print('24 ~ 31:', bytes_24to31)


# final flag
flag = bytes_0to7 + bytes_8to15 + bytes_16to23 + bytes_24to31
# print(flag)
print('wdflag{' + flag + '}')
# wdflag{c8f340a8cff759a831a6436222d648f7}
