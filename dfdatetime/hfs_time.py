# -*- coding: utf-8 -*-
"""HFS time implementation."""

from __future__ import unicode_literals

from dfdatetime import definitions
from dfdatetime import interface


class HFSTimeEpoch(interface.DateTimeEpoch):
  """HFS time epoch."""

  def __init__(self):
    """Initializes a HFS time epoch."""
    super(HFSTimeEpoch, self).__init__(1904, 1, 1)


class HFSTime(interface.DateTimeValues):
  """HFS timestamp.

  The HFS timestamp is an unsigned 32-bit integer that contains the number of
  seconds since 1904-01-01 00:00:00. Where in HFS the timestamp is typically
  in local time and in HFS+/HFSX in UTC.

  Attributes:
    is_local_time (bool): True if the date and time value is in local time.
    precision (str): precision of the date and time value, which should
        be one of the PRECISION_VALUES in definitions.
  """
  _EPOCH = HFSTimeEpoch()

  # The difference between Jan 1, 1904 and Jan 1, 1970 in seconds.
  _HFS_TO_POSIX_BASE = 2082844800

  def __init__(self, timestamp=None):
    """Initializes a HFS timestamp.

    Args:
      timestamp (Optional[int]): HFS timestamp.
    """
    super(HFSTime, self).__init__()
    self._timestamp = timestamp
    self.precision = definitions.PRECISION_1_SECOND

  @property
  def timestamp(self):
    """int: HFS timestamp or None if timestamp is not set."""
    return self._timestamp

  def _GetNormalizedTimestamp(self):
    """Retrieves the normalized timestamp.

    Returns:
      float: normalized timestamp, which contains the number of seconds since
          January 1, 1970.
    """
    if not self._normalized_timestamp:
      if (self._timestamp is not None and self._timestamp >= 0 and
          self._timestamp <= self._UINT32_MAX):
        self._normalized_timestamp = (
            float(self._timestamp) - self._HFS_TO_POSIX_BASE)

    return self._normalized_timestamp

  def GetPlasoTimestamp(self):
    """Retrieves a timestamp that is compatible with plaso.

    Returns:
      int: a POSIX timestamp in microseconds or None on error.
    """
    if (self._timestamp is None or self._timestamp < 0 or
        self._timestamp > self._UINT32_MAX):
      return

    timestamp = self._timestamp - self._HFS_TO_POSIX_BASE
    return timestamp * definitions.MICROSECONDS_PER_SECOND

  def CopyFromDateTimeString(self, time_string):
    """Copies a HFS timestamp from a date and time string.

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

    if year < 1904 or year > 2040:
      raise ValueError('Year value not supported.')

    self._normalized_timestamp = None
    self._timestamp = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds)
    self._timestamp += self._HFS_TO_POSIX_BASE

    self.is_local_time = False

  def CopyToDateTimeString(self):
    """Copies the HFS timestamp to a date and time string.

    Returns:
      str: date and time value formatted as:
          YYYY-MM-DD hh:mm:ss
    """
    if (self._timestamp is None or self._timestamp < 0 or
        self._timestamp > self._UINT32_MAX):
      return

    number_of_days, hours, minutes, seconds = self._GetTimeValues(
        self._timestamp)

    year, month, day_of_month = self._GetDateValuesWithEpoch(
        number_of_days, self._EPOCH)

    return '{0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}'.format(
        year, month, day_of_month, hours, minutes, seconds)

  def GetDate(self):
    """Retrieves the date represented by the date and time values.

    Returns:
       tuple[int, int, int]: year, month, day of month or (None, None, None)
           if the date and time values do not represent a date.
    """
    if (self.timestamp is None or self.timestamp < 0 or
        self.timestamp > self._UINT32_MAX):
      return None, None, None

    try:
      number_of_days, _, _, _ = self._GetTimeValues(self.timestamp)
      return self._GetDateValuesWithEpoch(number_of_days, self._EPOCH)

    except ValueError:
      return None, None, None
