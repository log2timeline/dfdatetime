#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the Delphi TDateTime implementation."""

from __future__ import unicode_literals

import unittest

from dfdatetime import delphi_date_time


class DelphiDateTimeEpochTest(unittest.TestCase):
  """Tests for the Delphi TDateTime epoch."""

  def testInitialize(self):
    """Tests the __init__ function."""
    delphi_date_time_epoch = delphi_date_time.DelphiDateTimeEpoch()
    self.assertIsNotNone(delphi_date_time_epoch)


class DelphiDateTimeInvalidYear(delphi_date_time.DelphiDateTime):
  """Delphi TDateTime timestamp for testing invalid year."""

  def _CopyDateTimeFromString(self, unused_time_string):
    """Copies a date and time from a string.

    Args:
      time_string (str): date and time value formatted as:
          YYYY-MM-DD hh:mm:ss.######[+-]##:##

          Where # are numeric digits ranging from 0 to 9 and the seconds
          fraction can be either 3 or 6 digits. The time of day, seconds
          fraction and time zone offset are optional. The default time zone
          is UTC.

    Returns:
      dict[str, int]: date and time values, such as year, month, day of month,
          hours, minutes, seconds, microseconds.

    Raises:
      ValueError: if the time string is invalid or not supported.
    """
    return {
        'year': 10000,
        'month': 1,
        'day_of_month': 2,
        'hours': 0,
        'minutes': 0,
        'seconds': 0}


class DelphiDateTimeTest(unittest.TestCase):
  """Tests for the Delphi TDateTime timestamp."""

  # pylint: disable=protected-access

  def testCopyFromDateTimeString(self):
    """Tests the CopyFromDateTimeString function."""
    delphi_date_time_object = delphi_date_time.DelphiDateTime()

    expected_timestamp = 41443.0
    delphi_date_time_object.CopyFromDateTimeString('2013-06-18')
    self.assertEqual(delphi_date_time_object.timestamp, expected_timestamp)

    expected_timestamp = 41443.82638888889
    delphi_date_time_object.CopyFromDateTimeString('2013-06-18 19:50:00')
    self.assertEqual(delphi_date_time_object.timestamp, expected_timestamp)

    expected_timestamp = 41443.826395218464
    delphi_date_time_object.CopyFromDateTimeString('2013-06-18 19:50:00.546875')
    self.assertEqual(delphi_date_time_object.timestamp, expected_timestamp)

    expected_timestamp = 41443.86806188513
    delphi_date_time_object.CopyFromDateTimeString(
        '2013-06-18 19:50:00.546875-01:00')
    self.assertEqual(delphi_date_time_object.timestamp, expected_timestamp)

    expected_timestamp = 41443.78472855179
    delphi_date_time_object.CopyFromDateTimeString(
        '2013-06-18 19:50:00.546875+01:00')
    self.assertEqual(delphi_date_time_object.timestamp, expected_timestamp)

    expected_timestamp = 1.0
    delphi_date_time_object.CopyFromDateTimeString('1899-12-31 00:00:00')
    self.assertEqual(delphi_date_time_object.timestamp, expected_timestamp)

    delphi_date_time_object = DelphiDateTimeInvalidYear()

    with self.assertRaises(ValueError):
      delphi_date_time_object.CopyFromDateTimeString('9999-01-02 00:00:00')

  def testCopyToStatTimeTuple(self):
    """Tests the CopyToStatTimeTuple function."""
    delphi_date_time_object = delphi_date_time.DelphiDateTime(
        timestamp=41443.8263953)

    stat_time_tuple = delphi_date_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, (1371585000, 5539197))

    delphi_date_time_object = delphi_date_time.DelphiDateTime()

    stat_time_tuple = delphi_date_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, (None, None))

  def testCopyToDateTimeString(self):
    """Tests the CopyToDateTimeString function."""
    delphi_date_time_object = delphi_date_time.DelphiDateTime(
        timestamp=41443.8263953)

    date_time_string = delphi_date_time_object.CopyToDateTimeString()
    self.assertEqual(date_time_string, '2013-06-18 19:50:00.553919')

    delphi_date_time_object = delphi_date_time.DelphiDateTime()

    date_time_string = delphi_date_time_object.CopyToDateTimeString()
    self.assertIsNone(date_time_string)

  def testGetDate(self):
    """Tests the GetDate function."""
    delphi_date_time_object = delphi_date_time.DelphiDateTime(
        timestamp=41443.8263953)

    date_tuple = delphi_date_time_object.GetDate()
    self.assertEqual(date_tuple, (2013, 6, 18))

    delphi_date_time_object._EPOCH.year = -1

    date_tuple = delphi_date_time_object.GetDate()
    self.assertEqual(date_tuple, (None, None, None))

    delphi_date_time_object = delphi_date_time.DelphiDateTime()

    date_tuple = delphi_date_time_object.GetDate()
    self.assertEqual(date_tuple, (None, None, None))

  def testGetPlasoTimestamp(self):
    """Tests the GetPlasoTimestamp function."""
    delphi_date_time_object = delphi_date_time.DelphiDateTime(
        timestamp=41443.8263953)

    micro_posix_timestamp = delphi_date_time_object.GetPlasoTimestamp()
    self.assertEqual(micro_posix_timestamp, 1371585000553920)

    delphi_date_time_object = delphi_date_time.DelphiDateTime()

    micro_posix_timestamp = delphi_date_time_object.GetPlasoTimestamp()
    self.assertIsNone(micro_posix_timestamp)


if __name__ == '__main__':
  unittest.main()
