# -*- coding: utf-8 -*-
"""FILETIME timestamp implementation."""

from dfdatetime import definitions
from dfdatetime import interface


class Filetime(interface.DateTimeValues):
  """Class that implements a FILETIME timestamp.

  The FILETIME timestamp is a 64-bit integer that contains the number
  of 100th nano seconds since 1601-01-01 00:00:00.

  Do not confuse this with the FILETIME structure that consists of
  2 x 32-bit integers and is presumed to be unsigned.

  Attributes:
    is_local_time (bool): True if the date and time value is in local time.
    precision (str): precision of the date and time value, which should
        be one of the PRECISION_VALUES in definitions.
    timestamp (int): FILETIME timestamp.
  """

  # The difference between Jan 1, 1601 and Jan 1, 1970 in seconds.
  _FILETIME_TO_POSIX_BASE = 11644473600
  _UINT64_MAX = (1 << 64) - 1

  def __init__(self, timestamp=None):
    """Initializes a FILETIME timestamp.

    Args:
      timestamp (Optional[int]): FILETIME timestamp.
    """
    super(Filetime, self).__init__()
    self.precision = definitions.PRECISION_100_NANOSECONDS
    self.timestamp = timestamp

  def CopyFromString(self, time_string):
    """Copies a FILETIME from a string containing a date and time value.

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

    if year < 1601:
      raise ValueError(u'Year value not supported: {0!s}.'.format(year))

    self.timestamp = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds)

    self.timestamp += self._FILETIME_TO_POSIX_BASE
    self.timestamp *= 1000000
    self.timestamp += date_time_values.get(u'microseconds', 0)
    self.timestamp *= 10

    self.is_local_time = False

  def CopyToStatTimeTuple(self):
    """Copies the FILETIME timestamp to a stat timestamp tuple.

    Returns:
      tuple[int, int]: a POSIX timestamp in seconds and the remainder in
          100 nano seconds or (None, None) on error.
    """
    if (self.timestamp is None or self.timestamp < 0 or
        self.timestamp > self._UINT64_MAX):
      return None, None

    timestamp, remainder = divmod(self.timestamp, 10000000)
    timestamp -= self._FILETIME_TO_POSIX_BASE
    return timestamp, remainder

  def GetPlasoTimestamp(self):
    """Retrieves a timestamp that is compatible with plaso.

    Returns:
      int: a POSIX timestamp in microseconds or None on error.
    """
    if (self.timestamp is None or self.timestamp < 0 or
        self.timestamp > self._UINT64_MAX):
      return

    timestamp, _ = divmod(self.timestamp, 10)
    return timestamp - (self._FILETIME_TO_POSIX_BASE * 1000000)
