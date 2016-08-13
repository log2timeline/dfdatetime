#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the FILETIME timestamp implementation."""

import unittest

from dfdatetime import filetime


class FiletimeTest(unittest.TestCase):
  """Tests for the FILETIME timestamp."""

  def testCopyFromString(self):
    """Tests the CopyFromString function."""
    filetime_object = filetime.Filetime()

    expected_timestamp = 0x1cb39b14e8c4000
    filetime_object.CopyFromString(u'2010-08-12')
    self.assertEqual(filetime_object.timestamp, expected_timestamp)

    expected_timestamp = 0x1cb3a623cb6a580
    filetime_object.CopyFromString(u'2010-08-12 21:06:31')
    self.assertEqual(filetime_object.timestamp, expected_timestamp)

    expected_timestamp = 0x01cb3a623d0a17ce
    filetime_object.CopyFromString(u'2010-08-12 21:06:31.546875')
    self.assertEqual(filetime_object.timestamp, expected_timestamp)

    expected_timestamp = 0x1cb3a6a9ece7fce
    filetime_object.CopyFromString(u'2010-08-12 21:06:31.546875-01:00')
    self.assertEqual(filetime_object.timestamp, expected_timestamp)

    expected_timestamp = 0x1cb3a59db45afce
    filetime_object.CopyFromString(u'2010-08-12 21:06:31.546875+01:00')
    self.assertEqual(filetime_object.timestamp, expected_timestamp)

    expected_timestamp = 86400 * 10000000
    filetime_object.CopyFromString(u'1601-01-02 00:00:00')
    self.assertEqual(filetime_object.timestamp, expected_timestamp)

    with self.assertRaises(ValueError):
      filetime_object.CopyFromString(u'1500-01-02 00:00:00')

  def testCopyToStatTimeTuple(self):
    """Tests the CopyToStatTimeTuple function."""
    filetime_object = filetime.Filetime(timestamp=0x01cb3a623d0a17ce)

    expected_stat_time_tuple = (1281647191, 5468750)
    stat_time_tuple = filetime_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, expected_stat_time_tuple)

    filetime_object = filetime.Filetime(timestamp=0x1ffffffffffffffff)

    expected_stat_time_tuple = (None, None)
    stat_time_tuple = filetime_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, expected_stat_time_tuple)

    filetime_object = filetime.Filetime()

    expected_stat_time_tuple = (None, None)
    stat_time_tuple = filetime_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, expected_stat_time_tuple)

  def testGetPlasoTimestamp(self):
    """Tests the GetPlasoTimestamp function."""
    filetime_object = filetime.Filetime(timestamp=0x01cb3a623d0a17ce)

    expected_micro_posix_timestamp = 1281647191546875
    micro_posix_timestamp = filetime_object.GetPlasoTimestamp()
    self.assertEqual(micro_posix_timestamp, expected_micro_posix_timestamp)

    filetime_object = filetime.Filetime(timestamp=0x1ffffffffffffffff)

    micro_posix_timestamp = filetime_object.GetPlasoTimestamp()
    self.assertIsNone(micro_posix_timestamp)

    filetime_object = filetime.Filetime()

    micro_posix_timestamp = filetime_object.GetPlasoTimestamp()
    self.assertIsNone(micro_posix_timestamp)


if __name__ == '__main__':
  unittest.main()
