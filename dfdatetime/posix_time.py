# -*- coding: utf-8 -*-
"""POSIX timestamp implementation."""

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
    is_local_time (bool): True if the date and time value is in local time.
    precision (str): precision of the date and time value, which should
        be one of the PRECISION_VALUES in definitions.
    timestamp (int): POSIX timestamp.
  """

  def __init__(self, timestamp=None):
    """Initializes a POSIX timestamp.

    Args:
      timestamp (Optional[int]): POSIX timestamp.
    """
    super(PosixTime, self).__init__()
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

    self.timestamp = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds)

    self.is_local_time = False

  def CopyToStatTimeTuple(self):
    """Copies the POSIX timestamp to a stat timestamp tuple.

    Returns:
      tuple[int, int]: a POSIX timestamp in seconds and the remainder in
          100 nano seconds or (None, None) on error.
    """
    if self.timestamp is None:
      return None, None

    return self.timestamp, None

  def GetPlasoTimestamp(self):
    """Retrieves a timestamp that is compatible with plaso.

    Returns:
      int: a POSIX timestamp in microseconds or None on error.
    """
    if self.timestamp is None:
      return

    return self.timestamp * 1000000


class PosixTimeInMicroseconds(interface.DateTimeValues):
  """Class that implements a POSIX timestamp in microseconds.

  Variant of the POSIX timestamp in microseconds.

  Attributes:
    is_local_time (bool): True if the date and time value is in local time.
    precision (str): precision of the date and time value, which should
        be one of the PRECISION_VALUES in definitions.
    timestamp (int): POSIX timestamp in microseconds.
  """

  def __init__(self, timestamp=None):
    """Initializes a POSIX timestamp in microseconds.

    Args:
      timestamp (Optional[int]): POSIX timestamp in microseconds.
    """
    super(PosixTimeInMicroseconds, self).__init__()
    self.precision = definitions.PRECISION_1_MICROSECOND
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
    microseconds = date_time_values.get(u'microseconds', 0)

    self.timestamp = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds)
    self.timestamp *= 1000000
    self.timestamp += microseconds

    self.is_local_time = False

  def CopyToStatTimeTuple(self):
    """Copies the POSIX timestamp to a stat timestamp tuple.

    Returns:
      tuple[int, int]: a POSIX timestamp in seconds and the remainder in
          100 nano seconds or (None, None) on error.
    """
    if self.timestamp is None:
      return None, None

    timestamp, microseconds = divmod(self.timestamp, 1000000)
    return timestamp, microseconds * 10

  def GetPlasoTimestamp(self):
    """Retrieves a timestamp that is compatible with plaso.

    Returns:
      int: a POSIX timestamp in microseconds or None on error.
    """
    if self.timestamp is None:
      return

    return self.timestamp
