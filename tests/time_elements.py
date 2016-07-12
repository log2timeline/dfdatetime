#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the time elements implementation."""

import unittest

from dfdatetime import time_elements


class PosixTimeTest(unittest.TestCase):
  """Tests for the POSIX timestamp object."""

  def testCopyToStatTimeTuple(self):
    """Tests the CopyToStatTimeTuple function."""
    time_elements_object = time_elements.TimeElements((2010, 8, 12, 20, 6, 31))

    expected_stat_time_tuple = (1281643591, 0)
    stat_time_tuple = time_elements_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, expected_stat_time_tuple)

  def testGetPlasoTimestamp(self):
    """Tests the GetPlasoTimestamp function."""
    time_elements_object = time_elements.TimeElements((2010, 8, 12, 20, 6, 31))

    expected_micro_posix_timestamp = 1281643591000000
    micro_posix_timestamp = time_elements_object.GetPlasoTimestamp()
    self.assertEqual(micro_posix_timestamp, expected_micro_posix_timestamp)


if __name__ == '__main__':
  unittest.main()
