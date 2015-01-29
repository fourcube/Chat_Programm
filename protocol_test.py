import random
import unittest
import protocol

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
        res = protocol.pack_text('foo')
        expected = '\x00\x02\x00\x03foo'

        self.assertEqual(res, expected)

    def test_unpack_text(self):
        res = protocol.unpack_packet('\x00\x02\x00\x03foo')
        expected = 'foo'

        self.assertEqual(res, expected)


if __name__ == '__main__':
    unittest.main()
