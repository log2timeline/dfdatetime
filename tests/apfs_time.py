#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for the APFS timestamp implementation."""

import decimal
import unittest

from dfdatetime import apfs_time


class APFSTimeTest(unittest.TestCase):
  """Tests for the APFS timestamp."""

  # pylint: disable=protected-access

  def testGetNormalizedTimestamp(self):
    """Tests the _GetNormalizedTimestamp function."""
    apfs_time_object = apfs_time.APFSTime(timestamp=1281643591987654321)

    normalized_timestamp = apfs_time_object._GetNormalizedTimestamp()
    self.assertEqual(
        normalized_timestamp, decimal.Decimal('1281643591.987654321'))

    apfs_time_object = apfs_time.APFSTime(
        time_zone_offset=60, timestamp=1281643591987654321)

    normalized_timestamp = apfs_time_object._GetNormalizedTimestamp()
    self.assertEqual(
        normalized_timestamp, decimal.Decimal('1281639991.987654321'))

    apfs_time_object = apfs_time.APFSTime()

    normalized_timestamp = apfs_time_object._GetNormalizedTimestamp()
    self.assertIsNone(normalized_timestamp)

    apfs_time_object = apfs_time.APFSTime(timestamp=9223372036854775810)

    date_time_string = apfs_time_object._GetNormalizedTimestamp()
    self.assertIsNone(date_time_string)

  def testCopyFromDateTimeString(self):
    """Tests the CopyFromDateTimeString function."""
    apfs_time_object = apfs_time.APFSTime()
    with self.assertRaises(ValueError):
      apfs_time_object.CopyFromDateTimeString('2554-07-21 23:34:34.000000')

  def testCopyToDateTimeString(self):
    """Tests the CopyToDateTimeString function."""
    apfs_time_object = apfs_time.APFSTime(timestamp=9223372036854775810)

    date_time_string = apfs_time_object.CopyToDateTimeString()
    self.assertIsNone(date_time_string)

    apfs_time_object = apfs_time.APFSTime()

    date_time_string = apfs_time_object.CopyToDateTimeString()
    self.assertIsNone(date_time_string)


if __name__ == '__main__':
  unittest.main()
