# -*- coding: utf-8 -*-
"""UUID version 1 time implementation."""

import decimal

from dfdatetime import definitions
from dfdatetime import factory
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

  def __init__(self, precision=None, time_zone_offset=None, timestamp=None):
    """Initializes an UUID version 1 timestamp.

    Args:
      precision (Optional[str]): precision of the date and time value, which
          should be one of the PRECISION_VALUES in definitions.
      time_zone_offset (Optional[int]): time zone offset in number of minutes
          from UTC or None if not set.
      timestamp (Optional[int]): UUID version 1 timestamp.

    Raises:
      ValueError: if the UUID version 1 timestamp is invalid.
    """
    if timestamp and (timestamp < 0 or timestamp > self._UINT60_MAX):
      raise ValueError('Invalid UUID version 1 timestamp.')

    super(UUIDTime, self).__init__(
        precision=precision or definitions.PRECISION_100_NANOSECONDS,
        time_zone_offset=time_zone_offset)
    self._timestamp = timestamp

  @property
  def timestamp(self):
    """int: UUID timestamp or None if not set."""
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
            decimal.Decimal(self._timestamp) / self._100_NANOSECONDS_PER_SECOND)
        self._normalized_timestamp -= self._UUID_TO_POSIX_BASE

        if self._time_zone_offset:
          self._normalized_timestamp -= self._time_zone_offset * 60

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
    time_zone_offset = date_time_values.get('time_zone_offset', 0)

    if year < 1582:
      raise ValueError('Year value not supported.')

    timestamp = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds)
    timestamp += self._UUID_TO_POSIX_BASE
    timestamp *= definitions.MICROSECONDS_PER_SECOND
    timestamp += date_time_values.get('microseconds', 0)
    timestamp *= self._100_NANOSECONDS_PER_MICROSECOND

    self._normalized_timestamp = None
    self._timestamp = timestamp
    self._time_zone_offset = time_zone_offset

  def CopyToDateTimeString(self):
    """Copies the UUID timestamp to a date and time string.

    Returns:
      str: date and time value formatted as: "YYYY-MM-DD hh:mm:ss.#######" or
          None if the timestamp is missing or invalid.
    """
    if (self._timestamp is None or self._timestamp < 0 or
        self._timestamp > self._UINT60_MAX):
      return None

    timestamp, fraction_of_second = divmod(
        self._timestamp, self._100_NANOSECONDS_PER_SECOND)
    number_of_days, hours, minutes, seconds = self._GetTimeValues(timestamp)

    year, month, day_of_month = self._GetDateValuesWithEpoch(
        number_of_days, self._EPOCH)

    return (f'{year:04d}-{month:02d}-{day_of_month:02d} '
            f'{hours:02d}:{minutes:02d}:{seconds:02d}.{fraction_of_second:07d}')


factory.Factory.RegisterDateTimeValues(UUIDTime)
