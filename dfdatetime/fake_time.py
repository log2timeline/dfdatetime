# -*- coding: utf-8 -*-
"""Fake timestamp implementation."""

from __future__ import unicode_literals

import time

from dfdatetime import definitions
from dfdatetime import interface


class FakeTime(interface.DateTimeValues):
  """Fake timestamp.

  The fake timestamp is intended for testing purposes. On initialization
  it contains the current time in UTC in microsecond precision.

  Attributes:
    is_local_time (bool): True if the date and time value is in local time.
    precision (str): precision of the date and time value, which should
        be one of the PRECISION_VALUES in definitions.
  """

  def __init__(self):
    """Initializes a fake timestamp."""
    super(FakeTime, self).__init__()
    # Note that time.time() and divmod return floating point values.
    timestamp, fraction_of_second = divmod(time.time(), 1)
    self._microseconds = int(
        fraction_of_second * definitions.MICROSECONDS_PER_SECOND)
    self._number_of_seconds = int(timestamp)
    self.precision = definitions.PRECISION_1_MICROSECOND

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

    self._number_of_seconds = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds)
    self._microseconds = date_time_values.get('microseconds', None)

    self.is_local_time = False

  def CopyToStatTimeTuple(self):
    """Copies the fake timestamp to a stat timestamp tuple.

    Returns:
      tuple[int, int]: a POSIX timestamp in seconds and the remainder in
          100 nano seconds or (None, None) on error.
    """
    if self._number_of_seconds is None:
      return None, None

    if self._microseconds is not None:
      return self._number_of_seconds, (
          self._microseconds * self._100NS_PER_MICROSECOND)

    return self._number_of_seconds, None

  def CopyToDateTimeString(self):
    """Copies the fake timestamp to a date and time string.

    Returns:
      str: date and time value formatted as one of the following:
          YYYY-MM-DD hh:mm:ss
          YYYY-MM-DD hh:mm:ss.######
    """
    if self._number_of_seconds is None:
      return

    number_of_days, hours, minutes, seconds = self._GetTimeValues(
        self._number_of_seconds)

    year, month, day_of_month = self._GetDateValues(
        number_of_days, 1970, 1, 1)

    if self._microseconds is None:
      return '{0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}'.format(
          year, month, day_of_month, hours, minutes, seconds)

    return '{0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}.{6:06d}'.format(
        year, month, day_of_month, hours, minutes, seconds,
        self._microseconds)

  def GetPlasoTimestamp(self):
    """Retrieves a timestamp that is compatible with plaso.

    Returns:
      int: a POSIX timestamp in microseconds or None on error.
    """
    if self._number_of_seconds is None:
      return

    timestamp = self._number_of_seconds * definitions.MICROSECONDS_PER_SECOND
    if self._microseconds is None:
      return timestamp

    return timestamp + self._microseconds
