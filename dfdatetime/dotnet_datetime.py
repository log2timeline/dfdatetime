# -*- coding: utf-8 -*-
""".NET DateTime implementation."""

import decimal

from dfdatetime import definitions
from dfdatetime import factory
from dfdatetime import interface


class DotNetDateTimeEpoch(interface.DateTimeEpoch):
  """.NET DateTime epoch."""

  def __init__(self):
    """Initializes a .NET DateTime epoch."""
    super(DotNetDateTimeEpoch, self).__init__(1, 1, 1)


class DotNetDateTime(interface.DateTimeValues):
  """.NET DateTime ticks.

  The .NET DateTime timestamp is a 64-bit signed integer that contains the date
  and time as the number of 100 nanoseconds since 12:00 AM January 1, year
  1 A.D. in the proleptic Gregorian Calendar.
  """
  _EPOCH = DotNetDateTimeEpoch()

  # The difference between January 1, 1 and January 1, 1970 in seconds.
  _DOTNET_TO_POSIX_BASE =  (
      ((1969 * 365) + (1969 // 4) - (1969 // 100) + (1969 // 400)) *
      definitions.SECONDS_PER_DAY)

  def __init__(self, precision=None, time_zone_offset=None, timestamp=None):
    """Initializes a .NET DateTime timestamp.

    Args:
      precision (Optional[str]): precision of the date and time value, which
          should be one of the PRECISION_VALUES in definitions.
      time_zone_offset (Optional[int]): time zone offset in number of minutes
          from UTC or None if not set.
      timestamp (Optional[int]): .NET DateTime ticks.
    """
    super(DotNetDateTime, self).__init__(
        precision=precision or definitions.PRECISION_100_NANOSECONDS,
        time_zone_offset=time_zone_offset)
    self._timestamp = timestamp or 0

  @property
  def timestamp(self):
    """integer: .NET DateTime timestamp or None if not set."""
    return self._timestamp

  def _GetNormalizedTimestamp(self):
    """Retrieves the normalized timestamp.

    Returns:
      decimal.Decimal: normalized timestamp, which contains the number of
          seconds since January 1, 1970 00:00:00 and a fraction of second used
          for increased precision, or None if the normalized timestamp cannot be
          determined.
    """
    if self._normalized_timestamp is None:
      if self._timestamp is not None:
        self._normalized_timestamp = (
            decimal.Decimal(self._timestamp) / self._100_NANOSECONDS_PER_SECOND)
        self._normalized_timestamp -= self._DOTNET_TO_POSIX_BASE

        if self._time_zone_offset:
          self._normalized_timestamp -= self._time_zone_offset * 60

    return self._normalized_timestamp

  def CopyFromDateTimeString(self, time_string):
    """Copies a .NET DateTime timestamp from a string.

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
    microseconds = date_time_values.get('microseconds', 0)
    time_zone_offset = date_time_values.get('time_zone_offset', 0)

    if year > 9999:
      raise ValueError(f'Unsupported year value: {year:d}.')

    timestamp = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds)
    timestamp += self._DOTNET_TO_POSIX_BASE
    timestamp *= definitions.MICROSECONDS_PER_SECOND
    timestamp += microseconds
    timestamp *= self._100_NANOSECONDS_PER_MICROSECOND

    self._normalized_timestamp = None
    self._timestamp = timestamp
    self._time_zone_offset = time_zone_offset

  def CopyToDateTimeString(self):
    """Copies the .NET DateTime timestamp to a date and time string.

    Returns:
      str: date and time value formatted as: "YYYY-MM-DD hh:mm:ss.######" or
          None if the timestamp is missing.
    """
    if (self._timestamp is None or self._timestamp < 0 or
        self._timestamp > self._UINT64_MAX):
      return None

    timestamp, fraction_of_second = divmod(
        self._timestamp, self._100_NANOSECONDS_PER_SECOND)
    number_of_days, hours, minutes, seconds = self._GetTimeValues(timestamp)

    year, month, day_of_month = self._GetDateValuesWithEpoch(
        number_of_days, self._EPOCH)

    return (f'{year:04d}-{month:02d}-{day_of_month:02d} '
            f'{hours:02d}:{minutes:02d}:{seconds:02d}.{fraction_of_second:07d}')


factory.Factory.RegisterDateTimeValues(DotNetDateTime)
