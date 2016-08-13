#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the semantic time implementation."""

import unittest

from dfdatetime import semantic_time


class SemanticTimeTest(unittest.TestCase):
  """Tests for semantic time."""

  # pylint: disable=protected-access

  def testCopyFromString(self):
    """Tests the CopyFromString function."""
    semantic_time_object = semantic_time.SemanticTime()

    semantic_time_object.CopyFromString(u'Never')
    self.assertEqual(semantic_time_object.string, u'Never')

  def testCopyToStatTimeTuple(self):
    """Tests the CopyToStatTimeTuple function."""
    semantic_time_object = semantic_time.SemanticTime()

    expected_stat_time_tuple = (0, 0)
    stat_time_tuple = semantic_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, expected_stat_time_tuple)

  def testGetPlasoTimestamp(self):
    """Tests the GetPlasoTimestamp function."""
    semantic_time_object = semantic_time.SemanticTime()

    expected_micro_posix_timestamp = 0
    micro_posix_timestamp = semantic_time_object.GetPlasoTimestamp()
    self.assertEqual(micro_posix_timestamp, expected_micro_posix_timestamp)


if __name__ == '__main__':
  unittest.main()
