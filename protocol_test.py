import random
import unittest
import protocol
from crypto import encryptedMessage, decryptedMessage

class TestProtocol(unittest.TestCase):

    def setUp(self):
        self.seq = range(10)

    def test_pack_ping(self):
        res = protocol.pack_ping()

        self.assertEqual(res, '\x00\x01')

    def test_unpack_ping(self):
        res = protocol.unpack_packet('\x00\x01')

        self.assertEqual(res, 0x0001)

    def test_pack_text(self):
        res = protocol.pack_text(encryptedMessage('Client %s is offline.' % 4,6))
        expected = '\x00\x02\x00\x14Iroktz 4 oy ullrotk.'

        self.assertEqual(res, expected)

    def test_unpack_text(self):
        decrypted = decryptedMessage('\x00\x02\x00\x14Iroktz 4 oy ullrotk.', 6)
        res = protocol.unpack_packet(decrypted)
        expected = 'Client 4 is offline.'

        self.assertEqual(res, expected)

    def test_pack_client_message(self):
        res = protocol.pack_client_message('foo', 'barbaz')
        expected = '\x00\x03\x00\x06barbaz\x00\x03foo'

        self.assertEqual(res, expected)

    def test_unpack_client_message(self):
        res = protocol.unpack_client_message('\x00\x03\x00\x06barbaz\x00\x03foo')
        expected = ('foo', 'barbaz')

        self.assertEqual(res, expected)



if __name__ == '__main__':
    unittest.main()
