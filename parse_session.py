#!/usr/bin/env python3
'''
Parse a raw iConsole packet log into human readable format.
'''
import sys
import csv
from read_log import read_log

log = read_log(sys.argv[1])
#fmt = 'txt'
fmt = 'csv'

writer = None
if fmt == 'csv':
    writer = csv.writer(sys.stdout)
    writer.writerow(['Time', 'Speed (km/h)', 'RPM', 'Distance (km)', 'Calories', 'HF', 'Power (W)', 'LVL'])

for timestamp, ic in log:
    if fmt == 'txt':
        print(ic)
    elif fmt == 'csv':
        time_str = "%d:%02d" % (ic.time // 60, ic.time % 60)
        fields = [time_str, ic.speed, ic.rpm, ic.distance, ic.calories, ic.hf, ic.power, ic.lvl]
        writer.writerow(fields)
