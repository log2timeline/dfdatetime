#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for the FILETIME timestamp implementation."""

import decimal
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

  # pylint: disable=protected-access

  def testProperties(self):
    """Tests the properties."""
    filetime_object = filetime.Filetime(timestamp=0x01cb3a623d0a17ce)
    self.assertEqual(filetime_object.timestamp, 0x01cb3a623d0a17ce)

    filetime_object = filetime.Filetime()
    self.assertIsNone(filetime_object.timestamp)

  def testGetNormalizedTimestamp(self):
    """Tests the _GetNormalizedTimestamp function."""
    filetime_object = filetime.Filetime(timestamp=0x01cb3a623d0a17ce)

    normalized_timestamp = filetime_object._GetNormalizedTimestamp()
    self.assertEqual(normalized_timestamp, decimal.Decimal('1281647191.546875'))

    filetime_object = filetime.Filetime(
        time_zone_offset=60, timestamp=0x01cb3a623d0a17ce)

    normalized_timestamp = filetime_object._GetNormalizedTimestamp()
    self.assertEqual(normalized_timestamp, decimal.Decimal('1281643591.546875'))

    filetime_object = filetime.Filetime(timestamp=0x1ffffffffffffffff)

    normalized_timestamp = filetime_object._GetNormalizedTimestamp()
    self.assertIsNone(normalized_timestamp)

    filetime_object = filetime.Filetime()

    normalized_timestamp = filetime_object._GetNormalizedTimestamp()
    self.assertIsNone(normalized_timestamp)

  def testCopyFromDateTimeString(self):
    """Tests the CopyFromDateTimeString function."""
    filetime_object = filetime.Filetime()

    filetime_object.CopyFromDateTimeString('2010-08-12')
    self.assertEqual(filetime_object._timestamp, 0x1cb39b14e8c4000)
    self.assertEqual(filetime_object._time_zone_offset, 0)

    filetime_object.CopyFromDateTimeString('2010-08-12 21:06:31')
    self.assertEqual(filetime_object._timestamp, 0x1cb3a623cb6a580)
    self.assertEqual(filetime_object._time_zone_offset, 0)

    filetime_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875')
    self.assertEqual(filetime_object._timestamp, 0x01cb3a623d0a17ce)
    self.assertEqual(filetime_object._time_zone_offset, 0)

    filetime_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875-01:00')
    self.assertEqual(filetime_object._timestamp, 0x01cb3a623d0a17ce)
    self.assertEqual(filetime_object._time_zone_offset, -60)

    filetime_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875+01:00')
    self.assertEqual(filetime_object._timestamp, 0x01cb3a623d0a17ce)
    self.assertEqual(filetime_object._time_zone_offset, 60)

    filetime_object.CopyFromDateTimeString('1601-01-02 00:00:00')
    self.assertEqual(filetime_object._timestamp, 86400 * 10000000)
    self.assertEqual(filetime_object._time_zone_offset, 0)

    with self.assertRaises(ValueError):
      filetime_object.CopyFromDateTimeString('1500-01-02 00:00:00')

  def testCopyToDateTimeString(self):
    """Tests the CopyToDateTimeString function."""
    filetime_object = filetime.Filetime(timestamp=0x01cb3a623d0a17ce)

    date_time_string = filetime_object.CopyToDateTimeString()
    self.assertEqual(date_time_string, '2010-08-12 21:06:31.5468750')

    filetime_object = filetime.Filetime()

    date_time_string = filetime_object.CopyToDateTimeString()
    self.assertIsNone(date_time_string)

  def testCopyToDateTimeStringISO8601(self):
    """Tests the CopyToDateTimeStringISO8601 function."""
    filetime_object = filetime.Filetime(timestamp=0x01cb3a623d0a17ce)

    date_time_string = filetime_object.CopyToDateTimeStringISO8601()
    self.assertEqual(date_time_string, '2010-08-12T21:06:31.5468750+00:00')

  def testGetDate(self):
    """Tests the GetDate function."""
    filetime_object = filetime.Filetime(timestamp=0x01cb3a623d0a17ce)

    date_tuple = filetime_object.GetDate()
    self.assertEqual(date_tuple, (2010, 8, 12))

    filetime_object = filetime.Filetime()

    date_tuple = filetime_object.GetDate()
    self.assertEqual(date_tuple, (None, None, None))

  def testGetDateWithTimeOfDay(self):
    """Tests the GetDateWithTimeOfDay function."""
    filetime_object = filetime.Filetime(timestamp=0x01cb3a623d0a17ce)

    date_with_time_of_day_tuple = filetime_object.GetDateWithTimeOfDay()
    self.assertEqual(date_with_time_of_day_tuple, (2010, 8, 12, 21, 6, 31))

    filetime_object = filetime.Filetime()

    date_with_time_of_day_tuple = filetime_object.GetDateWithTimeOfDay()
    self.assertEqual(
        date_with_time_of_day_tuple, (None, None, None, None, None, None))

  def testGetTimeOfDay(self):
    """Tests the GetTimeOfDay function."""
    filetime_object = filetime.Filetime(timestamp=0x01cb3a623d0a17ce)

    time_of_day_tuple = filetime_object.GetTimeOfDay()
    self.assertEqual(time_of_day_tuple, (21, 6, 31))

    filetime_object = filetime.Filetime()

    time_of_day_tuple = filetime_object.GetTimeOfDay()
    self.assertEqual(time_of_day_tuple, (None, None, None))


if __name__ == '__main__':
  unittest.main()
