#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for the semantic time implementation."""

from __future__ import unicode_literals

import unittest

from dfdatetime import semantic_time

from tests import interface


class SemanticTimeTest(unittest.TestCase):
  """Tests for semantic time."""

  # pylint: disable=assignment-from-none,protected-access

  def testComparison(self):
    """Tests the comparison functions."""
    semantic_time_object1 = semantic_time.SemanticTime()
    semantic_time_object1._SORT_ORDER = 1

    semantic_time_object2 = semantic_time.SemanticTime()
    semantic_time_object2._SORT_ORDER = 1

    self.assertTrue(semantic_time_object1 == semantic_time_object2)
    self.assertTrue(semantic_time_object1 >= semantic_time_object2)
    self.assertFalse(semantic_time_object1 > semantic_time_object2)
    self.assertTrue(semantic_time_object1 <= semantic_time_object2)
    self.assertFalse(semantic_time_object1 < semantic_time_object2)
    self.assertFalse(semantic_time_object1 != semantic_time_object2)

    semantic_time_object2 = semantic_time.SemanticTime()
    semantic_time_object2._SORT_ORDER = 2

    self.assertFalse(semantic_time_object1 == semantic_time_object2)
    self.assertFalse(semantic_time_object1 >= semantic_time_object2)
    self.assertFalse(semantic_time_object1 > semantic_time_object2)
    self.assertTrue(semantic_time_object1 <= semantic_time_object2)
    self.assertTrue(semantic_time_object1 < semantic_time_object2)
    self.assertTrue(semantic_time_object1 != semantic_time_object2)

    date_time_values1 = interface.TestDateTimeValues()

    self.assertFalse(semantic_time_object1 == date_time_values1)
    self.assertFalse(semantic_time_object1 >= date_time_values1)
    self.assertFalse(semantic_time_object1 > date_time_values1)
    self.assertTrue(semantic_time_object1 <= date_time_values1)
    self.assertTrue(semantic_time_object1 < date_time_values1)
    self.assertTrue(semantic_time_object1 != date_time_values1)

    self.assertFalse(semantic_time_object1 == 0.0)

    with self.assertRaises(ValueError):
      semantic_time_object1 >= 0.0  # pylint: disable=pointless-statement

    with self.assertRaises(ValueError):
      semantic_time_object1 > 0.0  # pylint: disable=pointless-statement

    with self.assertRaises(ValueError):
      semantic_time_object1 <= 0.0  # pylint: disable=pointless-statement

    with self.assertRaises(ValueError):
      semantic_time_object1 < 0.0  # pylint: disable=pointless-statement

    self.assertTrue(semantic_time_object1 != 0.0)

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

  def testCopyToDateTimeStringISO8601(self):
    """Tests the CopyToDateTimeStringISO8601 function."""
    semantic_time_object = semantic_time.SemanticTime(string='Never')

    date_time_string = semantic_time_object.CopyToDateTimeStringISO8601()
    self.assertIsNone(date_time_string)

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

  def testGetTimeOfDay(self):
    """Tests the GetTimeOfDay function."""
    semantic_time_object = semantic_time.SemanticTime()

    time_of_day_tuple = semantic_time_object.GetTimeOfDay()
    self.assertEqual(time_of_day_tuple, (None, None, None))

  def testGetPlasoTimestamp(self):
    """Tests the GetPlasoTimestamp function."""
    semantic_time_object = semantic_time.SemanticTime()

    micro_posix_timestamp = semantic_time_object.GetPlasoTimestamp()
    self.assertEqual(micro_posix_timestamp, 0)


class InvalidTimeTest(unittest.TestCase):
  """Tests for semantic time that represents invalid.."""

  def testInitialize(self):
    """Tests the __init__ function."""
    invalid_time_object = semantic_time.InvalidTime()
    self.assertEqual(invalid_time_object.string, 'Invalid')


class NeverTest(unittest.TestCase):
  """Tests for semantic time that represents never."""

  # pylint: disable=protected-access

  def testInitialize(self):
    """Tests the __init__ function."""
    never_time_object = semantic_time.Never()
    self.assertEqual(never_time_object.string, 'Never')

  def testComparison(self):
    """Tests the comparison functions."""
    never_time_object1 = semantic_time.Never()

    never_time_object2 = semantic_time.Never()

    self.assertTrue(never_time_object1 == never_time_object2)
    self.assertTrue(never_time_object1 >= never_time_object2)
    self.assertFalse(never_time_object1 > never_time_object2)
    self.assertTrue(never_time_object1 <= never_time_object2)
    self.assertFalse(never_time_object1 < never_time_object2)
    self.assertFalse(never_time_object1 != never_time_object2)

    semantic_time_object2 = semantic_time.SemanticTime()
    semantic_time_object2._SORT_ORDER = 1

    self.assertFalse(never_time_object1 == semantic_time_object2)
    self.assertTrue(never_time_object1 >= semantic_time_object2)
    self.assertTrue(never_time_object1 > semantic_time_object2)
    self.assertFalse(never_time_object1 <= semantic_time_object2)
    self.assertFalse(never_time_object1 < semantic_time_object2)
    self.assertTrue(never_time_object1 != semantic_time_object2)

    date_time_values1 = interface.TestDateTimeValues()

    self.assertFalse(never_time_object1 == date_time_values1)
    self.assertTrue(never_time_object1 >= date_time_values1)
    self.assertTrue(never_time_object1 > date_time_values1)
    self.assertFalse(never_time_object1 <= date_time_values1)
    self.assertFalse(never_time_object1 < date_time_values1)
    self.assertTrue(never_time_object1 != date_time_values1)

    self.assertFalse(never_time_object1 == 0.0)

    with self.assertRaises(ValueError):
      never_time_object1 >= 0.0  # pylint: disable=pointless-statement

    with self.assertRaises(ValueError):
      never_time_object1 > 0.0  # pylint: disable=pointless-statement

    with self.assertRaises(ValueError):
      never_time_object1 <= 0.0  # pylint: disable=pointless-statement

    with self.assertRaises(ValueError):
      never_time_object1 < 0.0  # pylint: disable=pointless-statement

    self.assertTrue(never_time_object1 != 0.0)


class NotSetTest(unittest.TestCase):
  """Tests for semantic time that represents not set."""

  def testInitialize(self):
    """Tests the __init__ function."""
    not_set_time_object = semantic_time.NotSet()
    self.assertEqual(not_set_time_object.string, 'Not set')


if __name__ == '__main__':
  unittest.main()
