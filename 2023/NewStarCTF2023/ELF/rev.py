'''
[1] input flag, encode(flag) -> procstr
[2] base64 encode the procstr -> b64_str
[3] b64_str equal to checking_b64
'''

import base64

checking_b64 = 'VlxRV2t0II8kX2WPJ15fZ49nWFEnj3V8do8hYy9t'
proc_str = base64.b64decode(checking_b64)
# print(proc_str)

flag = ''
for i in range(len(proc_str)):
    ch = (proc_str[i] - 16) ^ 0x20
    flag += chr(ch)

print(flag)
