#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the POSIX timestamp implementation."""

import unittest

from dfdatetime import posix_time


class PosixTimeTest(unittest.TestCase):
  """Tests for the POSIX timestamp."""

  def testCopyFromString(self):
    """Tests the CopyFromString function."""
    posix_time_object = posix_time.PosixTime()

    expected_timestamp = 1281571200
    posix_time_object.CopyFromString(u'2010-08-12')
    self.assertEqual(posix_time_object.timestamp, expected_timestamp)
    self.assertIsNone(posix_time_object.microseconds)

    expected_timestamp = 1281647191
    posix_time_object.CopyFromString(u'2010-08-12 21:06:31')
    self.assertEqual(posix_time_object.timestamp, expected_timestamp)
    self.assertIsNone(posix_time_object.microseconds)

    expected_timestamp = 1281647191
    posix_time_object.CopyFromString(u'2010-08-12 21:06:31.546875')
    self.assertEqual(posix_time_object.timestamp, expected_timestamp)
    self.assertEqual(posix_time_object.microseconds, 546875)

    expected_timestamp = 1281650791
    posix_time_object.CopyFromString(u'2010-08-12 21:06:31.546875-01:00')
    self.assertEqual(posix_time_object.timestamp, expected_timestamp)
    self.assertEqual(posix_time_object.microseconds, 546875)

    expected_timestamp = 1281643591
    posix_time_object.CopyFromString(u'2010-08-12 21:06:31.546875+01:00')
    self.assertEqual(posix_time_object.timestamp, expected_timestamp)
    self.assertEqual(posix_time_object.microseconds, 546875)

    expected_timestamp = -11644387200
    posix_time_object.CopyFromString(u'1601-01-02 00:00:00')
    self.assertEqual(posix_time_object.timestamp, expected_timestamp)
    self.assertIsNone(posix_time_object.microseconds)

  def testCopyToStatTimeTuple(self):
    """Tests the CopyToStatTimeTuple function."""
    posix_time_object = posix_time.PosixTime(
        microseconds=546875, timestamp=1281643591)

    expected_stat_time_tuple = (1281643591, 5468750)
    stat_time_tuple = posix_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, expected_stat_time_tuple)

    posix_time_object = posix_time.PosixTime(timestamp=1281643591)

    expected_stat_time_tuple = (1281643591, None)
    stat_time_tuple = posix_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, expected_stat_time_tuple)

    posix_time_object = posix_time.PosixTime()

    expected_stat_time_tuple = (None, None)
    stat_time_tuple = posix_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, expected_stat_time_tuple)

  def testGetPlasoTimestamp(self):
    """Tests the GetPlasoTimestamp function."""
    posix_time_object = posix_time.PosixTime(
        microseconds=546875, timestamp=1281643591)

    expected_micro_posix_timestamp = 1281643591546875
    micro_posix_timestamp = posix_time_object.GetPlasoTimestamp()
    self.assertEqual(micro_posix_timestamp, expected_micro_posix_timestamp)

    posix_time_object = posix_time.PosixTime(timestamp=1281643591)

    expected_micro_posix_timestamp = 1281643591000000
    micro_posix_timestamp = posix_time_object.GetPlasoTimestamp()
    self.assertEqual(micro_posix_timestamp, expected_micro_posix_timestamp)

    posix_time_object = posix_time.PosixTime()

    micro_posix_timestamp = posix_time_object.GetPlasoTimestamp()
    self.assertIsNone(micro_posix_timestamp)


if __name__ == '__main__':
  unittest.main()
