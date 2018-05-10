# -*- coding: utf-8 -*-
"""Fake timestamp implementation."""

from __future__ import unicode_literals

import decimal
import time

from dfdatetime import definitions
from dfdatetime import interface
from dfdatetime import posix_time


class FakeTime(interface.DateTimeValues):
  """Fake timestamp.

  The fake timestamp is intended for testing purposes. On initialization
  it contains the current time in UTC in microsecond precision.

  Attributes:
    is_local_time (bool): True if the date and time value is in local time.
  """

  _EPOCH = posix_time.PosixTimeEpoch()

  def __init__(self):
    """Initializes a fake timestamp."""
    # Note that time.time() and divmod return floating point values.
    timestamp, fraction_of_second = divmod(time.time(), 1)

    super(FakeTime, self).__init__()
    self._microseconds = int(
        fraction_of_second * definitions.MICROSECONDS_PER_SECOND)
    self._number_of_seconds = int(timestamp)
    self._precision = definitions.PRECISION_1_MICROSECOND

  def _GetNormalizedTimestamp(self):
    """Retrieves the normalized timestamp.

    Returns:
      decimal.Decimal: normalized timestamp, which contains the number of
          seconds since January 1, 1970 00:00:00 and a fraction of second used
          for increased precision, or None if the normalized timestamp cannot be
          determined.
    """
    if self._normalized_timestamp is None:
      if self._number_of_seconds is not None:
        self._normalized_timestamp = (
            decimal.Decimal(self._microseconds) /
            definitions.MICROSECONDS_PER_SECOND)
        self._normalized_timestamp += decimal.Decimal(self._number_of_seconds)

    return self._normalized_timestamp

  def CopyFromDateTimeString(self, time_string):
    """Copies a fake timestamp from a date and time string.

    Args:
      time_string (str): date and time value formatted as:
          YYYY-MM-DD hh:mm:ss.######[+-]##:##

          Where # are numeric digits ranging from 0 to 9 and the seconds
          fraction can be either 3 or 6 digits. The time of day, seconds
          fraction and time zone offset are optional. The default time zone
          is UTC.
    """
    date_time_values = self._CopyDateTimeFromString(time_string)

    year = date_time_values.get('year', 0)
    month = date_time_values.get('month', 0)
    day_of_month = date_time_values.get('day_of_month', 0)
    hours = date_time_values.get('hours', 0)
    minutes = date_time_values.get('minutes', 0)
    seconds = date_time_values.get('seconds', 0)

    self._normalized_timestamp = None
    self._number_of_seconds = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds)
    self._microseconds = date_time_values.get('microseconds', None)

    self.is_local_time = False

  def CopyToDateTimeString(self):
    """Copies the fake timestamp to a date and time string.

    Returns:
      str: date and time value formatted as: "YYYY-MM-DD hh:mm:ss" or
          "YYYY-MM-DD hh:mm:ss.######" or None if the number of seconds
          is missing.
    """
    if self._number_of_seconds is None:
      return None

    number_of_days, hours, minutes, seconds = self._GetTimeValues(
        self._number_of_seconds)

    year, month, day_of_month = self._GetDateValuesWithEpoch(
        number_of_days, self._EPOCH)

    if self._microseconds is None:
      return '{0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}'.format(
          year, month, day_of_month, hours, minutes, seconds)

    return '{0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}.{6:06d}'.format(
        year, month, day_of_month, hours, minutes, seconds,
        self._microseconds)
