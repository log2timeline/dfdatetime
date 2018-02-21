# -*- coding: utf-8 -*-
"""FILETIME timestamp implementation."""

from __future__ import unicode_literals

from dfdatetime import definitions
from dfdatetime import interface


class FiletimeEpoch(interface.DateTimeEpoch):
  """FILETIME epoch."""

  def __init__(self):
    """Initializes a FILETIME epoch."""
    super(FiletimeEpoch, self).__init__(1601, 1, 1)


class Filetime(interface.DateTimeValues):
  """FILETIME timestamp.

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

  _EPOCH = FiletimeEpoch()

  # The difference between Jan 1, 1601 and Jan 1, 1970 in seconds.
  _FILETIME_TO_POSIX_BASE = 11644473600

  def __init__(self, timestamp=None):
    """Initializes a FILETIME timestamp.

    Args:
      timestamp (Optional[int]): FILETIME timestamp.
    """
    super(Filetime, self).__init__()
    self.precision = definitions.PRECISION_100_NANOSECONDS
    self.timestamp = timestamp

  def CopyFromDateTimeString(self, time_string):
    """Copies a FILETIME timestamp from a date and time string.

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

    year = date_time_values.get('year', 0)
    month = date_time_values.get('month', 0)
    day_of_month = date_time_values.get('day_of_month', 0)
    hours = date_time_values.get('hours', 0)
    minutes = date_time_values.get('minutes', 0)
    seconds = date_time_values.get('seconds', 0)

    if year < 1601:
      raise ValueError('Year value not supported: {0!s}.'.format(year))

    self.timestamp = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds)
    self.timestamp += self._FILETIME_TO_POSIX_BASE
    self.timestamp *= definitions.MICROSECONDS_PER_SECOND
    self.timestamp += date_time_values.get('microseconds', 0)
    self.timestamp *= self._100NS_PER_MICROSECOND

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

    timestamp, remainder = divmod(self.timestamp, self._100NS_PER_SECOND)
    timestamp -= self._FILETIME_TO_POSIX_BASE
    return timestamp, remainder

  def CopyToDateTimeString(self):
    """Copies the FILETIME timestamp to a date and time string.

    Returns:
      str: date and time value formatted as:
          YYYY-MM-DD hh:mm:ss.#######
    """
    if (self.timestamp is None or self.timestamp < 0 or
        self.timestamp > self._UINT64_MAX):
      return

    timestamp, remainder = divmod(self.timestamp, self._100NS_PER_SECOND)
    number_of_days, hours, minutes, seconds = self._GetTimeValues(timestamp)

    year, month, day_of_month = self._GetDateValuesWithEpoch(
        number_of_days, self._EPOCH)

    return '{0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}.{6:07d}'.format(
        year, month, day_of_month, hours, minutes, seconds, remainder)

  def GetDate(self):
    """Retrieves the date represented by the date and time values.

    Returns:
       tuple[int, int, int]: year, month, day of month or (None, None, None)
           if the date and time values do not represent a date.
    """
    if (self.timestamp is None or self.timestamp < 0 or
        self.timestamp > self._UINT64_MAX):
      return None, None, None

    try:
      timestamp, _ = divmod(self.timestamp, self._100NS_PER_SECOND)
      number_of_days, _, _, _ = self._GetTimeValues(timestamp)
      return self._GetDateValuesWithEpoch(number_of_days, self._EPOCH)

    except ValueError:
      return None, None, None

  def GetPlasoTimestamp(self):
    """Retrieves a timestamp that is compatible with plaso.

    Returns:
      int: a POSIX timestamp in microseconds or None on error.
    """
    if (self.timestamp is None or self.timestamp < 0 or
        self.timestamp > self._UINT64_MAX):
      return

    timestamp, _ = divmod(self.timestamp, self._100NS_PER_MICROSECOND)
    return timestamp - (
        self._FILETIME_TO_POSIX_BASE * definitions.MICROSECONDS_PER_SECOND)
