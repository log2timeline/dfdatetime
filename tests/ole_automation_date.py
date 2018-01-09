#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the OLE Automation date implementation."""

from __future__ import unicode_literals

import unittest

from dfdatetime import ole_automation_date


class OLEAutomationDateTest(unittest.TestCase):
  """Tests for the OLE Automation date."""

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

  def testCopyToStatTimeTuple(self):
    """Tests the CopyToStatTimeTuple function."""
    ole_automation_date_object = ole_automation_date.OLEAutomationDate(
        timestamp=43044.480556)

    expected_stat_time_tuple = (1509881520, 384001)
    stat_time_tuple = ole_automation_date_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, expected_stat_time_tuple)

    ole_automation_date_object = ole_automation_date.OLEAutomationDate()

    expected_stat_time_tuple = (None, None)
    stat_time_tuple = ole_automation_date_object.CopyToStatTimeTuple()
    self.assertEqual(stat_time_tuple, expected_stat_time_tuple)

  def testCopyToDateTimeString(self):
    """Tests the CopyToDateTimeString function."""
    ole_automation_date_object = ole_automation_date.OLEAutomationDate(
        timestamp=43044.480556)

    date_time_string = ole_automation_date_object.CopyToDateTimeString()
    self.assertEqual(date_time_string, '2017-11-05 11:32:00.038400')

    ole_automation_date_object = ole_automation_date.OLEAutomationDate()

    date_time_string = ole_automation_date_object.CopyToDateTimeString()
    self.assertIsNone(date_time_string)

  def testGetPlasoTimestamp(self):
    """Tests the GetPlasoTimestamp function."""
    ole_automation_date_object = ole_automation_date.OLEAutomationDate(
        timestamp=43044.480556)

    expected_micro_posix_timestamp = 1509881520038400
    micro_posix_timestamp = ole_automation_date_object.GetPlasoTimestamp()
    self.assertEqual(micro_posix_timestamp, expected_micro_posix_timestamp)

    ole_automation_date_object = ole_automation_date.OLEAutomationDate()

    micro_posix_timestamp = ole_automation_date_object.GetPlasoTimestamp()
    self.assertIsNone(micro_posix_timestamp)


if __name__ == '__main__':
  unittest.main()
