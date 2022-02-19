#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for the .NET DateTime implementation."""

import decimal
import unittest

from dfdatetime import dotnet_datetime


class DotNetDateTimeEpochTest(unittest.TestCase):
  """Tests for the .NET DateTime epoch."""

  def testInitialize(self):
    """Tests the __init__ function."""
    dotnet_date_time_epoch = dotnet_datetime.DotNetDateTimeEpoch()
    self.assertIsNotNone(dotnet_date_time_epoch)


class DotNetDateTimeTest(unittest.TestCase):
  """Tests for the ,NET DateTime timestamp."""

  # pylint: disable=protected-access

  def testProperties(self):
    """Tests the properties."""
    dotnet_date_time = dotnet_datetime.DotNetDateTime()
    self.assertEqual(dotnet_date_time.timestamp, 0)

    dotnet_date_time = dotnet_datetime.DotNetDateTime(
        timestamp=637751130027210000)
    self.assertEqual(dotnet_date_time.timestamp, 637751130027210000)

  def testGetNormalizedTimestamp(self):
    """Tests the _GetNormalizedTimestamp function."""
    dotnet_date_time = dotnet_datetime.DotNetDateTime(
        timestamp=637433719321230000)
    expected_normalized_timestamp = decimal.Decimal(1607775132123) / 1000
    normalized_timestamp = dotnet_date_time._GetNormalizedTimestamp()
    self.assertEqual(normalized_timestamp, expected_normalized_timestamp)

  def testCopyFromDateTimeString(self):
    """Tests the CopyFromDateTimeString function."""
    dotnet_date_time = dotnet_datetime.DotNetDateTime()

    dotnet_date_time.CopyFromDateTimeString('2020-12-12')
    self.assertEqual(dotnet_date_time._timestamp, 637433280000000000)
    self.assertEqual(dotnet_date_time._time_zone_offset, 0)

    dotnet_date_time.CopyFromDateTimeString('2020-12-12 12:12:12')
    self.assertEqual(dotnet_date_time._timestamp, 637433719320000000)
    self.assertEqual(dotnet_date_time._time_zone_offset, 0)

    dotnet_date_time.CopyFromDateTimeString('2020-12-12 12:12:12.123')
    self.assertEqual(dotnet_date_time._timestamp, 637433719321230000)
    self.assertEqual(dotnet_date_time._time_zone_offset, 0)

  def testCopyToDateTimeString(self):
    """Tests the CopyToDateTimeString function."""
    dotnet_date_time = dotnet_datetime.DotNetDateTime(
        timestamp=637433280000000000)

    dotnet_date_string = dotnet_date_time.CopyToDateTimeString()
    self.assertEqual(dotnet_date_string, '2020-12-12 00:00:00.0000000')

    dotnet_date_time = dotnet_datetime.DotNetDateTime(
        timestamp=637433719320000000)

    dotnet_date_string = dotnet_date_time.CopyToDateTimeString()
    self.assertEqual(dotnet_date_string, '2020-12-12 12:12:12.0000000')

    dotnet_date_time = dotnet_datetime.DotNetDateTime(
        timestamp=637433719321230000)

    dotnet_date_string = dotnet_date_time.CopyToDateTimeString()
    self.assertEqual(dotnet_date_string, '2020-12-12 12:12:12.1230000')


if __name__ == '__main__':
  unittest.main()
