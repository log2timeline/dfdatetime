#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the semantic time implementation."""

from __future__ import unicode_literals

import unittest

from dfdatetime import semantic_time


class SemanticTimeTest(unittest.TestCase):
  """Tests for semantic time."""

  # pylint: disable=protected-access

  def testCopyFromString(self):
    """Tests the CopyFromString function."""
    semantic_time_object = semantic_time.SemanticTime()

    semantic_time_object.CopyFromString('Never')
    self.assertEqual(semantic_time_object.string, 'Never')

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


class InvalidSemanticTimeTest(unittest.TestCase):
  """Tests for semantic time that represents invalid.."""

  def testInitialize(self):
    """Tests the __init__ function."""
    semantic_time_object = semantic_time.InvalidSemanticTime()
    self.assertEqual(semantic_time_object.string, 'Invalid')


class NeverSemanticTimeTest(unittest.TestCase):
  """Tests for semantic time that represents never."""

  def testInitialize(self):
    """Tests the __init__ function."""
    semantic_time_object = semantic_time.NeverSemanticTime()
    self.assertEqual(semantic_time_object.string, 'Never')


class NotSetSemanticTimeTest(unittest.TestCase):
  """Tests for semantic time that represents not set."""

  def testInitialize(self):
    """Tests the __init__ function."""
    semantic_time_object = semantic_time.NotSetSemanticTime()
    self.assertEqual(semantic_time_object.string, 'Not set')


if __name__ == '__main__':
  unittest.main()
