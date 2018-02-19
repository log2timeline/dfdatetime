#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the FILETIME timestamp implementation."""

from __future__ import unicode_literals

import unittest

from dfdatetime import filetime


class FiletimeEpochTest(unittest.TestCase):
  """Tests for the FILETIME epoch."""

  def testInitialize(self):
    """Tests the __init__ function."""
    filetime_epoch = filetime.FiletimeEpoch()
    self.assertIsNotNone(filetime_epoch)


class FiletimeTest(unittest.TestCase):
  """Tests for the FILETIME timestamp."""

  def testCopyFromDateTimeString(self):
    """Tests the CopyFromDateTimeString function."""
    filetime_object = filetime.Filetime()

    expected_timestamp = 0x1cb39b14e8c4000
    filetime_object.CopyFromDateTimeString('2010-08-12')
    self.assertEqual(filetime_object.timestamp, expected_timestamp)

    expected_timestamp = 0x1cb3a623cb6a580
    filetime_object.CopyFromDateTimeString('2010-08-12 21:06:31')
    self.assertEqual(filetime_object.timestamp, expected_timestamp)

    expected_timestamp = 0x01cb3a623d0a17ce
    filetime_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875')
    self.assertEqual(filetime_object.timestamp, expected_timestamp)

    expected_timestamp = 0x1cb3a6a9ece7fce
    filetime_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875-01:00')
    self.assertEqual(filetime_object.timestamp, expected_timestamp)

    expected_timestamp = 0x1cb3a59db45afce
    filetime_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875+01:00')
    self.assertEqual(filetime_object.timestamp, expected_timestamp)

    expected_timestamp = 86400 * 10000000
    filetime_object.CopyFromDateTimeString('1601-01-02 00:00:00')
    self.assertEqual(filetime_object.timestamp, expected_timestamp)

    with self.assertRaises(ValueError):
      filetime_object.CopyFromDateTimeString('1500-01-02 00:00:00')

  def testCopyToStatTimeTuple(self):
    """Tests the CopyToStatTimeTuple function."""
    filetime_object = filetime.Filetime(timestamp=0x01cb3a623d0a17ce)

    stat_time_tuple = filetime_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, (1281647191, 5468750))

    filetime_object = filetime.Filetime(timestamp=0x1ffffffffffffffff)

    stat_time_tuple = filetime_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, (None, None))

    filetime_object = filetime.Filetime()

    stat_time_tuple = filetime_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, (None, None))

  def testCopyToDateTimeString(self):
    """Tests the CopyToDateTimeString function."""
    filetime_object = filetime.Filetime(timestamp=0x01cb3a623d0a17ce)

    date_time_string = filetime_object.CopyToDateTimeString()
    self.assertEqual(date_time_string, '2010-08-12 21:06:31.5468750')

    filetime_object = filetime.Filetime()

    date_time_string = filetime_object.CopyToDateTimeString()
    self.assertIsNone(date_time_string)

  def testGetDate(self):
    """Tests the GetDate function."""
    filetime_object = filetime.Filetime(timestamp=0x01cb3a623d0a17ce)

    date_tuple = filetime_object.GetDate()
    self.assertEqual(date_tuple, (2010, 8, 12))

    filetime_object._EPOCH.year = -1

    date_tuple = filetime_object.GetDate()
    self.assertEqual(date_tuple, (None, None, None))

    filetime_object = filetime.Filetime()

    date_tuple = filetime_object.GetDate()
    self.assertEqual(date_tuple, (None, None, None))

  def testGetPlasoTimestamp(self):
    """Tests the GetPlasoTimestamp function."""
    filetime_object = filetime.Filetime(timestamp=0x01cb3a623d0a17ce)

    micro_posix_timestamp = filetime_object.GetPlasoTimestamp()
    self.assertEqual(micro_posix_timestamp, 1281647191546875)

    filetime_object = filetime.Filetime(timestamp=0x1ffffffffffffffff)

    micro_posix_timestamp = filetime_object.GetPlasoTimestamp()
    self.assertIsNone(micro_posix_timestamp)

    filetime_object = filetime.Filetime()

    micro_posix_timestamp = filetime_object.GetPlasoTimestamp()
    self.assertIsNone(micro_posix_timestamp)


if __name__ == '__main__':
  unittest.main()
