import sys
import math
import time
import string
import struct
import socket
import pandas as pd
import numpy as np


def _readString(data):
    """Reads the next (null-terminated) block of data
    """
    length = string.find(data, "\0")
    nextData = int(math.ceil((length+1) / 4.0) * 4)
    return (data[0:length], data[nextData:])


def _readBlob(data):
    """Reads the next (numbered) block of data
    """
    length = struct.unpack(">i", data[0:4])[0]
    nextData = int(math.ceil((length) / 4.0) * 4) + 4
    return (data[4:length+4], data[nextData:])


def _readInt(data):
    """Tries to interpret the next 4 bytes of the data
    as a 32-bit integer. """
    if(len(data) < 4):
        print "Error: too few bytes for int", data, len(data)
        rest = data
        integer = 0
    else:
        integer = struct.unpack(">i", data[0:4])[0]
        rest = data[4:]

    return (integer, rest)


def _readTimeTag(data):
    """Tries to interpret the next 8 bytes of the data
    as a TimeTag.
     """
    high, low = struct.unpack(">ll", data[0:8])
    if (high == 0) and (low <= 1):
        time = 0.0
    else:
        time = int(high) + float(low / 1e9)
    rest = data[8:]
    return (time, rest)


def _readFloat(data):
    """Tries to interpret the next 4 bytes of the data
    as a 32-bit float.
    """

    if(len(data) < 4):
        print "Error: too few bytes for float", data, len(data)
        rest = data
        float = 0
    else:
        float = struct.unpack(">f", data[0:4])[0]
        rest = data[4:]

    return (float, rest)


def decodeOSC(data):
    """Converts a binary OSC message to a Python list.
    """
    table = {"i": _readInt, "f": _readFloat, "s": _readString, "b": _readBlob}
    decoded = []
    address,  rest = _readString(data)
    if address.startswith(","):
        typetags = address
        address = ""
    else:
        typetags = ""

    if address == "#bundle":
        time, rest = _readTimeTag(rest)
        decoded.append(address)
        decoded.append(time)
        while len(rest) > 0:
            length, rest = _readInt(rest)
            decoded.append(decodeOSC(rest[:length]))
            rest = rest[length:]

    elif len(rest) > 0:
        if not len(typetags):
            typetags, rest = _readString(rest)
        decoded.append(address)
        decoded.append(typetags)
        if typetags.startswith(","):
            for tag in typetags[1:]:
                value, rest = table[tag](rest)
                decoded.append(value)
        else:
            raise ValueError("OSCMessage's typetag-string lacks the magic ','")

    return decoded


def get_inv_map():

    path = "/Users/JRLetelier/perso/sonification/data/sources/oced/oced_code_treatment.csv"
    df = pd.read_csv(path, sep=';', engine="python")[["new_indicator_name", "treatment"]]
    df["new_indicator_name"] = df["new_indicator_name"].apply(lambda n: n.replace(',', ''))
    map_ = {t.new_indicator_name: t.treatment for t in df.itertuples()}

    def share(x):
        return ('%1.1f' % (100*(1-x)/2.) + "%")

    def no_treat(x):
        return x

    def percentage(x):
        return ('%1.1f' % (100.*x) + "%")

    def no_treat_percent(x):
        return ('%1.1f' % (100.*x) + "%")

    def sex(x):
        return ("%1.1f" % (100*x) + "% men/women difference")

    inv_fn = {'share': share,
              'no_treat': no_treat,
              'percentage': percentage,
              'no_treat_percent': no_treat_percent,
              'sex': sex,
              }

    return {k: inv_fn[v] for k, v in map_.iteritems()}


if __name__ == "__main__":

    UDP_IP = sys.argv[1]  # "localhost"
    UDP_PORT = int(sys.argv[2])  # 9001

    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP
    sock.bind((UDP_IP, UDP_PORT))

    inv_fn_map = get_inv_map()

    # clear window
    for i in range(300):
        print '\n'

    while True:
        decoded = decodeOSC(sock.recv(1024))
        endpoint, types_ = decoded[:2]
        if endpoint == "/woman":
            country, measure, year, value = decoded[2:]
            country = country.replace('_', ' ').replace('__', ' ')
            measure = measure.replace('_', ' ').replace('__', ' ').replace('  ', ' ')
            indent = np.random.randint(0, 10)
            if measure in inv_fn_map:
                # print "value new: %f" % value
                value = inv_fn_map[measure](value)
                # print inv_fn_map[measure].__name__
                # print "value old: %s" % value
            if year == 0:
                year = 'Various years'
            print ("\t" * indent + "%s %s %s %s" % (country, measure, year, value) + '\n')
        elif endpoint == "/clean":
            for i in range(200):
                print '\n'
        else:
            raise ValueError("Wrong endpoint %s. Must be '/woman' or '/clean'.")
