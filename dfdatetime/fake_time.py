# -*- coding: utf-8 -*-
"""Fake timestamp implementation."""

import time

from dfdatetime import definitions
from dfdatetime import interface


class FakeTime(interface.DateTimeValues):
  """Class that implements a fake timestamp.

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
    self._microseconds = int(fraction_of_second * 1000000)
    self._number_of_seconds = int(timestamp)
    self.precision = definitions.PRECISION_1_MICROSECOND

  def CopyFromString(self, time_string):
    """Copies a fake timestamp from a string containing a date and time value.

    Args:
      time_string (str): date and time value formatted as:
          YYYY-MM-DD hh:mm:ss.######[+-]##:##

          Where # are numeric digits ranging from 0 to 9 and the seconds
          fraction can be either 3 or 6 digits. The time of day, seconds
          fraction and time zone offset are optional. The default time zone
          is UTC.
    """
    date_time_values = self._CopyDateTimeFromString(time_string)

    year = date_time_values.get(u'year', 0)
    month = date_time_values.get(u'month', 0)
    day_of_month = date_time_values.get(u'day_of_month', 0)
    hours = date_time_values.get(u'hours', 0)
    minutes = date_time_values.get(u'minutes', 0)
    seconds = date_time_values.get(u'seconds', 0)

    self._number_of_seconds = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds)

    self._microseconds = date_time_values.get(u'microseconds', None)

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
      return self._number_of_seconds, self._microseconds * 10

    return self._number_of_seconds, None

  def GetPlasoTimestamp(self):
    """Retrieves a timestamp that is compatible with plaso.

    Returns:
      int: a POSIX timestamp in microseconds or None on error.
    """
    if self._number_of_seconds is None:
      return

    if self._microseconds is not None:
      return (self._number_of_seconds * 1000000) + self._microseconds

    return self._number_of_seconds * 1000000
