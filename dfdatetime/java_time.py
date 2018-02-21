# -*- coding: utf-8 -*-
"""Java java.util.Date timestamp implementation."""

from __future__ import unicode_literals

from dfdatetime import definitions
from dfdatetime import interface
from dfdatetime import posix_time


class JavaTime(interface.DateTimeValues):
  """Java java.util.Date timestamp.

  The Java java.util.Date timestamp is a signed integer that contains the
  number of milliseconds since 1970-01-01 00:00:00 (also known as the POSIX
  epoch). Negative values represent date and times predating the POSIX epoch.

  Also see:
    https://docs.oracle.com/javase/8/docs/api/java/util/Date.html

  Attributes:
    is_local_time (bool): True if the date and time value is in local time.
    precision (str): precision of the date and time value, which should
        be one of the PRECISION_VALUES in definitions.
    timestamp (int): Java timestamp.
  """

  _EPOCH = posix_time.PosixTimeEpoch()

  def __init__(self, timestamp=None):
    """Initializes a Java timestamp.

    Args:
      timestamp (Optional[int]): Java timestamp.
    """
    super(JavaTime, self).__init__()
    self.precision = definitions.PRECISION_1_MILLISECOND
    self.timestamp = timestamp

  def CopyFromDateTimeString(self, time_string):
    """Copies a Java timestamp from a date and time string.

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
    microseconds = date_time_values.get('microseconds', None)

    self.timestamp = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds)
    self.timestamp *= definitions.MILLISECONDS_PER_SECOND

    if microseconds:
      milliseconds, _ = divmod(
          microseconds, definitions.MILLISECONDS_PER_SECOND)
      self.timestamp += milliseconds

    self.is_local_time = False

  def CopyToStatTimeTuple(self):
    """Copies the Java timestamp to a stat timestamp tuple.

    Returns:
      tuple[int, int]: a POSIX timestamp in seconds and the remainder in
          100 nano seconds or (None, None) on error.
    """
    if (self.timestamp is None or self.timestamp < self._INT64_MIN or
        self.timestamp > self._INT64_MAX):
      return None, None

    timestamp, milliseconds = divmod(
        self.timestamp, definitions.MILLISECONDS_PER_SECOND)
    return timestamp, milliseconds * self._100NS_PER_MILLISECOND

  def CopyToDateTimeString(self):
    """Copies the Java timestamp to a date and time string.

    Returns:
      str: date and time value formatted as:
          YYYY-MM-DD hh:mm:ss.###
    """
    if (self.timestamp is None or self.timestamp < self._INT64_MIN or
        self.timestamp > self._INT64_MAX):
      return

    timestamp, milliseconds = divmod(
        self.timestamp, definitions.MILLISECONDS_PER_SECOND)
    number_of_days, hours, minutes, seconds = self._GetTimeValues(timestamp)

    year, month, day_of_month = self._GetDateValuesWithEpoch(
        number_of_days, self._EPOCH)

    return '{0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}.{6:03d}'.format(
        year, month, day_of_month, hours, minutes, seconds, milliseconds)

  def GetDate(self):
    """Retrieves the date represented by the date and time values.

    Returns:
       tuple[int, int, int]: year, month, day of month or (None, None, None)
           if the date and time values do not represent a date.
    """
    if (self.timestamp is None or self.timestamp < self._INT64_MIN or
        self.timestamp > self._INT64_MAX):
      return None, None, None

    try:
      timestamp, _ = divmod(self.timestamp, definitions.MILLISECONDS_PER_SECOND)
      number_of_days, _, _, _ = self._GetTimeValues(timestamp)
      return self._GetDateValuesWithEpoch(number_of_days, self._EPOCH)

    except ValueError:
      return None, None, None

  def GetPlasoTimestamp(self):
    """Retrieves a timestamp that is compatible with plaso.

    Returns:
      int: a POSIX timestamp in microseconds or None on error.
    """
    if (self.timestamp is None or self.timestamp < self._INT64_MIN or
        self.timestamp > self._INT64_MAX):
      return

    return self.timestamp * definitions.MICROSECONDS_PER_MILLISECOND
