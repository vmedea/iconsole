'''
Packet descriptions for iConsole serial protocol.
'''

# Packets
INIT_A0 = bytes([0xf0, 0xa0, 0x02, 0x02])
# f0:b7:01:01:04 INIT_A0_RESPONSE (get version?)

PING    = bytes([0xf0, 0xa0, 0x01, 0x01])
# f0:b0:01:01 PONG

PONG    = bytes([0xf0, 0xb0, 0x01, 0x01])

STATUS  = bytes([0xf0, 0xa1, 0x01, 0x01])
# f0:b1:01:01:21  STATUS_RESPONSE
#    last byte seems to be "max level"

READ    = bytes([0xf0, 0xa2, 0x01, 0x01])
# f0:b2:01:01:01:01:01:01:01:01:01:01:01:01:01:45:01:01:21:02  READ_RESPONSE
#   0 1 : f0:b2
#   2 3 4 5 : d:h:m:s
#   6 7: SPEED kmh * 10
#   8 9: RPM
#   10 11: distance in 10m
#   12 13: calories
#   14 15: HF
#   16 17: WATT * 10
#   18: LVL
#   19: state (1=stopped, 2=started)

INIT_A3 = bytes([0xf0, 0xa3, 0x01, 0x01, 0x01])
# f0:b3:01:01:01  INIT_A3_RESPONSE

INIT_A4 = bytes([0xf0, 0xa4, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01])
# f0:b4:01:01:01:01:01:01:01:01:01:01:01:01  INIT_A4_RESPONSE

START   = bytes([0xf0, 0xa5, 0x01, 0x01, 0x02])
# f0:b5:01:01:02  STARTED

STOP    = bytes([0xf0, 0xa5, 0x01, 0x01, 0x04])
# f0:b5:01:01:04  STOPPED

SET_LEVEL = bytes([0xf0, 0xa6, 0x01, 0x01, 0x00]) # last byte is lvl + 1
# f0:b6:01:01:21  SET_LEVEL_RESPONSE (last byte is lvl + 1)

class ReadResponse(object):
    '''
    Parse the response to a READ packet.
    '''
    def __init__(self, gota):
        self.time = (gota[4] - 1) * 60 + gota[5] - 1
        self.speed = ((100*(gota[6] - 1) + gota[7] - 1) / 10.0)
        self.rpm = ((100*(gota[8] - 1) + gota[9] - 1))
        self.distance = ((100*(gota[10]-1) + gota[11] - 1) / 10.0)
        self.calories = ((100*(gota[12]-1) + gota[13] - 1))
        self.hf = ((100*(gota[14]-1) + gota[15] - 1))
        self.power = ((100*(gota[16]-1) + gota[17] -1) / 10.0)
        self.lvl = gota[18] - 1

    def __str__(self):
        time_str = "%3d:%02d" % (self.time // 60, self.time % 60)
        speed_str = "V: % 5.1f km/h" % self.speed
        rpm_str = "%3d RPM" % self.rpm
        distance_str = "D: %4.1f km" % self.distance
        calories_str = "%4d kcal" % self.calories
        hf_str = "HF %3d" % self.hf
        power_str = "%5.1f W" % self.power
        lvl_str = "L: %d" % self.lvl
        return ("%s - %s - %s - %s - %s - %s - %s - %s" % (time_str,
                                                         speed_str,
                                                         rpm_str,
                                                         distance_str,
                                                         calories_str,
                                                         hf_str,
                                                         power_str,
                                                         lvl_str))
