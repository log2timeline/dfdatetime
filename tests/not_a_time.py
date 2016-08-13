#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the not a time implementation."""

import unittest

from dfdatetime import not_a_time


class NotATimeTest(unittest.TestCase):
  """Tests for not a time."""

  # pylint: disable=protected-access

  def testCopyFromString(self):
    """Tests the CopyFromString function."""
    not_a_time_object = not_a_time.NotATime()

    with self.assertRaises(ValueError):
      not_a_time_object.CopyFromString(u'2010-08-12 21:06:31.546875+01:00')

  def testCopyToStatTimeTuple(self):
    """Tests the CopyToStatTimeTuple function."""
    not_a_time_object = not_a_time.NotATime()

    expected_stat_time_tuple = (0, 0)
    stat_time_tuple = not_a_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, expected_stat_time_tuple)

  def testGetPlasoTimestamp(self):
    """Tests the GetPlasoTimestamp function."""
    not_a_time_object = not_a_time.NotATime()

    expected_micro_posix_timestamp = 0
    micro_posix_timestamp = not_a_time_object.GetPlasoTimestamp()
    self.assertEqual(micro_posix_timestamp, expected_micro_posix_timestamp)


if __name__ == '__main__':
  unittest.main()
