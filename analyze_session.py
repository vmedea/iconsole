#!/usr/bin/env python3
'''
Parse a raw iConsole packet log into human readable format.
'''
import sys
import csv
import collections
from read_log import read_log

stats = []
for filename in sys.argv[1:]:
    log = read_log(filename)

    hf_histogram = collections.defaultdict(int)
    rpm_histogram = collections.defaultdict(int)
    prevtime = 0
    calories = 0
    for timestamp, ic in log:
        delta = ic.time - prevtime
        if delta > 0:
            hf_histogram[(ic.hf // 10) * 10] += delta
            rpm_histogram[(ic.rpm // 10) * 10] += delta
        calories = ic.calories
        prevtime = ic.time

    stats.append((filename, hf_histogram, rpm_histogram, calories))

for idx, (filename, _, _, _) in enumerate(stats):
    print('[{}] {}'.format(idx + 1, filename))
print()

hdrs = []
for num in range(len(stats)):
    s = f'[{num + 1}]'
    s = f'{s:6}'
    hdrs.append(s)
hdrs = ''.join(hdrs)

print('Stats ' + hdrs)
print('-' * (len(hdrs) + 3))

line = "cal"
for (_, _, _, calories) in stats:
    line += ' {:5}'.format(calories)
print(line)
print()

print(' HF   ' + hdrs)
print('-' * (len(hdrs) + 3))
for hf in range(60, 170, 10):
    line = f"{hf:3}"
    for (_, hf_histogram, _, _) in stats:
        line += ' {:5}'.format(hf_histogram[hf])
    print(line)
print()

print('RPM   ' + hdrs)
print('-' * (len(hdrs) + 3))
for rpm in range(00, 100, 10):
    line = f"{rpm:3}"
    for (_, _, rpm_histogram, _) in stats:
        line += ' {:5}'.format(rpm_histogram[rpm])
    print(line)
