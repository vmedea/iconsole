from binascii import hexlify,unhexlify
import packets

def read_log(logfile):
    with open(logfile, 'r') as f:
        for line in f:
            line = line.rstrip().split()
            timestamp = float(line[0])
            pkt = unhexlify(line[1])
            if pkt[1] == 0xb2:
                ic = packets.ReadResponse(pkt)
                yield (timestamp, ic)
