#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the semantic time implementation."""

from __future__ import unicode_literals

import unittest

from dfdatetime import semantic_time


class SemanticTimeTest(unittest.TestCase):
  """Tests for semantic time."""

  # pylint: disable=protected-access

  def testCopyFromDateTimeString(self):
    """Tests the CopyFromDateTimeString function."""
    semantic_time_object = semantic_time.SemanticTime()

    semantic_time_object.CopyFromDateTimeString('Never')
    self.assertEqual(semantic_time_object.string, 'Never')

  def testCopyToDateTimeString(self):
    """Tests the CopyToDateTimeString function."""
    semantic_time_object = semantic_time.SemanticTime(string='Never')

    date_time_string = semantic_time_object.CopyToDateTimeString()
    self.assertEqual(date_time_string, 'Never')

  def testCopyToStatTimeTuple(self):
    """Tests the CopyToStatTimeTuple function."""
    semantic_time_object = semantic_time.SemanticTime()

    stat_time_tuple = semantic_time_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, (None, None))

  def testGetDate(self):
    """Tests the GetDate function."""
    semantic_time_object = semantic_time.SemanticTime()

    date_tuple = semantic_time_object.GetDate()
    self.assertEqual(date_tuple, (None, None, None))

  def testGetPlasoTimestamp(self):
    """Tests the GetPlasoTimestamp function."""
    semantic_time_object = semantic_time.SemanticTime()

    micro_posix_timestamp = semantic_time_object.GetPlasoTimestamp()
    self.assertEqual(micro_posix_timestamp, 0)


class InvalidTimeTest(unittest.TestCase):
  """Tests for semantic time that represents invalid.."""

  def testInitialize(self):
    """Tests the __init__ function."""
    semantic_time_object = semantic_time.InvalidTime()
    self.assertEqual(semantic_time_object.string, 'Invalid')


class NeverTest(unittest.TestCase):
  """Tests for semantic time that represents never."""

  def testInitialize(self):
    """Tests the __init__ function."""
    semantic_time_object = semantic_time.Never()
    self.assertEqual(semantic_time_object.string, 'Never')


class NotSetTest(unittest.TestCase):
  """Tests for semantic time that represents not set."""

  def testInitialize(self):
    """Tests the __init__ function."""
    semantic_time_object = semantic_time.NotSet()
    self.assertEqual(semantic_time_object.string, 'Not set')


if __name__ == '__main__':
  unittest.main()
