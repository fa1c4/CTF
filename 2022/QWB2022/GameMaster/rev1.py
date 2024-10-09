'''
<rev1.py>
1. reverse the blackjack logic, find that gamemessage is xor and decrypted by AES
2. decrypt the gamemessage, find that MZ in the binary data
3. export MZ... data as binary file using 010 editor

<rev2.py>
4. reverse the binary as .Net binary, find that x,y,z (array[0], array[1], array[2]) is flag related data
5. Z3 solve the included .Net binary logic to get x,y,z data (flag)
'''

from Crypto.Cipher import AES


with open("gamemessage", "rb") as f:
    gamemessage = f.read()

dataArr = [t for t in gamemessage]

for i in range(len(dataArr)):
    dataArr[i] ^= 34
data_bytes = bytes(dataArr)

AES_key = [66, 114, 97, 105, 110, 115, 116, 111, 114, 109, 105, 110, 103, 33, 33, 33]
AES_key = bytes(AES_key)

cipher = AES.new(AES_key, AES.MODE_ECB)
decrypted = cipher.decrypt(data_bytes)

binary_dump = './DEC'
with open(binary_dump, 'wb') as f:
    f.write(decrypted)
print('Decrypted data saved as', binary_dump)
