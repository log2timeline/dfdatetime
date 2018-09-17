#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for the APFS timestamp implementation."""

from __future__ import unicode_literals

import decimal
import unittest

from dfdatetime import apfs_time


class APFSTimeTest(unittest.TestCase):
  """Tests for the APFS timestamp."""

  # pylint: disable=protected-access

  def testProperties(self):
    """Tests the properties."""
    apfs_time_object = apfs_time.APFSTime(timestamp=1281643591987654321)
    self.assertEqual(apfs_time_object.timestamp, 1281643591987654321)

    apfs_time_object = apfs_time.APFSTime()
    self.assertIsNone(apfs_time_object.timestamp)

  def testGetNormalizedTimestamp(self):
    """Tests the _GetNormalizedTimestamp function."""
    apfs_time_object = apfs_time.APFSTime(timestamp=1281643591987654321)

    normalized_timestamp = apfs_time_object._GetNormalizedTimestamp()
    self.assertEqual(
        normalized_timestamp, decimal.Decimal('1281643591.987654321'))

    apfs_time_object = apfs_time.APFSTime()

    normalized_timestamp = apfs_time_object._GetNormalizedTimestamp()
    self.assertIsNone(normalized_timestamp)

  def testCopyFromDateTimeString(self):
    """Tests the CopyFromDateTimeString function."""
    apfs_time_object = apfs_time.APFSTime()

    expected_timestamp = 1281571200000000000
    apfs_time_object.CopyFromDateTimeString('2010-08-12')
    self.assertEqual(apfs_time_object.timestamp, expected_timestamp)

    expected_timestamp = 1281647191000000000
    apfs_time_object.CopyFromDateTimeString('2010-08-12 21:06:31')
    self.assertEqual(apfs_time_object.timestamp, expected_timestamp)

    expected_timestamp = 1281647191654321000
    apfs_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.654321')
    self.assertEqual(apfs_time_object.timestamp, expected_timestamp)

    expected_timestamp = 1281650791654321000
    apfs_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.654321-01:00')
    self.assertEqual(apfs_time_object.timestamp, expected_timestamp)

    expected_timestamp = 1281643591654321000
    apfs_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.654321+01:00')
    self.assertEqual(apfs_time_object.timestamp, expected_timestamp)

    expected_timestamp = -11644387200000000000
    apfs_time_object.CopyFromDateTimeString('1601-01-02 00:00:00')
    self.assertEqual(apfs_time_object.timestamp, expected_timestamp)

    apfs_time_object = apfs_time.APFSTime()
    with self.assertRaises(ValueError):
      apfs_time_object.CopyFromDateTimeString('2554-07-21 23:34:34.000000')

  def testCopyToDateTimeString(self):
    """Tests the CopyToDateTimeString function."""
    apfs_time_object = apfs_time.APFSTime(timestamp=1281643591987654321)

    date_time_string = apfs_time_object.CopyToDateTimeString()
    self.assertEqual(date_time_string, '2010-08-12 20:06:31.987654321')

    apfs_time_object = apfs_time.APFSTime()

    date_time_string = apfs_time_object.CopyToDateTimeString()
    self.assertIsNone(date_time_string)

  def testCopyToDateTimeStringISO8601(self):
    """Tests the CopyToDateTimeStringISO8601 function."""
    apfs_time_object = apfs_time.APFSTime(timestamp=1281643591987654321)

    date_time_string = apfs_time_object.CopyToDateTimeStringISO8601()
    self.assertEqual(date_time_string, '2010-08-12T20:06:31.987654321Z')

  def testGetDate(self):
    """Tests the GetDate function."""
    apfs_time_object = apfs_time.APFSTime(timestamp=1281643591987654321)

    date_tuple = apfs_time_object.GetDate()
    self.assertEqual(date_tuple, (2010, 8, 12))

    apfs_time_object = apfs_time.APFSTime()

    date_tuple = apfs_time_object.GetDate()
    self.assertEqual(date_tuple, (None, None, None))

  def testGetTimeOfDay(self):
    """Tests the GetTimeOfDay function."""
    apfs_time_object = apfs_time.APFSTime(timestamp=1281643591987654321)

    time_of_day_tuple = apfs_time_object.GetTimeOfDay()
    self.assertEqual(time_of_day_tuple, (20, 6, 31))

    apfs_time_object = apfs_time.APFSTime()

    time_of_day_tuple = apfs_time_object.GetTimeOfDay()
    self.assertEqual(time_of_day_tuple, (None, None, None))


if __name__ == '__main__':
  unittest.main()
