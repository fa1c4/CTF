'''
analyze the time statistic of the side channel attack
get the median of the time statistic for each digit
'''

import json

with open('./time_statistic.json', 'r') as f:
    time_statistic = json.load(f)

rounds = 10
input_code = ['0' for _ in range(6)]
for i in range(6):
    max_time = 0.0
    for j in range(10):
        median_time = sorted(time_statistic[str(i)][str(j)])[rounds // 2]
        if median_time > max_time:
            max_time = median_time
            input_code[i] = str(j)

print(''.join(input_code))
