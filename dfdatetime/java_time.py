# -*- coding: utf-8 -*-
"""Java java.util.Date timestamp implementation."""

from dfdatetime import definitions
from dfdatetime import interface


class JavaTime(interface.DateTimeValues):
  """Class that implements a Java java.util.Date timestamp.

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
  _INT64_MIN = -(1 << 63)
  _INT64_MAX = (1 << 63) - 1

  def __init__(self, timestamp=None):
    """Initializes a Java timestamp.

    Args:
      timestamp (Optional[int]): Java timestamp.
    """
    super(JavaTime, self).__init__()
    self.precision = definitions.PRECISION_1_MILLISECOND
    self.timestamp = timestamp

  def CopyFromString(self, time_string):
    """Copies a Java timestamp from a string containing a date and time value.

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
    microseconds = date_time_values.get(u'microseconds', None)

    self.timestamp = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds)
    self.timestamp *= 1000

    if microseconds:
      milliseconds, _ = divmod(microseconds, 1000)
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

    timestamp, milliseconds = divmod(self.timestamp, 1000)
    return timestamp, milliseconds * 10000

  def GetPlasoTimestamp(self):
    """Retrieves a timestamp that is compatible with plaso.

    Returns:
      int: a POSIX timestamp in microseconds or None on error.
    """
    if (self.timestamp is None or self.timestamp < self._INT64_MIN or
        self.timestamp > self._INT64_MAX):
      return

    return self.timestamp * 1000
