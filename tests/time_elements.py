#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the time elements implementation."""

import unittest

from dfdatetime import time_elements


class TimeElementsTest(unittest.TestCase):
  """Tests for the time elements."""

  # pylint: disable=protected-access

  def testInitialize(self):
    """Tests the initialization function."""
    time_elements_object = time_elements.TimeElements()
    self.assertIsNotNone(time_elements_object)

    expected_time_elements_tuple = (2010, 8, 12, 20, 6, 31)
    time_elements_object = time_elements.TimeElements(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31))
    self.assertIsNotNone(time_elements_object)
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)

    with self.assertRaises(ValueError):
      time_elements.TimeElements(
          time_elements_tuple=(2010, 8, 12, 20, 6))

    with self.assertRaises(ValueError):
      time_elements.TimeElements(
          time_elements_tuple=(2010, 13, 12, 20, 6, 31))

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

  def testCopyFromStringTuple(self):
    """Tests the CopyFromStringTuple function."""
    time_elements_object = time_elements.TimeElements()

    expected_time_elements_tuple = (2010, 8, 12, 20, 6, 31)
    time_elements_object.CopyFromStringTuple(
        time_elements_tuple=(u'2010', u'8', u'12', u'20', u'6', u'31'))
    self.assertIsNotNone(time_elements_object)
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)

    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringTuple(
          time_elements_tuple=(u'2010', u'8', u'12', u'20', u'6'))

    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringTuple(
          time_elements_tuple=(u'20A0', u'B', u'12', u'20', u'6', u'31'))

    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringTuple(
          time_elements_tuple=(u'2010', u'B', u'12', u'20', u'6', u'31'))

    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringTuple(
          time_elements_tuple=(u'2010', u'8', u'1C', u'20', u'6', u'31'))

    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringTuple(
          time_elements_tuple=(u'2010', u'8', u'12', u'D0', u'6', u'31'))

    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringTuple(
          time_elements_tuple=(u'2010', u'8', u'12', u'20', u'E', u'31'))

    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringTuple(
          time_elements_tuple=(u'2010', u'8', u'12', u'20', u'6', u'F1'))

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


class TimeElementsInMillisecondsTest(unittest.TestCase):
  """Tests for the time elements in milliseconds."""

  # pylint: disable=protected-access

  def testInitialize(self):
    """Tests the initialization function."""
    time_elements_object = time_elements.TimeElements()
    self.assertIsNotNone(time_elements_object)

    expected_time_elements_tuple = (2010, 8, 12, 20, 6, 31)
    time_elements_object = time_elements.TimeElementsInMilliseconds(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31, 546))
    self.assertIsNotNone(time_elements_object)
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._milliseconds, 546)

    with self.assertRaises(ValueError):
      time_elements.TimeElementsInMilliseconds(
          time_elements_tuple=(2010, 13, 12, 20, 6, 31))

    with self.assertRaises(ValueError):
      time_elements.TimeElementsInMilliseconds(
          time_elements_tuple=(2010, 13, 12, 20, 6, 31, 1001))

  def testCopyFromString(self):
    """Tests the CopyFromString function."""
    time_elements_object = time_elements.TimeElementsInMilliseconds()

    expected_time_elements_tuple = (2010, 8, 12, 0, 0, 0, 0)
    expected_number_of_seconds = 1281571200
    time_elements_object.CopyFromString(u'2010-08-12')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31, 0)
    expected_number_of_seconds = 1281647191
    time_elements_object.CopyFromString(u'2010-08-12 21:06:31')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31, 546)
    expected_number_of_seconds = 1281647191
    time_elements_object.CopyFromString(u'2010-08-12 21:06:31.546875')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)

    expected_time_elements_tuple = (2010, 8, 12, 22, 6, 31, 546)
    expected_number_of_seconds = 1281650791
    time_elements_object.CopyFromString(u'2010-08-12 21:06:31.546875-01:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)

    expected_time_elements_tuple = (2010, 8, 12, 20, 6, 31, 546)
    expected_number_of_seconds = 1281643591
    time_elements_object.CopyFromString(u'2010-08-12 21:06:31.546875+01:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)

    expected_time_elements_tuple = (1601, 1, 2, 0, 0, 0, 0)
    expected_number_of_seconds = -11644387200
    time_elements_object.CopyFromString(u'1601-01-02 00:00:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)

  def testCopyFromStringISO8601(self):
    """Tests the CopyFromStringISO8601 function."""
    time_elements_object = time_elements.TimeElementsInMilliseconds()

    expected_time_elements_tuple = (2010, 8, 12, 0, 0, 0, 0)
    expected_number_of_seconds = 1281571200
    time_elements_object.CopyFromStringISO8601(u'2010-08-12')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31, 0)
    expected_number_of_seconds = 1281647191
    time_elements_object.CopyFromStringISO8601(u'2010-08-12T21:06:31')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31, 0)
    expected_number_of_seconds = 1281647191
    time_elements_object.CopyFromStringISO8601(u'2010-08-12T21:06:31Z')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31, 546)
    expected_number_of_seconds = 1281647191
    time_elements_object.CopyFromStringISO8601(u'2010-08-12T21:06:31.546875')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)

    expected_time_elements_tuple = (2010, 8, 12, 21, 6, 31, 546)
    expected_number_of_seconds = 1281647191
    time_elements_object.CopyFromStringISO8601(u'2010-08-12T21:06:31,546875')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)

    expected_time_elements_tuple = (2010, 8, 12, 22, 6, 31, 546)
    expected_number_of_seconds = 1281650791
    time_elements_object.CopyFromStringISO8601(
        u'2010-08-12T21:06:31.546875-01:00')
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(
        time_elements_object._number_of_seconds, expected_number_of_seconds)

    expected_time_elements_tuple = (2010, 8, 12, 20, 6, 31, 546)
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

  def testCopyFromStringTuple(self):
    """Tests the CopyFromStringTuple function."""
    time_elements_object = time_elements.TimeElementsInMilliseconds()

    expected_time_elements_tuple = (2010, 8, 12, 20, 6, 31)
    time_elements_object.CopyFromStringTuple(
        time_elements_tuple=(u'2010', u'8', u'12', u'20', u'6', u'31', u'546'))
    self.assertIsNotNone(time_elements_object)
    self.assertEqual(
        time_elements_object._time_elements_tuple, expected_time_elements_tuple)
    self.assertEqual(time_elements_object._milliseconds, 546)

    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringTuple(
          time_elements_tuple=(u'2010', u'8', u'12', u'20', u'6', u'31'))

    with self.assertRaises(ValueError):
      time_elements_object.CopyFromStringTuple(
          time_elements_tuple=(u'2010', u'8', u'12', u'20', u'6', u'31', u'9S'))

  def testCopyToStatTimeTuple(self):
    """Tests the CopyToStatTimeTuple function."""
    time_elements_object = time_elements.TimeElementsInMilliseconds(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31, 429))

    expected_stat_time_tuple = (1281643591, 429000)
    stat_time_tuple = time_elements_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, expected_stat_time_tuple)

    time_elements_object = time_elements.TimeElementsInMilliseconds()

    expected_stat_time_tuple = (None, None)
    stat_time_tuple = time_elements_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, expected_stat_time_tuple)

  def testGetPlasoTimestamp(self):
    """Tests the GetPlasoTimestamp function."""
    time_elements_object = time_elements.TimeElementsInMilliseconds(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31, 429))

    expected_micro_posix_number_of_seconds = 1281643591429000
    micro_posix_number_of_seconds = time_elements_object.GetPlasoTimestamp()
    self.assertEqual(
        micro_posix_number_of_seconds, expected_micro_posix_number_of_seconds)

    time_elements_object = time_elements.TimeElementsInMilliseconds()

    micro_posix_number_of_seconds = time_elements_object.GetPlasoTimestamp()
    self.assertIsNone(micro_posix_number_of_seconds)


if __name__ == '__main__':
  unittest.main()
