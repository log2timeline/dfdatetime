#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the UUID version 1 timestamp implementation."""

import uuid
import unittest

from dfdatetime import uuid_time


class UUIDTimeTest(unittest.TestCase):
  """Tests for the UUID version 1 timestamp."""

  def testInitialize(self):
    """Tests the initialization function."""
    uuid_time_object = uuid_time.UUIDTime()
    self.assertIsNotNone(uuid_time_object)

    uuid_object = uuid.UUID(u'00911b54-9ef4-11e1-be53-525400123456')
    uuid_time_object = uuid_time.UUIDTime(timestamp=uuid_object.time)
    self.assertIsNotNone(uuid_time_object)
    expected_timestamp = 135564234616544084
    self.assertEqual(uuid_time_object.timestamp, expected_timestamp)

    with self.assertRaises(ValueError):
      uuid_time.UUIDTime(timestamp=0x1fffffffffffffff)

    with self.assertRaises(ValueError):
      uuid_time.UUIDTime(timestamp=-1)

  def testCopyFromString(self):
    """Tests the CopyFromString function."""
    uuid_time_object = uuid_time.UUIDTime()

    expected_timestamp = 135946080000000000
    uuid_time_object.CopyFromString(u'2013-08-01')
    self.assertEqual(uuid_time_object.timestamp, expected_timestamp)

    expected_timestamp = 135946635280000000
    uuid_time_object.CopyFromString(u'2013-08-01 15:25:28')
    self.assertEqual(uuid_time_object.timestamp, expected_timestamp)

    expected_timestamp = 135946635285468750
    uuid_time_object.CopyFromString(u'2013-08-01 15:25:28.546875')
    self.assertEqual(uuid_time_object.timestamp, expected_timestamp)

    expected_timestamp = 135946671285468750
    uuid_time_object.CopyFromString(u'2013-08-01 15:25:28.546875-01:00')
    self.assertEqual(uuid_time_object.timestamp, expected_timestamp)

    expected_timestamp = 135946599285468750
    uuid_time_object.CopyFromString(u'2013-08-01 15:25:28.546875+01:00')
    self.assertEqual(uuid_time_object.timestamp, expected_timestamp)

    expected_timestamp = 864000000000
    uuid_time_object.CopyFromString(u'1582-10-16 00:00:00')
    self.assertEqual(uuid_time_object.timestamp, expected_timestamp)

    with self.assertRaises(ValueError):
      uuid_time_object.CopyFromString(u'1570-01-02 00:00:00')

  def testCopyToStatTimeTuple(self):
    """Tests the CopyToStatTimeTuple function."""
    uuid_object = uuid.UUID(u'00911b54-9ef4-11e1-be53-525400123456')
    uuid_time_object = uuid_time.UUIDTime(timestamp=uuid_object.time)

    expected_stat_time_tuple = (1337130661, 6544084)
    stat_time_tuple = uuid_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, expected_stat_time_tuple)

    uuid_time_object = uuid_time.UUIDTime()
    uuid_time_object.timestamp = 0x1fffffffffffffff

    expected_stat_time_tuple = (None, None)
    stat_time_tuple = uuid_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, expected_stat_time_tuple)

    uuid_time_object = uuid_time.UUIDTime()
    uuid_time_object.timestamp = -1

    expected_stat_time_tuple = (None, None)
    stat_time_tuple = uuid_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, expected_stat_time_tuple)

    uuid_time_object = uuid_time.UUIDTime()

    expected_stat_time_tuple = (None, None)
    stat_time_tuple = uuid_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, expected_stat_time_tuple)

  def testGetPlasoTimestamp(self):
    """Tests the GetPlasoTimestamp function."""
    uuid_object = uuid.UUID(u'00911b54-9ef4-11e1-be53-525400123456')
    uuid_time_object = uuid_time.UUIDTime(timestamp=uuid_object.time)

    expected_micro_posix_timestamp = 1337130661654408
    micro_posix_timestamp = uuid_time_object.GetPlasoTimestamp()
    self.assertEqual(micro_posix_timestamp, expected_micro_posix_timestamp)

    uuid_time_object = uuid_time.UUIDTime()
    uuid_time_object.timestamp = 0x1fffffffffffffff

    micro_posix_timestamp = uuid_time_object.GetPlasoTimestamp()
    self.assertIsNone(micro_posix_timestamp)

    uuid_time_object = uuid_time.UUIDTime()
    uuid_time_object.timestamp = -1

    micro_posix_timestamp = uuid_time_object.GetPlasoTimestamp()
    self.assertIsNone(micro_posix_timestamp)

    uuid_time_object = uuid_time.UUIDTime()

    micro_posix_timestamp = uuid_time_object.GetPlasoTimestamp()
    self.assertIsNone(micro_posix_timestamp)


if __name__ == '__main__':
  unittest.main()
