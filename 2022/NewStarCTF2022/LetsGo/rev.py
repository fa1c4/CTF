'''
1. get the key and encrypted from IDApro9.0
    qmemcpy(key, "NewStar!NewStar!", 16);
    v3 = "ee01674b13ff8dd86f8e481aa86f5d25e773a3fd0338f60988cb738b8b178c44";
2. debug to determine what IV is, and find IV.array initialized by 0xFF56C0 (NewStar!NewStar!)
3. AES CBC mode decrypt to get flag
'''

from Crypto.Cipher import AES

AES_key = b'NewStar!NewStar!'
data_bytes = bytes.fromhex('ee01674b13ff8dd86f8e481aa86f5d25e773a3fd0338f60988cb738b8b178c44')
# AES_iv = b"\x7C\x57\x45\x61\x46\x53\x40\x13\x7C\x57\x45\x61\x46\x53\x40\x13"
AES_iv = []
for i in AES_key:
    AES_iv.append(i ^ 0x32)

AES_iv = bytes(AES_iv)
# print(AES_iv)

cipher = AES.new(AES_key, AES.MODE_CBC, AES_iv)
decrypted = cipher.decrypt(data_bytes)
print(decrypted.decode())
