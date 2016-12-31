# -*- coding: utf-8 -*-
"""UUID version 1 timestamp implementation."""

from dfdatetime import definitions
from dfdatetime import interface


class UUIDTime(interface.DateTimeValues):
  """Class that implements an UUID version 1 timestamp.

  The UUID version 1 timestamp is an unsigned 60-bit value that contains
  the number of 100th nano seconds intervals since 1582-10-15 00:00:00.

  Also see:
    https://en.wikipedia.org/wiki/Universally_unique_identifier

  Attributes:
    is_local_time (bool): True if the date and time value is in local time.
    precision (str): precision of the date and time value, which should
        be one of the PRECISION_VALUES in definitions.
    timestamp (int): UUID timestamp.
  """
  # The difference between Oct 15, 1582 and Jan 1, 1970 in seconds.
  _UUID_TO_POSIX_BASE = 12219292800
  _UINT60_MAX = (1 << 60) - 1

  def __init__(self, timestamp=None):
    """Initializes an UUID version 1 timestamp.

    Args:
      timestamp (Optional[int]): UUID version 1 timestamp.

    Raises:
      ValueError: if the UUID version 1 timestamp is invalid.
    """
    if timestamp and (timestamp < 0 or timestamp > self._UINT60_MAX):
      raise ValueError(u'Invalid UUID version 1 timestamp.')

    super(UUIDTime, self).__init__()
    self.precision = definitions.PRECISION_100_NANOSECONDS
    self.timestamp = timestamp

  def CopyFromString(self, time_string):
    """Copies an UUID timestamp from a string containing a date and time value.

    Args:
      time_string (str): date and time value formatted as:
          YYYY-MM-DD hh:mm:ss.######[+-]##:##

          Where # are numeric digits ranging from 0 to 9 and the seconds
          fraction can be either 3 or 6 digits. The time of day, seconds
          fraction and time zone offset are optional. The default time zone
          is UTC.

    Raises:
      ValueError: if the time string is invalid or not supported.
    """
    date_time_values = self._CopyDateTimeFromString(time_string)

    year = date_time_values.get(u'year', 0)
    month = date_time_values.get(u'month', 0)
    day_of_month = date_time_values.get(u'day_of_month', 0)
    hours = date_time_values.get(u'hours', 0)
    minutes = date_time_values.get(u'minutes', 0)
    seconds = date_time_values.get(u'seconds', 0)

    if year < 1582:
      raise ValueError(u'Year value not supported.')

    self.timestamp = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds)
    self.timestamp += self._UUID_TO_POSIX_BASE
    self.timestamp *= 1000000
    self.timestamp += date_time_values.get(u'microseconds', 0)
    self.timestamp *= 10

    self.is_local_time = False

  def CopyToStatTimeTuple(self):
    """Copies the UUID timestamp to a stat timestamp tuple.

    Returns:
      tuple[int, int]: a POSIX timestamp in seconds and the remainder in
          100 nano seconds or (None, None) on error.
    """
    if (self.timestamp is None or self.timestamp < 0 or
        self.timestamp > self._UINT60_MAX):
      return None, None

    timestamp, remainder = divmod(self.timestamp, 10000000)
    timestamp -= self._UUID_TO_POSIX_BASE
    return timestamp, remainder

  def GetPlasoTimestamp(self):
    """Retrieves a timestamp that is compatible with plaso.

    Returns:
      int: a POSIX timestamp in microseconds or None on error.
    """
    if (self.timestamp is None or self.timestamp < 0 or
        self.timestamp > self._UINT60_MAX):
      return

    timestamp, _ = divmod(self.timestamp, 10)
    return timestamp - (self._UUID_TO_POSIX_BASE * 1000000)
