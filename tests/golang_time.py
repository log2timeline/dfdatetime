# -*- coding: utf-8 -*-
"""Tests for the Golang time.Time timestamp implementation."""

import decimal
import struct
import unittest

from dfdatetime import golang_time


class GolangEpochTest(unittest.TestCase):
  """Test for the Golang time.Time epoch."""

  def testInitialize(self):
    """Tests the __init__ function."""
    golang_epoch = golang_time.GolangTimeEpoch()
    self.assertIsNotNone(golang_epoch)

  def testEpochDate(self):
    """Tests the Golang time.Time epoch properties."""
    golang_epoch = golang_time.GolangTimeEpoch()
    self.assertEqual(golang_epoch.year, 1)
    self.assertEqual(golang_epoch.month, 1)
    self.assertEqual(golang_epoch.day_of_month, 1)


class GolangTest(unittest.TestCase):
  """Tests for the Golang time.Time timestamp."""

  # pylint: disable=protected-access

  def testProperties(self):
    """Tests the Golang time.Time timestamp properties."""
    golang_timestamp = struct.pack('>Bqih', 1, 0, 0, -1)
    golang_time_object = golang_time.GolangTime(
        golang_timestamp=golang_timestamp)
    self.assertEqual(golang_time_object._number_of_seconds, 0)
    self.assertEqual(golang_time_object._nanoseconds, 0)
    self.assertEqual(golang_time_object.is_local_time, False)
    self.assertEqual(golang_time_object._time_zone_offset, 0)

    golang_timestamp = struct.pack(
        '>Bqih', 1, golang_time.GolangTime._GOLANG_TO_POSIX_BASE, 0, 1)
    golang_time_object = golang_time.GolangTime(
        golang_timestamp=golang_timestamp)
    self.assertEqual(golang_time_object._number_of_seconds,
                     golang_time.GolangTime._GOLANG_TO_POSIX_BASE)
    self.assertEqual(golang_time_object._nanoseconds, 0)
    self.assertEqual(golang_time_object.is_local_time, True)
    self.assertEqual(golang_time_object._time_zone_offset, 1)

    golang_timestamp = bytes.fromhex('010000000e7791f70000000000ffff')
    golang_time_object = golang_time.GolangTime(
        golang_timestamp=golang_timestamp)
    self.assertEqual(golang_time_object._number_of_seconds,
                     golang_time.GolangTime._GOLANG_TO_POSIX_BASE)
    self.assertEqual(golang_time_object._nanoseconds, 0)
    self.assertEqual(golang_time_object.is_local_time, False)
    self.assertEqual(golang_time_object._time_zone_offset, 0)

  def testGetNormalizedTimestamp(self):
    """Test the _GetNormalizedTimestamp function."""
    golang_timestamp = bytes.fromhex('010000000000000000000000000000')
    golang_time_object = golang_time.GolangTime(
        golang_timestamp=golang_timestamp)

    normalized_timestamp = golang_time_object._GetNormalizedTimestamp()
    self.assertIsNone(normalized_timestamp)

    golang_timestamp = struct.pack('>Bqih', 1, 63772480949, 711098348, 0)
    golang_time_object = golang_time.GolangTime(
        golang_timestamp=golang_timestamp)

    normalized_timestamp = golang_time_object._GetNormalizedTimestamp()
    self.assertEqual(
        normalized_timestamp, decimal.Decimal('1636884149.711098348'))

    golang_timestamp = bytes.fromhex('010000000e7791f70000000000ffff')
    golang_time_object = golang_time.GolangTime(
        golang_timestamp=golang_timestamp)

    normalized_timestamp = golang_time_object._GetNormalizedTimestamp()
    self.assertEqual(normalized_timestamp, decimal.Decimal('0'))

    golang_timestamp = bytes.fromhex('010000000e7791f60000000000ffff')
    golang_time_object = golang_time.GolangTime(
        golang_timestamp=golang_timestamp)

    normalized_timestamp = golang_time_object._GetNormalizedTimestamp()
    self.assertIsNone(normalized_timestamp)

  def testGetNumberOfSeconds(self):
    """Test the _GetNumberOfSeconds function."""
    golang_time_object = golang_time.GolangTime()

    golang_timestamp = bytes.fromhex('010000000000000002000000030004')
    number_of_seconds, nanoseconds, time_zone_offset = (
        golang_time_object._GetNumberOfSeconds(golang_timestamp))
    self.assertEqual(number_of_seconds, 2)
    self.assertEqual(nanoseconds, 3)
    self.assertEqual(time_zone_offset, 4)

    golang_timestamp = bytes.fromhex('02000000000000000500000006ffff08')
    number_of_seconds, nanoseconds, time_zone_offset = (
        golang_time_object._GetNumberOfSeconds(golang_timestamp))
    self.assertEqual(number_of_seconds, 5)
    self.assertEqual(nanoseconds, 6)
    self.assertEqual(time_zone_offset, 0)

    with self.assertRaises(ValueError):
      golang_timestamp = bytes.fromhex('0100')
      golang_time_object._GetNumberOfSeconds(golang_timestamp)

    with self.assertRaises(ValueError):
      golang_timestamp = bytes.fromhex('020000000000000000000000000000')
      golang_time_object._GetNumberOfSeconds(golang_timestamp)

    with self.assertRaises(ValueError):
      golang_timestamp = bytes.fromhex('ff0000000000000000000000000000')
      golang_time_object._GetNumberOfSeconds(golang_timestamp)

  def testCopyFromDateTimeString(self):
    """Tests the CopyFromDateTimeString function."""
    golang_time_object = golang_time.GolangTime()

    golang_time_object.CopyFromDateTimeString('0001-01-01')
    self.assertEqual(golang_time_object._number_of_seconds, 0)
    self.assertEqual(golang_time_object._nanoseconds, 0)
    self.assertEqual(golang_time_object._time_zone_offset, 0)

    golang_time_object.CopyFromDateTimeString('0001-01-01 00:01:00')
    self.assertEqual(golang_time_object._number_of_seconds, 60)
    self.assertEqual(golang_time_object._nanoseconds, 0)
    self.assertEqual(golang_time_object._time_zone_offset, 0)

    golang_time_object.CopyFromDateTimeString('0001-01-01 00:00:00.000001')
    self.assertEqual(golang_time_object._number_of_seconds, 0)
    self.assertEqual(golang_time_object._nanoseconds, 1000)
    self.assertEqual(golang_time_object._time_zone_offset, 0)

    golang_time_object.CopyFromDateTimeString('2000-01-01')
    self.assertEqual(golang_time_object._number_of_seconds, 63082281600)
    self.assertEqual(golang_time_object._nanoseconds, 0)
    self.assertEqual(golang_time_object._time_zone_offset, 0)

    golang_time_object.CopyFromDateTimeString('2000-01-01 12:23:45.567890')
    self.assertEqual(golang_time_object._number_of_seconds, 63082326225)
    self.assertEqual(golang_time_object._nanoseconds, 567890000)
    self.assertEqual(golang_time_object._time_zone_offset, 0)

    golang_time_object.CopyFromDateTimeString(
        '2000-01-01 12:23:45.567890+01:00')
    self.assertEqual(golang_time_object._number_of_seconds, 63082326225)
    self.assertEqual(golang_time_object._nanoseconds, 567890000)
    self.assertEqual(golang_time_object._time_zone_offset, 60)

  def testCopyToDateTimeString(self):
    """Test the CopyToDateTimeString function."""
    golang_timestamp = bytes.fromhex('010000000eafffe8d121d95050ffff')
    golang_time_object = golang_time.GolangTime(
        golang_timestamp=golang_timestamp)

    self.assertEqual(golang_time_object._number_of_seconds, 63082326225)
    self.assertEqual(golang_time_object._nanoseconds, 567890000)
    self.assertEqual(golang_time_object._time_zone_offset, 0)

    date_time_string = golang_time_object.CopyToDateTimeString()
    self.assertEqual(date_time_string, '2000-01-01 12:23:45.567890000')

    golang_timestamp = bytes.fromhex('010000000eafffe8d10000ddd5ffff')
    golang_time_object = golang_time.GolangTime(
        golang_timestamp=golang_timestamp)

    self.assertEqual(golang_time_object._number_of_seconds, 63082326225)
    self.assertEqual(golang_time_object._nanoseconds, 56789)
    self.assertEqual(golang_time_object._time_zone_offset, 0)

    date_time_string = golang_time_object.CopyToDateTimeString()
    self.assertEqual(date_time_string, '2000-01-01 12:23:45.000056789')
