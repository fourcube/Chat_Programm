from struct import pack, unpack, unpack_from, calcsize

PING = 0x0001
TEXT = 0x0002

def get_type(packet):
    return unpack_from('!h', packet)[0]

def pack_ping():
    return pack('!h', PING)

def pack_text(text):
    length = len(text)
    return pack('!hh%ds' % length, # Dynamisches format
        TEXT,   # 0x0002
        len(text),              # Textlaenge
        text)                   # Text

def unpack_text(packet):
    length = len(packet) - calcsize('!hh')
    return unpack('!hh%ds' % length, packet)[2]

def unpack_packet(packet):
    # Die ersten beiden Bytes betrachten
    packet_type = get_type(packet)

    # Wenn es ein PING ist, muessen wir nichts weiter tun
    if packet_type is PING:
        return packet_type
    elif packet_type is TEXT:
        return unpack_text(packet)
