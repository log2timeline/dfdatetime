# -*- coding: utf-8 -*-
"""POSIX timestamp implementation."""

import calendar

from dfdatetime import definitions
from dfdatetime import interface


class PosixTime(interface.DateTimeValues):
  """Class that implements a POSIX timestamp.

  The POSIX timestamp is a signed integer that contains the number of
  seconds since 1970-01-01 00:00:00 (also known as the POSIX epoch).
  Negative values represent date and times predating the POSIX epoch.

  The POSIX timestamp was initially 32-bit though 64-bit variants
  are known to be used.

  Attributes:
    micro_seconds (int): number of microseconds
    precision (str): precision of the date and time value, which should
        be one of the PRECISION_VALUES in definitions.
    timestamp (int): POSIX timestamp.
    time_zone (str): time zone the date and time values are in.
  """

  def __init__(self, microseconds=None, timestamp=None):
    """Initializes a POSIX timestamp object.

    Args:
      micro_seconds (Optional[int]): number of microseconds.
      timestamp (Optional[int]): POSIX timestamp.
    """
    super(PosixTime, self).__init__()
    self.microseconds = microseconds
    if microseconds is not None:
      self.precision = definitions.PRECISION_1_MICROSECOND
    else:
      self.precision = definitions.PRECISION_1_SECOND
    self.timestamp = timestamp

  def CopyFromString(self, time_string):
    """Copies a POSIX timestamp from a string containing a date and time value.

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

    time_tuple = (year, month, day_of_month, hours, minutes, seconds)
    self.timestamp = calendar.timegm(time_tuple)
    self.timestamp = int(self.timestamp)

    self.microseconds = date_time_values.get(u'microseconds', None)

    if self.microseconds is not None:
      self.precision = definitions.PRECISION_1_MICROSECOND
    else:
      self.precision = definitions.PRECISION_1_SECOND

    self.time_zone = u'UTC'

  def CopyToStatTimeTuple(self):
    """Copies the POSIX timestamp to a stat timestamp tuple.

    Returns:
      tuple[int, int]: a POSIX timestamp in seconds and the remainder in
          100 nano seconds or (None, None) on error.
    """
    if self.timestamp is None:
      return None, None

    if self.microseconds is not None:
      return self.timestamp, self.microseconds * 10

    return self.timestamp, None

  def GetPlasoTimestamp(self):
    """Retrieves a timestamp that is compatible with plaso.

    Returns:
      int: a POSIX timestamp in microseconds or None on error.
    """
    if self.timestamp is None:
      return

    if self.microseconds is not None:
      return (self.timestamp * 1000000) + self.microseconds

    return self.timestamp * 1000000
