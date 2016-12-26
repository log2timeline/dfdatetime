#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the Delphi TDateTime timestamp implementation."""

import unittest

from dfdatetime import delphi_date_time


class DelphiDateTimeTest(unittest.TestCase):
  """Tests for the Delphi TDateTime timestamp."""

  def testCopyFromString(self):
    """Tests the CopyFromString function."""
    delphi_date_time_object = delphi_date_time.DelphiDateTime()

    expected_timestamp = 41443.0
    delphi_date_time_object.CopyFromString(u'2013-06-18')
    self.assertEqual(delphi_date_time_object.timestamp, expected_timestamp)

    expected_timestamp = 41443.82638888889
    delphi_date_time_object.CopyFromString(u'2013-06-18 19:50:00')
    self.assertEqual(delphi_date_time_object.timestamp, expected_timestamp)

    expected_timestamp = 41443.826395218464
    delphi_date_time_object.CopyFromString(u'2013-06-18 19:50:00.546875')
    self.assertEqual(delphi_date_time_object.timestamp, expected_timestamp)

    expected_timestamp = 41443.86806188513
    delphi_date_time_object.CopyFromString(u'2013-06-18 19:50:00.546875-01:00')
    self.assertEqual(delphi_date_time_object.timestamp, expected_timestamp)

    expected_timestamp = 41443.78472855179
    delphi_date_time_object.CopyFromString(u'2013-06-18 19:50:00.546875+01:00')
    self.assertEqual(delphi_date_time_object.timestamp, expected_timestamp)

    expected_timestamp = 1.0
    delphi_date_time_object.CopyFromString(u'1899-12-31 00:00:00')
    self.assertEqual(delphi_date_time_object.timestamp, expected_timestamp)

    with self.assertRaises(ValueError):
      delphi_date_time_object.CopyFromString(u'10000-01-01 00:00:00')

  def testCopyToStatTimeTuple(self):
    """Tests the CopyToStatTimeTuple function."""
    delphi_date_time_object = delphi_date_time.DelphiDateTime(
        timestamp=41443.8263953)

    expected_stat_time_tuple = (1371585000, 5539197)
    stat_time_tuple = delphi_date_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, expected_stat_time_tuple)

    delphi_date_time_object = delphi_date_time.DelphiDateTime()

    expected_stat_time_tuple = (None, None)
    stat_time_tuple = delphi_date_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, expected_stat_time_tuple)

  def testGetPlasoTimestamp(self):
    """Tests the GetPlasoTimestamp function."""
    delphi_date_time_object = delphi_date_time.DelphiDateTime(
        timestamp=41443.8263953)

    expected_micro_posix_timestamp = 1371585000553920
    micro_posix_timestamp = delphi_date_time_object.GetPlasoTimestamp()
    self.assertEqual(micro_posix_timestamp, expected_micro_posix_timestamp)

    delphi_date_time_object = delphi_date_time.DelphiDateTime()

    micro_posix_timestamp = delphi_date_time_object.GetPlasoTimestamp()
    self.assertIsNone(micro_posix_timestamp)


if __name__ == '__main__':
  unittest.main()
