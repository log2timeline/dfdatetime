# -*- coding: utf-8 -*-
"""Tests for the Golang timestamp implementation."""

import decimal
import struct
import unittest

from dfdatetime import golang_time


class GolangEpochTest(unittest.TestCase):
  """Test for the Golang epoch."""

  def testInitialize(self):
    """Tests the __init__ function."""
    golang_epoch = golang_time.GolangTimeEpoch()
    self.assertIsNotNone(golang_epoch)

  def testEpochDate(self):
    """Tests the Golang epoch properties."""
    golang_epoch = golang_time.GolangTimeEpoch()
    self.assertEqual(golang_epoch.year, 1)
    self.assertEqual(golang_epoch.month, 1)
    self.assertEqual(golang_epoch.day_of_month, 1)


class GolangTest(unittest.TestCase):
  """Tests for the Golang timestamp."""

  # pylint: disable=protected-access

  def testProperties(self):
    """Tests the Golang timestamp properties."""
    timestamp = struct.pack('>Bqih', 1, 0, 0, -1)
    golang_object = golang_time.GolangTime(timestamp)
    self.assertEqual(golang_object._seconds, 0)
    self.assertEqual(golang_object._nanoseconds, 0)
    self.assertEqual(golang_object.is_local_time, False)
    self.assertEqual(golang_object._time_zone_offset, -1)

    timestamp = struct.pack(
        '>Bqih', 1, golang_time.GolangTime._GOLANG_TO_POSIX_BASE, 0, 0)
    golang_object = golang_time.GolangTime(timestamp)
    self.assertEqual(golang_object._seconds,
                     golang_time.GolangTime._GOLANG_TO_POSIX_BASE)
    self.assertEqual(golang_object._nanoseconds, 0)
    self.assertEqual(golang_object.is_local_time, True)
    self.assertEqual(golang_object._time_zone_offset, 0)

    timestamp = bytes.fromhex('010000000e7791f70000000000ffff')
    golang_object = golang_time.GolangTime(timestamp)
    self.assertEqual(golang_object._seconds,
                     golang_time.GolangTime._GOLANG_TO_POSIX_BASE)
    self.assertEqual(golang_object._nanoseconds, 0)
    self.assertEqual(golang_object.is_local_time, False)
    self.assertEqual(golang_object._time_zone_offset, -1)

  def testGetNormalizedTimestamp(self):
    """Test the _GetNormalizedTimestamp function."""
    timestamp = bytes.fromhex('010000000000000000000000000000')
    golang_object = golang_time.GolangTime(timestamp)

    normalized_timestamp = golang_object._GetNormalizedTimestamp()
    self.assertIsNone(normalized_timestamp)

    timestamp = struct.pack('>Bqih', 1, 63772480949, 711098348, 0)
    golang_object = golang_time.GolangTime(timestamp)

    normalized_timestamp = golang_object._GetNormalizedTimestamp()
    self.assertEqual(
        normalized_timestamp, decimal.Decimal('1636884149.711098348')
    )

    timestamp = bytes.fromhex('010000000e7791f70000000000ffff')
    golang_object = golang_time.GolangTime(timestamp)

    normalized_timestamp = golang_object._GetNormalizedTimestamp()
    self.assertEqual(normalized_timestamp, decimal.Decimal('0'))

    timestamp = bytes.fromhex('010000000e7791f60000000000ffff')
    golang_object = golang_time.GolangTime(timestamp)

    normalized_timestamp = golang_object._GetNormalizedTimestamp()
    self.assertIsNone(normalized_timestamp)

  def testCopyFromDateTimeString(self):
    """Tests the CopyFromDateTimeString function."""
    timestamp = bytes.fromhex('010000000000000000000000000000')
    golang_object = golang_time.GolangTime(timestamp)

    golang_object.CopyFromDateTimeString('0001-01-01')
    self.assertEqual(golang_object._seconds, 0)
    self.assertEqual(golang_object._nanoseconds, 0)
    self.assertEqual(golang_object._time_zone_offset, 0)

    golang_object.CopyFromDateTimeString('0001-01-01 00:01:00')
    self.assertEqual(golang_object._seconds, 60)
    self.assertEqual(golang_object._nanoseconds, 0)
    self.assertEqual(golang_object._time_zone_offset, 0)

    golang_object.CopyFromDateTimeString('0001-01-01 00:00:00.000001')
    self.assertEqual(golang_object._seconds, 0)
    self.assertEqual(golang_object._nanoseconds, 1000)
    self.assertEqual(golang_object._time_zone_offset, 0)

    golang_object.CopyFromDateTimeString('2000-01-01')
    self.assertEqual(golang_object._seconds, 63082281600)
    self.assertEqual(golang_object._nanoseconds, 0)
    self.assertEqual(golang_object._time_zone_offset, 0)

    golang_object.CopyFromDateTimeString('2000-01-01 12:23:45.567890')
    self.assertEqual(golang_object._seconds, 63082326225)
    self.assertEqual(golang_object._nanoseconds, 567890000)
    self.assertEqual(golang_object._time_zone_offset, 0)

    golang_object.CopyFromDateTimeString('2000-01-01 12:23:45.567890+01:00')
    self.assertEqual(golang_object._seconds, 63082326225)
    self.assertEqual(golang_object._nanoseconds, 567890000)
    self.assertEqual(golang_object._time_zone_offset, 60)


  def testCopyToDateTimeString(self):
    """Test the CopyToDateTimeString function."""
    timestamp = bytes.fromhex('010000000eafffe8d121d95050ffff')
    golang_object = golang_time.GolangTime(timestamp)
    self.assertEqual(golang_object._seconds, 63082326225)
    self.assertEqual(golang_object._nanoseconds, 567890000)
    self.assertEqual(golang_object._time_zone_offset, -1)

    date_time_string = golang_object.CopyToDateTimeString()
    self.assertEqual(date_time_string, '2000-01-01 12:23:45.567890')

    timestamp = bytes.fromhex('010000000eafffe8d10000ddd5ffff')
    golang_object = golang_time.GolangTime(timestamp)
    self.assertEqual(golang_object._seconds, 63082326225)
    self.assertEqual(golang_object._nanoseconds, 56789)
    self.assertEqual(golang_object._time_zone_offset, -1)

    date_time_string = golang_object.CopyToDateTimeString()
    self.assertEqual(date_time_string, '2000-01-01 12:23:45.000056')
