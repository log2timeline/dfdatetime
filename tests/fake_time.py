#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the fake time implementation."""

from __future__ import unicode_literals

import unittest

from dfdatetime import fake_time


class FakeTimeTest(unittest.TestCase):
  """Tests for the fake time."""

  # pylint: disable=protected-access

  def testCopyFromDateTimeString(self):
    """Tests the CopyFromDateTimeString function."""
    fake_time_object = fake_time.FakeTime()

    expected_number_of_seconds = 1281571200
    fake_time_object.CopyFromDateTimeString('2010-08-12')
    self.assertEqual(
        fake_time_object._number_of_seconds, expected_number_of_seconds)
    self.assertIsNone(fake_time_object._microseconds)

    expected_number_of_seconds = 1281647191
    fake_time_object.CopyFromDateTimeString('2010-08-12 21:06:31')
    self.assertEqual(
        fake_time_object._number_of_seconds, expected_number_of_seconds)
    self.assertIsNone(fake_time_object._microseconds)

    expected_number_of_seconds = 1281647191
    fake_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875')
    self.assertEqual(
        fake_time_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(fake_time_object._microseconds, 546875)

    expected_number_of_seconds = 1281650791
    fake_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875-01:00')
    self.assertEqual(
        fake_time_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(fake_time_object._microseconds, 546875)

    expected_number_of_seconds = 1281643591
    fake_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875+01:00')
    self.assertEqual(
        fake_time_object._number_of_seconds, expected_number_of_seconds)
    self.assertEqual(fake_time_object._microseconds, 546875)

    expected_number_of_seconds = -11644387200
    fake_time_object.CopyFromDateTimeString('1601-01-02 00:00:00')
    self.assertEqual(
        fake_time_object._number_of_seconds, expected_number_of_seconds)
    self.assertIsNone(fake_time_object._microseconds)

  def testCopyToStatTimeTuple(self):
    """Tests the CopyToStatTimeTuple function."""
    fake_time_object = fake_time.FakeTime()
    fake_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875')

    expected_stat_time_tuple = (1281647191, 5468750)
    stat_time_tuple = fake_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, expected_stat_time_tuple)

    fake_time_object = fake_time.FakeTime()
    fake_time_object.CopyFromDateTimeString('2010-08-12 21:06:31')

    expected_stat_time_tuple = (1281647191, None)
    stat_time_tuple = fake_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, expected_stat_time_tuple)

    fake_time_object = fake_time.FakeTime()
    fake_time_object._number_of_seconds = None

    expected_stat_time_tuple = (None, None)
    stat_time_tuple = fake_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, expected_stat_time_tuple)

  def testCopyToDateTimeString(self):
    """Tests the CopyToDateTimeString function."""
    fake_time_object = fake_time.FakeTime()
    fake_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875')

    date_time_string = fake_time_object.CopyToDateTimeString()
    self.assertEqual(date_time_string, '2010-08-12 21:06:31.546875')

    fake_time_object = fake_time.FakeTime()
    fake_time_object._number_of_seconds = None

    date_time_string = fake_time_object.CopyToDateTimeString()
    self.assertIsNone(date_time_string)

  def testGetDate(self):
    """Tests the GetDate function."""
    fake_time_object = fake_time.FakeTime()
    fake_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875')

    date_tuple = fake_time_object.GetDate()
    self.assertEqual(date_tuple, (2010, 8, 12))

    fake_time_object._EPOCH.year = -1

    date_tuple = fake_time_object.GetDate()
    self.assertEqual(date_tuple, (None, None, None))

    fake_time_object = fake_time.FakeTime()

    date_tuple = fake_time_object.GetDate()
    self.assertEqual(date_tuple, (None, None, None))

  def testGetPlasoTimestamp(self):
    """Tests the GetPlasoTimestamp function."""
    fake_time_object = fake_time.FakeTime()
    fake_time_object.CopyFromDateTimeString('2010-08-12 21:06:31.546875')

    expected_micro_posix_number_of_seconds = 1281647191546875
    micro_posix_number_of_seconds = fake_time_object.GetPlasoTimestamp()
    self.assertEqual(
        micro_posix_number_of_seconds, expected_micro_posix_number_of_seconds)

    fake_time_object = fake_time.FakeTime()
    fake_time_object.CopyFromDateTimeString('2010-08-12 21:06:31')

    expected_micro_posix_number_of_seconds = 1281647191000000
    micro_posix_number_of_seconds = fake_time_object.GetPlasoTimestamp()
    self.assertEqual(
        micro_posix_number_of_seconds, expected_micro_posix_number_of_seconds)

    fake_time_object = fake_time.FakeTime()
    fake_time_object._number_of_seconds = None

    micro_posix_number_of_seconds = fake_time_object.GetPlasoTimestamp()
    self.assertIsNone(micro_posix_number_of_seconds)


if __name__ == '__main__':
  unittest.main()
