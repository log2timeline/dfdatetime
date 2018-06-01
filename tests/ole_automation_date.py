#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for the OLE Automation date implementation."""

from __future__ import unicode_literals

import decimal
import unittest

from dfdatetime import ole_automation_date


class OLEAutomationDateEpochTest(unittest.TestCase):
  """Tests for the OLE Automation date epoch."""

  def testInitialize(self):
    """Tests the __init__ function."""
    ole_automation_date_epoch = ole_automation_date.OLEAutomationDateEpoch()
    self.assertIsNotNone(ole_automation_date_epoch)


class OLEAutomationDateTest(unittest.TestCase):
  """Tests for the OLE Automation date."""

  # pylint: disable=protected-access

  def testProperties(self):
    """Tests the properties."""
    ole_automation_date_object = ole_automation_date.OLEAutomationDate(
        timestamp=43044.480556)
    self.assertEqual(ole_automation_date_object.timestamp, 43044.480556)

    ole_automation_date_object = ole_automation_date.OLEAutomationDate()
    self.assertIsNone(ole_automation_date_object.timestamp)

  def testGetNormalizedTimestamp(self):
    """Tests the _GetNormalizedTimestamp function."""
    ole_automation_date_object = ole_automation_date.OLEAutomationDate(
        timestamp=43044.480556)

    expected_normalized_timestamp = decimal.Decimal(
        '1509881520.038400194607675076')
    normalized_timestamp = ole_automation_date_object._GetNormalizedTimestamp()
    self.assertEqual(normalized_timestamp, expected_normalized_timestamp)

    ole_automation_date_object = ole_automation_date.OLEAutomationDate()

    normalized_timestamp = ole_automation_date_object._GetNormalizedTimestamp()
    self.assertIsNone(normalized_timestamp)

  def testCopyFromDateTimeString(self):
    """Tests the CopyFromDateTimeString function."""
    ole_automation_date_object = ole_automation_date.OLEAutomationDate()

    expected_timestamp = 43044.0
    ole_automation_date_object.CopyFromDateTimeString('2017-11-05')
    self.assertEqual(ole_automation_date_object.timestamp, expected_timestamp)

    expected_timestamp = 43044.48055555555
    ole_automation_date_object.CopyFromDateTimeString('2017-11-05 11:32:00')
    self.assertEqual(ole_automation_date_object.timestamp, expected_timestamp)

    expected_timestamp = 43044.480561885124
    ole_automation_date_object.CopyFromDateTimeString(
        '2017-11-05 11:32:00.546875')
    self.assertEqual(ole_automation_date_object.timestamp, expected_timestamp)

    expected_timestamp = 43044.522228551796
    ole_automation_date_object.CopyFromDateTimeString(
        '2017-11-05 11:32:00.546875-01:00')
    self.assertEqual(ole_automation_date_object.timestamp, expected_timestamp)

    expected_timestamp = 43044.43889521846
    ole_automation_date_object.CopyFromDateTimeString(
        '2017-11-05 11:32:00.546875+01:00')
    self.assertEqual(ole_automation_date_object.timestamp, expected_timestamp)

    expected_timestamp = 2.0
    ole_automation_date_object.CopyFromDateTimeString('1900-01-01 00:00:00')
    self.assertEqual(ole_automation_date_object.timestamp, expected_timestamp)

  def testCopyToDateTimeString(self):
    """Tests the CopyToDateTimeString function."""
    ole_automation_date_object = ole_automation_date.OLEAutomationDate(
        timestamp=43044.480556)

    date_time_string = ole_automation_date_object.CopyToDateTimeString()
    self.assertEqual(date_time_string, '2017-11-05 11:32:00.038400')

    ole_automation_date_object = ole_automation_date.OLEAutomationDate()

    date_time_string = ole_automation_date_object.CopyToDateTimeString()
    self.assertIsNone(date_time_string)

  def testCopyToDateTimeStringISO8601(self):
    """Tests the CopyToDateTimeStringISO8601 function."""
    ole_automation_date_object = ole_automation_date.OLEAutomationDate(
        timestamp=43044.480556)

    date_time_string = ole_automation_date_object.CopyToDateTimeStringISO8601()
    self.assertEqual(date_time_string, '2017-11-05T11:32:00.038400Z')

  def testGetDate(self):
    """Tests the GetDate function."""
    ole_automation_date_object = ole_automation_date.OLEAutomationDate(
        timestamp=43044.480556)

    date_tuple = ole_automation_date_object.GetDate()
    self.assertEqual(date_tuple, (2017, 11, 5))

    ole_automation_date_object = ole_automation_date.OLEAutomationDate()

    date_tuple = ole_automation_date_object.GetDate()
    self.assertEqual(date_tuple, (None, None, None))

  def testGetTimeOfDay(self):
    """Tests the GetTimeOfDay function."""
    ole_automation_date_object = ole_automation_date.OLEAutomationDate(
        timestamp=43044.480556)

    time_of_day_tuple = ole_automation_date_object.GetTimeOfDay()
    self.assertEqual(time_of_day_tuple, (11, 32, 0))

    ole_automation_date_object = ole_automation_date.OLEAutomationDate()

    time_of_day_tuple = ole_automation_date_object.GetTimeOfDay()
    self.assertEqual(time_of_day_tuple, (None, None, None))


if __name__ == '__main__':
  unittest.main()
