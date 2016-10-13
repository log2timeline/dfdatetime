#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the HFS timestamp implementation."""

import unittest

from dfdatetime import hfs_time


class HFSTimeTest(unittest.TestCase):
  """Tests for the HFS timestamp."""

  def testCopyFromString(self):
    """Tests the CopyFromString function."""
    hfs_time_object = hfs_time.HFSTime()

    expected_timestamp = 3458160000
    hfs_time_object.CopyFromString(u'2013-08-01')
    self.assertEqual(hfs_time_object.timestamp, expected_timestamp)

    expected_timestamp = 3458215528
    hfs_time_object.CopyFromString(u'2013-08-01 15:25:28')
    self.assertEqual(hfs_time_object.timestamp, expected_timestamp)

    expected_timestamp = 3458215528
    hfs_time_object.CopyFromString(u'2013-08-01 15:25:28.546875')
    self.assertEqual(hfs_time_object.timestamp, expected_timestamp)

    expected_timestamp = 3458219128
    hfs_time_object.CopyFromString(u'2013-08-01 15:25:28.546875-01:00')
    self.assertEqual(hfs_time_object.timestamp, expected_timestamp)

    expected_timestamp = 3458211928
    hfs_time_object.CopyFromString(u'2013-08-01 15:25:28.546875+01:00')
    self.assertEqual(hfs_time_object.timestamp, expected_timestamp)

    expected_timestamp = 86400
    hfs_time_object.CopyFromString(u'1904-01-02 00:00:00')
    self.assertEqual(hfs_time_object.timestamp, expected_timestamp)

  def testCopyToStatTimeTuple(self):
    """Tests the CopyToStatTimeTuple function."""
    hfs_time_object = hfs_time.HFSTime(timestamp=3458215528)

    expected_stat_time_tuple = (1375370728, 0)
    stat_time_tuple = hfs_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, expected_stat_time_tuple)

    hfs_time_object = hfs_time.HFSTime(timestamp=0x1ffffffff)

    expected_stat_time_tuple = (None, None)
    stat_time_tuple = hfs_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, expected_stat_time_tuple)

    hfs_time_object = hfs_time.HFSTime(timestamp=-0x1ffffffff)

    expected_stat_time_tuple = (None, None)
    stat_time_tuple = hfs_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, expected_stat_time_tuple)

    hfs_time_object = hfs_time.HFSTime()

    expected_stat_time_tuple = (None, None)
    stat_time_tuple = hfs_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, expected_stat_time_tuple)

  def testGetPlasoTimestamp(self):
    """Tests the GetPlasoTimestamp function."""
    hfs_time_object = hfs_time.HFSTime(timestamp=3458215528)

    expected_micro_posix_timestamp = 1375370728000000
    micro_posix_timestamp = hfs_time_object.GetPlasoTimestamp()
    self.assertEqual(micro_posix_timestamp, expected_micro_posix_timestamp)

    hfs_time_object = hfs_time.HFSTime(timestamp=0x1ffffffff)

    micro_posix_timestamp = hfs_time_object.GetPlasoTimestamp()
    self.assertIsNone(micro_posix_timestamp)

    hfs_time_object = hfs_time.HFSTime(timestamp=-0x1ffffffff)

    micro_posix_timestamp = hfs_time_object.GetPlasoTimestamp()
    self.assertIsNone(micro_posix_timestamp)

    hfs_time_object = hfs_time.HFSTime()

    micro_posix_timestamp = hfs_time_object.GetPlasoTimestamp()
    self.assertIsNone(micro_posix_timestamp)


if __name__ == '__main__':
  unittest.main()
