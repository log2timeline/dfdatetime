# -*- coding: utf-8 -*-
"""Fake timestamp implementation."""

import calendar
import time

from dfdatetime import interface


class FakeTime(interface.DateTimeValues):
  """Class that implements a fake timestamp."""

  def __init__(self):
    """Initializes the fake timestamp object."""
    super(FakeTime, self).__init__()
    # Note that time.time() and divmod return floating point values.
    timestamp, fraction_of_seconds = divmod(time.time(), 1)
    self._microseconds = int(fraction_of_seconds * 1000000)
    self._timestamp = int(timestamp)

  def CopyFromString(self, time_string):
    """Copies a fake timestamp from a string containing a date and time value.

    Args:
      time_string (str): date and time value formatted as:
          YYYY-MM-DD hh:mm:ss.######[+-]##:##

          Where # are numeric digits ranging from 0 to 9 and the seconds
          fraction can be either 3 or 6 digits. The time of day, seconds
          fraction and timezone offset are optional. The default timezone
          is UTC.

    Raises:
      ValueError: if the time string is invalid or not supported.
    """
    date_time_values = self._CopyDateTimeFromString(time_string)

    self._timestamp = int(calendar.timegm((
        date_time_values.get(u'year', 0),
        date_time_values.get(u'month', 0),
        date_time_values.get(u'day_of_month', 0),
        date_time_values.get(u'hours', 0),
        date_time_values.get(u'minutes', 0),
        date_time_values.get(u'seconds', 0))))

    timezone_offset = date_time_values.get(u'timezone_offset', None)
    if timezone_offset:
      self._timestamp += timezone_offset

    self._microseconds = date_time_values.get(u'microseconds', None)

  def CopyToStatTimeTuple(self):
    """Copies the fake timestamp to a stat timestamp tuple.

    Returns:
      tuple[int, int]: a POSIX timestamp in seconds and the remainder in
          100 nano seconds or (None, None) on error.
    """
    if self._timestamp is None:
      return None, None

    if self._microseconds is not None:
      return self._timestamp, self._microseconds * 10

    return self._timestamp, 0

  def GetPlasoTimestamp(self):
    """Retrieves a timestamp that is compatible with plaso.

    Returns:
      int: a POSIX timestamp in microseconds or None on error.
    """
    if self._microseconds is not None:
      return (self._timestamp * 1000000) + self._microseconds
    return self._timestamp * 1000000
