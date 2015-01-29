from struct import pack, unpack, unpack_from, calcsize

PING = 0x0001
TEXT = 0x0002
CLIENT_MESSAGE = 0x0003

def get_type(packet):
    return unpack_from('h', packet)[0]

def pack_ping():
    return pack('h', PING)

def pack_text(text):
    length = len(text)
    return pack('hh%ds' % length, # Dynamisches format
        TEXT,   # 0x0002
        length,              # Textlaenge
        text)                   # Text

def unpack_text(packet):
    length = len(packet) - calcsize('hh')
    return unpack('hh%ds' % length, packet)[2]

def pack_client_message(username, text):
    usernameLength = len(username)
    textLength = len(text)
    return pack('hh%dsh%ds' % (textLength, usernameLength),
        CLIENT_MESSAGE,
        textLength,
        text,
        usernameLength,
        username)

def unpack_client_message(packet):
    textHeaderSize = calcsize('hh')
    textLength = unpack_from('hh', packet)[1]
    text = packet[textHeaderSize:textHeaderSize+textLength]

    usernamePacket = packet[textHeaderSize+len(text):]
    usernameHeaderSize = calcsize('h')
    username = unpack_from('h%ds' % (len(usernamePacket) - usernameHeaderSize), usernamePacket)[1]

    return (username, text)

def unpack_packet(packet):
    # Die ersten beiden Bytes betrachten
    packet_type = get_type(packet)

    # Wenn es ein PING ist, muessen wir nichts weiter tun
    if packet_type is PING:
        return packet_type
    elif packet_type is TEXT:
        return unpack_text(packet)
    elif packet_type is CLIENT_MESSAGE:
        return unpack_client_message(packet)
