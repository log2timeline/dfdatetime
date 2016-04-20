#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the fake timestamp implementation."""

import unittest

from dfdatetime import fake_time


class FakeTimeTest(unittest.TestCase):
  """Tests for the fake timestamp object."""

  def testCopyToMicroPosixTimestamp(self):
    """Tests the CopyToMicroPosixTimestamp function."""
    fake_time_object = fake_time.FakeTime()

    expected_micro_posix_timestamp = 0
    micro_posix_timestamp = fake_time_object.CopyToMicroPosixTimestamp()
    self.assertNotEqual(micro_posix_timestamp, expected_micro_posix_timestamp)

  def testCopyToStatTimeTuple(self):
    """Tests the CopyToStatTimeTuple function."""
    fake_time_object = fake_time.FakeTime()

    expected_stat_time_tuple = (0, 0)
    stat_time_tuple = fake_time_object.CopyToStatTimeTuple()
    self.assertNotEqual(stat_time_tuple, expected_stat_time_tuple)


if __name__ == '__main__':
  unittest.main()
