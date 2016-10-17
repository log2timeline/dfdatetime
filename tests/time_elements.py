#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the time elements implementation."""

import unittest

from dfdatetime import time_elements


class TimeElementsTimeTest(unittest.TestCase):
  """Tests for the time elements."""

  # pylint: disable=protected-access

  def testCopyFromString(self):
    """Tests the CopyFromString function."""
    time_elements_object = time_elements.TimeElements()

    expected_time_elements_tuple = (2010, 8, 12, 0, 0, 0)
    expected_number_of_seconds = 1281571200
    time_elements_object.CopyFromString(u'2010-08-12')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    expected_number_of_seconds = 1281647191
    time_elements_object.CopyFromString(u'2010-08-12 21:06:31')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    expected_number_of_seconds = 1281647191
    time_elements_object.CopyFromString(u'2010-08-12 21:06:31.546875')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)

    expected_time_elements_tuple = (2010, 8, 12, 22, 6, 31)
    expected_number_of_seconds = 1281650791
    time_elements_object.CopyFromString(u'2010-08-12 21:06:31.546875-01:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)

    expected_time_elements_tuple = (2010, 8, 12, 20, 6, 31)
    expected_number_of_seconds = 1281643591
    time_elements_object.CopyFromString(u'2010-08-12 21:06:31.546875+01:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)

    expected_time_elements_tuple = (1601, 1, 2, 0, 0, 0)
    expected_number_of_seconds = -11644387200
    time_elements_object.CopyFromString(u'1601-01-02 00:00:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)

  def testCopyFromStringISO8601(self):
    """Tests the CopyFromStringISO8601 function."""
    time_elements_object = time_elements.TimeElements()

    expected_time_elements_tuple = (2010, 8, 12, 0, 0, 0)
    expected_number_of_seconds = 1281571200
    time_elements_object.CopyFromStringISO8601(u'2010-08-12')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    expected_number_of_seconds = 1281647191
    time_elements_object.CopyFromStringISO8601(u'2010-08-12T21:06:31')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    expected_number_of_seconds = 1281647191
    time_elements_object.CopyFromStringISO8601(u'2010-08-12T21:06:31Z')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    expected_number_of_seconds = 1281647191
    time_elements_object.CopyFromStringISO8601(u'2010-08-12T21:06:31.546875')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31)
    expected_number_of_seconds = 1281647191
    time_elements_object.CopyFromStringISO8601(u'2010-08-12T21:06:31,546875')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)

    expected_time_elements_tuple = (2010, 8, 12, 22, 6, 31)
    expected_number_of_seconds = 1281650791
    time_elements_object.CopyFromStringISO8601(
        u'2010-08-12T21:06:31.546875-01:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)

    expected_time_elements_tuple = (2010, 8, 12, 20, 6, 31)
    expected_number_of_seconds = 1281643591
    time_elements_object.CopyFromStringISO8601(
        u'2010-08-12T21:06:31.546875+01:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)

    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringISO8601(None)

    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringISO8601(
          u'2010-08-12 21:06:31.546875+01:00')

    # Valid ISO 8601 notations currently not supported.
    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringISO8601(u'2016-W33')

    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringISO8601(u'2016-W33-3')

    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringISO8601(u'--08-17')

    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringISO8601(u'2016-230')

    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringISO8601(u'2010-08-12T21:06:31.5')

  def testCopyToStatTimeTuple(self):
    """Tests the CopyToStatTimeTuple function."""
    time_elements_object = time_elements.TimeElements(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31))

    expected_stat_time_tuple = (1281643591, None)
    stat_time_tuple = time_elements_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, expected_stat_time_tuple)

    time_elements_object = time_elements.TimeElements()

    expected_stat_time_tuple = (None, None)
    stat_time_tuple = time_elements_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, expected_stat_time_tuple)

  def testGetPlasoTimestamp(self):
    """Tests the GetPlasoTimestamp function."""
    time_elements_object = time_elements.TimeElements(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31))

    expected_micro_posix_number_of_seconds = 1281643591000000
    micro_posix_number_of_seconds = time_elements_object.GetPlasoTimestamp()
    self.assertEqual(
        micro_posix_number_of_seconds, expected_micro_posix_number_of_seconds)

    time_elements_object = time_elements.TimeElements()

    micro_posix_number_of_seconds = time_elements_object.GetPlasoTimestamp()
    self.assertIsNone(micro_posix_number_of_seconds)


if __name__ == '__main__':
  unittest.main()
