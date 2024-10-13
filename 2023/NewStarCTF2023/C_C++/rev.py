'''
.Net reverse

0 -> 35: input[i] += i - chr(' ')
0 -> 6: input[i] += k ^ -(key_text[k] % 4)
7 -> 13: input[i] += key_text[k] % 5
14 -> 20: input[i] += 2 * k
21 -> 27: input[i] += 2 ^ k
28 -> 34: input[i] += key_text[k] // 5 + chr('\n')
'''

checking_arr = [68, 75, 66, 72, 99, 19, 19, 78, 83, 74,
        91, 86, 35, 39, 77, 85, 44, 89, 47, 92,
        49, 88, 48, 91, 88, 102, 105, 51, 76, 115,
        -124, 125, 79, 122, -103]

key_text = "NEWSTAR"

for i in range(35):
    k = i % 7
    if i >= 0 and i <= 6:
        checking_arr[i] -= k ^ -(ord(key_text[k]) % 4)
    elif i >= 7 and i <= 13:
        checking_arr[i] -= ord(key_text[k]) % 5
    elif i >= 14 and i <= 20:
        checking_arr[i] -= 2 * k
    elif i >= 21 and i <= 27:
        checking_arr[i] -= 2 ^ k
    elif i >= 28 and i <= 34:
        checking_arr[i] -= ord(key_text[k]) // 5 + ord('\n')
    else:
        print('invalid i range')

flag = ''
for i in range(35):
    checking_arr[i] -= i - ord(' ')
    print(checking_arr[i], end=' ')
    checking_arr[i] = checking_arr[i] % 256
    flag += chr(checking_arr[i])

print(f'\n{flag}')
