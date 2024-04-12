#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for date and time precision helpers."""

import decimal
import unittest

from dfdatetime import definitions
from dfdatetime import precisions


class DateTimePrecisionHelperTest(unittest.TestCase):
  """Tests for the date time precision helper interface."""

  def testCopyNanosecondsToFractionOfSecond(self):
    """Tests the CopyNanosecondsToFractionOfSecond function."""
    precision_helper = precisions.DateTimePrecisionHelper

    with self.assertRaises(NotImplementedError):
      precision_helper.CopyNanosecondsToFractionOfSecond(0)

  def testCopyToDateTimeString(self):
    """Tests the CopyToDateTimeString function."""
    precision_helper = precisions.DateTimePrecisionHelper

    with self.assertRaises(NotImplementedError):
      precision_helper.CopyToDateTimeString((2018, 1, 2, 19, 45, 12), 0.5)


class SecondsPrecisionHelperTest(unittest.TestCase):
  """Tests for the seconds precision helper."""

  def testCopyNanosecondsToFractionOfSecond(self):
    """Tests the CopyNanosecondsToFractionOfSecond function."""
    precision_helper = precisions.SecondsPrecisionHelper

    fraction_of_second = precision_helper.CopyNanosecondsToFractionOfSecond(
        123456)
    self.assertEqual(fraction_of_second, 0.0)

    with self.assertRaises(ValueError):
      precision_helper.CopyNanosecondsToFractionOfSecond(-1)

    with self.assertRaises(ValueError):
      precision_helper.CopyNanosecondsToFractionOfSecond(1000000000)

  def testCopyToDateTimeString(self):
    """Tests the CopyToDateTimeString function."""
    precision_helper = precisions.SecondsPrecisionHelper

    date_time_string = precision_helper.CopyToDateTimeString(
        (2018, 1, 2, 19, 45, 12), 0.123456)
    self.assertEqual(date_time_string, '2018-01-02 19:45:12')

    with self.assertRaises(ValueError):
      precision_helper.CopyToDateTimeString((2018, 1, 2, 19, 45, 12), 4.123456)


class CentisecondsPrevisionHelperTest(unittest.TestCase):
  """Tests for the centiseconds prevision helper."""

  def testCopyNanosecondsToFractionOfSecond(self):
    """Tests the CopyNanosecondsToFractionOfSecond function."""
    precision_helper = precisions.CentisecondsPrecisionHelper

    fraction_of_second = precision_helper.CopyNanosecondsToFractionOfSecond(
        123456789)
    self.assertEqual(fraction_of_second, decimal.Decimal('0.12'))

    with self.assertRaises(ValueError):
      precision_helper.CopyNanosecondsToFractionOfSecond(-1)

    with self.assertRaises(ValueError):
      precision_helper.CopyNanosecondsToFractionOfSecond(1000000000)

  def testCopyToDateTimeString(self):
    """Tests the CopyToDateTimeString function."""
    precision_helper = precisions.CentisecondsPrecisionHelper

    date_time_string = precision_helper.CopyToDateTimeString(
        (2018, 1, 2, 19, 45, 12), 0.123456)
    self.assertEqual(date_time_string, '2018-01-02 19:45:12.12')

    with self.assertRaises(ValueError):
      precision_helper.CopyToDateTimeString((2018, 1, 2, 19, 45, 12), 4.123456)


class MillisecondsPrecisionHelperTest(unittest.TestCase):
  """Tests for the milliseconds precision helper."""

  def testCopyNanosecondsToFractionOfSecond(self):
    """Tests the CopyNanosecondsToFractionOfSecond function."""
    precision_helper = precisions.MillisecondsPrecisionHelper

    fraction_of_second = precision_helper.CopyNanosecondsToFractionOfSecond(
        123456789)
    self.assertEqual(fraction_of_second, decimal.Decimal('0.123'))

    with self.assertRaises(ValueError):
      precision_helper.CopyNanosecondsToFractionOfSecond(-1)

    with self.assertRaises(ValueError):
      precision_helper.CopyNanosecondsToFractionOfSecond(1000000000)

  def testCopyToDateTimeString(self):
    """Tests the CopyToDateTimeString function."""
    precision_helper = precisions.MillisecondsPrecisionHelper

    date_time_string = precision_helper.CopyToDateTimeString(
        (2018, 1, 2, 19, 45, 12), 0.123456)
    self.assertEqual(date_time_string, '2018-01-02 19:45:12.123')

    with self.assertRaises(ValueError):
      precision_helper.CopyToDateTimeString((2018, 1, 2, 19, 45, 12), 4.123456)


class MicrosecondsPrecisionHelperTest(unittest.TestCase):
  """Tests for the microseconds precision helper."""

  def testCopyNanosecondsToFractionOfSecond(self):
    """Tests the CopyNanosecondsToFractionOfSecond function."""
    precision_helper = precisions.MicrosecondsPrecisionHelper

    fraction_of_second = precision_helper.CopyNanosecondsToFractionOfSecond(
        123456789)
    self.assertEqual(fraction_of_second, decimal.Decimal('0.123456'))

    with self.assertRaises(ValueError):
      precision_helper.CopyNanosecondsToFractionOfSecond(-1)

    with self.assertRaises(ValueError):
      precision_helper.CopyNanosecondsToFractionOfSecond(1000000000)

  def testCopyToDateTimeString(self):
    """Tests the CopyToDateTimeString function."""
    precision_helper = precisions.MicrosecondsPrecisionHelper

    date_time_string = precision_helper.CopyToDateTimeString(
        (2018, 1, 2, 19, 45, 12), 0.123456)
    self.assertEqual(date_time_string, '2018-01-02 19:45:12.123456')

    with self.assertRaises(ValueError):
      precision_helper.CopyToDateTimeString((2018, 1, 2, 19, 45, 12), 4.123456)


class NanosecondsPrecisionHelperTest(unittest.TestCase):
  """Tests for the nanoseconds precision helper."""

  def testCopyNanosecondsToFractionOfSecond(self):
    """Tests the CopyNanosecondsToFractionOfSecond function."""
    precision_helper = precisions.NanosecondsPrecisionHelper

    fraction_of_second = precision_helper.CopyNanosecondsToFractionOfSecond(
        123456789)
    self.assertEqual(fraction_of_second, decimal.Decimal('0.123456789'))

    with self.assertRaises(ValueError):
      precision_helper.CopyNanosecondsToFractionOfSecond(-1)

    with self.assertRaises(ValueError):
      precision_helper.CopyNanosecondsToFractionOfSecond(1000000000)

  def testCopyToDateTimeString(self):
    """Tests the CopyToDateTimeString function."""
    precision_helper = precisions.NanosecondsPrecisionHelper

    date_time_string = precision_helper.CopyToDateTimeString(
        (2018, 1, 2, 19, 45, 12), 0.123456789)
    self.assertEqual(date_time_string, '2018-01-02 19:45:12.123456789')

    with self.assertRaises(ValueError):
      precision_helper.CopyToDateTimeString(
          (2018, 1, 2, 19, 45, 12), 4.123456789)


class PrecisionHelperFactoryTest(unittest.TestCase):
  """Tests for the date time precision helper factory."""

  def testCreatePrecisionHelper(self):
    """Tests the CreatePrecisionHelper function."""
    precision_helper = precisions.PrecisionHelperFactory.CreatePrecisionHelper(
        definitions.PRECISION_1_MICROSECOND)

    self.assertIsNotNone(precision_helper)

    with self.assertRaises(ValueError):
      precisions.PrecisionHelperFactory.CreatePrecisionHelper('bogus')


if __name__ == '__main__':
  unittest.main()
