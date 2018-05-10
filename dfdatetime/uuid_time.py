# -*- coding: utf-8 -*-
"""UUID version 1 time implementation."""

from __future__ import unicode_literals

import decimal

from dfdatetime import definitions
from dfdatetime import interface


class UUIDTimeEpoch(interface.DateTimeEpoch):
  """UUID version 1 time epoch."""

  def __init__(self):
    """Initializes an UUID version 1 time epoch."""
    super(UUIDTimeEpoch, self).__init__(1582, 10, 15)


class UUIDTime(interface.DateTimeValues):
  """UUID version 1 timestamp.

  The UUID version 1 timestamp is an unsigned 60-bit value that contains
  the number of 100th nano seconds intervals since 1582-10-15 00:00:00.

  Also see:
    https://en.wikipedia.org/wiki/Universally_unique_identifier

  Attributes:
    is_local_time (bool): True if the date and time value is in local time.
  """
  _EPOCH = UUIDTimeEpoch()

  # The difference between October 15, 1582 and January 1, 1970 in seconds.
  _UUID_TO_POSIX_BASE = 12219292800

  def __init__(self, timestamp=None):
    """Initializes an UUID version 1 timestamp.

    Args:
      timestamp (Optional[int]): UUID version 1 timestamp.

    Raises:
      ValueError: if the UUID version 1 timestamp is invalid.
    """
    if timestamp and (timestamp < 0 or timestamp > self._UINT60_MAX):
      raise ValueError('Invalid UUID version 1 timestamp.')

    super(UUIDTime, self).__init__()
    self._precision = definitions.PRECISION_100_NANOSECONDS
    self._timestamp = timestamp

  @property
  def timestamp(self):
    """int: UUID timestamp or None if timestamp is not set."""
    return self._timestamp

  def _GetNormalizedTimestamp(self):
    """Retrieves the normalized timestamp.

    Returns:
      decimal.Decimal: normalized timestamp, which contains the number of
          seconds since January 1, 1970 00:00:00 and a fraction of second
          used for increased precision, or None if the normalized timestamp
          cannot be determined.
    """
    if self._normalized_timestamp is None:
      if (self._timestamp is not None and self._timestamp >= 0 and
          self._timestamp <= self._UINT60_MAX):
        self._normalized_timestamp = (
            decimal.Decimal(self._timestamp) / self._100NS_PER_SECOND)
        self._normalized_timestamp -= self._UUID_TO_POSIX_BASE

    return self._normalized_timestamp

  def CopyFromDateTimeString(self, time_string):
    """Copies an UUID timestamp from a date and time string.

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

    if year < 1582:
      raise ValueError('Year value not supported.')

    timestamp = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds)
    timestamp += self._UUID_TO_POSIX_BASE
    timestamp *= definitions.MICROSECONDS_PER_SECOND
    timestamp += date_time_values.get('microseconds', 0)
    timestamp *= self._100NS_PER_MICROSECOND

    self._normalized_timestamp = None
    self._timestamp = timestamp
    self.is_local_time = False

  def CopyToDateTimeString(self):
    """Copies the UUID timestamp to a date and time string.

    Returns:
      str: date and time value formatted as: "YYYY-MM-DD hh:mm:ss.#######" or
          None if the timestamp is missing or invalid.
    """
    if (self._timestamp is None or self._timestamp < 0 or
        self._timestamp > self._UINT60_MAX):
      return None

    timestamp, remainder = divmod(self._timestamp, self._100NS_PER_SECOND)
    number_of_days, hours, minutes, seconds = self._GetTimeValues(timestamp)

    year, month, day_of_month = self._GetDateValuesWithEpoch(
        number_of_days, self._EPOCH)

    return '{0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}.{6:07d}'.format(
        year, month, day_of_month, hours, minutes, seconds, remainder)
