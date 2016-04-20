#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the POSIX timestamp implementation."""

import unittest

from dfdatetime import posix_time


class PosixTimeTest(unittest.TestCase):
  """Tests for the POSIX timestamp object."""

  def testCopyToMicroPosixTimestamp(self):
    """Tests the CopyToMicroPosixTimestamp function."""
    posix_time_object = posix_time.PosixTime(1281643591, micro_seconds=546875)

    expected_micro_posix_timestamp = 1281643591546875
    micro_posix_timestamp = posix_time_object.CopyToMicroPosixTimestamp()
    self.assertEqual(micro_posix_timestamp, expected_micro_posix_timestamp)

  def testCopyToStatTimeTuple(self):
    """Tests the CopyToStatTimeTuple function."""
    posix_time_object = posix_time.PosixTime(1281643591, micro_seconds=546875)

    expected_stat_time_tuple = (1281643591, 5468750)
    stat_time_tuple = posix_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, expected_stat_time_tuple)

  def testGetPlasoTimestamp(self):
    """Tests the GetPlasoTimestamp function."""
    posix_time_object = posix_time.PosixTime(1281643591, micro_seconds=546875)

    expected_micro_posix_timestamp = 1281643591546875
    micro_posix_timestamp = posix_time_object.GetPlasoTimestamp()
    self.assertEqual(micro_posix_timestamp, expected_micro_posix_timestamp)


if __name__ == '__main__':
  unittest.main()
