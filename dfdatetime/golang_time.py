# -*- coding: utf-8 -*-
"""Golang time.Time time implementation."""

import decimal

from dfdatetime import definitions
from dfdatetime import factory
from dfdatetime import interface


class GolangTimeEpoch(interface.DateTimeEpoch):
  """Golang time.Time epoch."""

  def __init__(self):
    """Initializes a Golang time.Time epoch."""
    super(GolangTimeEpoch, self).__init__(1, 1, 1)


class GolangTime(interface.DateTimeValues):
  """Golang time.Time timestamp.

  A Golang time.Time timestamp contans the number of nanoseconds since
  January 1, 1 UTC. Depending on the version of the timestamp, the time
  zone is stored in minutes or seconds relative to UTC.

  A serialized version 1 Golang time.Time timestamp is a 15 byte value
  that consists of:

  * byte 0 - version as an 8-bit integer.
  * bytes 1-8 - number of seconds since January 1, 1 as a little-endian signed
      integer.
  * bytes 9-12 - faction of second, number of nanoseconds as a little-endian
      signed integer.
  * bytes 13-14 - time zone offset in minutes as a 16-bit little endian integer,
      where -1 represents UTC.

  A serialized version 2 Golang time.Time timestamp is a 16 byte value
  that consists of:

  * byte 0 - version as an 8-bit integer.
  * bytes 1-8 - number of seconds since January 1, 1 as a little-endian signed
      integer.
  * bytes 9-12 - faction of second, number of nanoseconds as a little-endian
      signed integer.
  * bytes 13-14 - time zone offset in minutes as a 16-bit little endian integer,
      where -1 represents UTC.
  * byte 15 - time zone offset in seconds as an 8-bit integer.

  Attributes:
    is_local_time (bool): True if the date and time value is in local time
  """

  # The delta between January 1, 1970 (unix epoch) and January 1, 1
  # (Golang epoch)
  _GOLANG_TO_POSIX_BASE = (
      ((1969 * 365) + (1969 // 4) - (1969 // 100) + (1969 // 400)) *
      definitions.SECONDS_PER_DAY)

  _EPOCH = GolangTimeEpoch()

  def __init__(self,
      seconds=None, nanoseconds=None, time_zone_offset=None,
      time_zone_seconds=None):
    """Initializes a Golang time.Time timestamp.

    Args:
      seconds (Optional[int]): seconds since epoch.
      nanoseconds (Optional[int]): nanoseconds component.
      time_zone_offset (Optional[int]): the time zone in minutes, -1 is a
          special value for UTC (no Location set).
      time_zone_seconds (Optional[int]): the time zone in seconds. Only valid
          for version 2 time zones.
    """
    super(GolangTime, self).__init__(time_zone_offset=time_zone_offset or 0)
    self._nanoseconds = nanoseconds
    self._precision = definitions.PRECISION_1_NANOSECOND
    self._seconds = seconds
    self._time_zone_seconds = 0

    if time_zone_offset != -1:
      self._time_zone_seconds = time_zone_seconds

  def _GetNormalizedTimestamp(self):
    """Retrieves the normalized timestamp.

    Returns:
      decimal.Decimal: normalized timestamp, which contains the number of
          seconds since January 1, 1970 00:00:00 and a fraction of second used
          for increased precision, or None if the normalized timestamp cannot be
          determined.
    """
    if self._normalized_timestamp is None:
      if (self._seconds is not None and
          self._seconds >= self._GOLANG_TO_POSIX_BASE and
          self._nanoseconds is not None and self._nanoseconds >= 0):

        self._normalized_timestamp = decimal.Decimal(
            self._seconds - GolangTime._GOLANG_TO_POSIX_BASE)

        if self._nanoseconds is not None and self._nanoseconds >= 0:
          self._normalized_timestamp += (
              decimal.Decimal(self._nanoseconds) /
              definitions.NANOSECONDS_PER_SECOND)

    return self._normalized_timestamp

  def CopyFromDateTimeString(self, time_string):
    """Copies a date time value from a date and time string.

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

    if year < 0:
      raise ValueError('Year value not supported: {0!s}.'.format(year))

    seconds = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds)

    seconds += self._GOLANG_TO_POSIX_BASE
    nanoseconds = microseconds * definitions.NANOSECONDS_PER_MICROSECOND

    self._normalized_timestamp = None
    self._seconds = seconds
    self._nanoseconds = nanoseconds
    self._time_zone_offset = time_zone_offset

  def CopyToDateTimeString(self):
    """Copies the Golang time value to a date and time string.

    Returns:
      str: date and time value formatted as: "YYYY-MM-DD hh:mm:ss.######" or
          None if the timestamp cannot be copied to a date and time string.
    """
    if self._seconds is None or self._seconds < 0:
      return None

    seconds = self._seconds
    nanoseconds_seconds, remainder = divmod(
        self._nanoseconds, definitions.NANOSECONDS_PER_SECOND)

    seconds += nanoseconds_seconds
    remainder = remainder // definitions.NANOSECONDS_PER_MICROSECOND
    number_of_days, hours, minutes, seconds = self._GetTimeValues(seconds)

    year, month, day_of_month = self._GetDateValuesWithEpoch(
        number_of_days, self._EPOCH)

    return '{0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}.{6:06d}'.format(
        year, month, day_of_month, hours, minutes, seconds, remainder)


factory.Factory.RegisterDateTimeValues(GolangTime)
