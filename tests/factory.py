#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for the date and time values factory."""

import unittest

from dfdatetime import interface
from dfdatetime import factory


class TestDateTimeValues(interface.DateTimeValues):
  """Date and time values for testing."""

  # pylint: disable=redundant-returns-doc

  def _GetNormalizedTimestamp(self):
    """Retrieves the normalized timestamp.

    Returns:
      decimal.Decimal: normalized timestamp, which contains the number of
          seconds since January 1, 1970 00:00:00 and a fraction of second used
          for increased precision, or None if the normalized timestamp cannot be
          determined.
    """
    return None

  def CopyFromDateTimeString(self, time_string):
    """Copies a date time value from a date and time string.

    Args:
      time_string (str): date and time value formatted as:
          YYYY-MM-DD hh:mm:ss.######[+-]##:##

          Where # are numeric digits ranging from 0 to 9 and the seconds
          fraction can be either 3 or 6 digits. The time of day, seconds
          fraction and time zone offset are optional. The default time zone
          is UTC.

    Raises:
      ValueError: if the time string is invalid or not supported.
    """
    return

  def CopyToDateTimeString(self):
    """Copies the date time value to a date and time string.

    Returns:
      str: date and time value formatted as: "YYYY-MM-DD hh:mm:ss.######" or
          None if the timestamp cannot be copied to a date and time string.
    """
    return None


class FactoryTest(unittest.TestCase):
  """Tests the date and time values factory."""

  def testDateTimeValuesRegistration(self):
    """Tests the Register and DeregisterDateTimeValues functions."""
    # pylint: disable=protected-access
    number_of_date_time_values_types = len(
        factory.Factory._date_time_values_types)

    factory.Factory.RegisterDateTimeValues(TestDateTimeValues)
    self.assertEqual(
        len(factory.Factory._date_time_values_types),
        number_of_date_time_values_types + 1)

    with self.assertRaises(KeyError):
      factory.Factory.RegisterDateTimeValues(TestDateTimeValues)

    factory.Factory.DeregisterDateTimeValues(TestDateTimeValues)
    self.assertEqual(
        len(factory.Factory._date_time_values_types),
        number_of_date_time_values_types)

  def testNewDateTimeValues(self):
    """Tests the NewDateTimeValues function."""
    test_date_time_values = factory.Factory.NewDateTimeValues(
        'Filetime', timestamp=0x01cb3a623d0a17ce)

    self.assertIsNotNone(test_date_time_values)


if __name__ == '__main__':
  unittest.main()
