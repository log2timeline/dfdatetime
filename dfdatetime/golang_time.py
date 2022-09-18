# -*- coding: utf-8 -*-
"""Golang time.Time timestamp implementation."""

import decimal
import struct

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

  A Golang time.Time timestamp contains the number of nanoseconds since
  January 1, 1 UTC. Depending on the version of the timestamp, the time
  zone is stored in minutes or seconds relative to UTC.

  A serialized version 1 Golang time.Time timestamp is a 15 byte value
  that consists of:

  * byte 0 - version as an 8-bit integer.
  * bytes 1-8 - number of seconds since January 1, 1 as a big-endian signed
      integer.
  * bytes 9-12 - fraction of second, number of nanoseconds as a big-endian
      signed integer.
  * bytes 13-14 - time zone offset in minutes as a 16-bit big endian integer,
      where -1 represents UTC.

  A serialized version 2 Golang time.Time timestamp is a 16 byte value
  that consists of:

  * byte 0 - version as an 8-bit integer.
  * bytes 1-8 - number of seconds since January 1, 1 as a big-endian signed
      integer.
  * bytes 9-12 - fraction of second, number of nanoseconds as a big-endian
      signed integer.
  * bytes 13-14 - time zone offset in minutes as a 16-bit big endian integer,
      where -1 represents UTC.
  * byte 15 - time zone offset in seconds as an 8-bit integer.

  Attributes:
    is_local_time (bool): True if the date and time value is in local time
  """

  # The delta between January 1, 1970 (unix epoch) and January 1, 1
  # (Golang epoch).
  _GOLANG_TO_POSIX_BASE = (
      ((1969 * 365) + (1969 // 4) - (1969 // 100) + (1969 // 400)) *
      definitions.SECONDS_PER_DAY)

  _EPOCH = GolangTimeEpoch()

  def __init__(self, golang_timestamp=None, precision=None):
    """Initializes a Golang time.Time timestamp.

    Args:
      golang_timestamp (Optional[bytes]): the Golang time.Time timestamp.
      precision (Optional[str]): precision of the date and time value, which
          should be one of the PRECISION_VALUES in definitions.
    """
    number_of_seconds, nanoseconds, time_zone_offset = (None, None, None)
    if golang_timestamp is not None:
      number_of_seconds, nanoseconds, time_zone_offset = (
          self._GetNumberOfSeconds(golang_timestamp))

    super(GolangTime, self).__init__(
        precision=precision or definitions.PRECISION_1_NANOSECOND,
        time_zone_offset=time_zone_offset)
    self._golang_timestamp = golang_timestamp
    self._nanoseconds = nanoseconds
    self._number_of_seconds = number_of_seconds

    if time_zone_offset:
      self.is_local_time = True

  @property
  def golang_timestamp(self):
    """int: Golang time.Time timestamp or None if not set."""
    return self._golang_timestamp

  def _GetNormalizedTimestamp(self):
    """Retrieves the normalized timestamp.

    Returns:
      decimal.Decimal: normalized timestamp, which contains the number of
          seconds since January 1, 1970 00:00:00 and a fraction of second used
          for increased precision, or None if the normalized timestamp cannot be
          determined.
    """
    if self._normalized_timestamp is None:
      if (self._number_of_seconds is not None and
          self._number_of_seconds >= self._GOLANG_TO_POSIX_BASE and
          self._nanoseconds is not None and self._nanoseconds >= 0):

        self._normalized_timestamp = decimal.Decimal(
            self._number_of_seconds - GolangTime._GOLANG_TO_POSIX_BASE)

        if self._nanoseconds is not None and self._nanoseconds >= 0:
          self._normalized_timestamp += (
              decimal.Decimal(self._nanoseconds) /
              definitions.NANOSECONDS_PER_SECOND)

    return self._normalized_timestamp

  def _GetNumberOfSeconds(self, golang_timestamp):
    """Retrieves the number of seconds from a Golang time.Time timestamp.

    Args:
      golang_timestamp (bytes): the Golang time.Time timestamp.

    Returns:
      tuple[int, int, int]: number of seconds since January 1, 1 00:00:00,
          fraction of second in nanoseconds and time zone offset in minutes.

    Raises:
      ValueError: if the Golang time.Time timestamp could not be parsed.
    """
    byte_size = len(golang_timestamp)
    if byte_size < 15:
      raise ValueError('Unsupported Golang time.Time timestamp.')

    version = golang_timestamp[0]
    if version not in (1, 2):
      raise ValueError(
          f'Unsupported Golang time.Time timestamp version: {version:d}.')

    if (version == 1 and byte_size != 15) or (version == 2 and byte_size != 16):
      raise ValueError('Unsupported Golang time.Time timestamp.')

    try:
      number_of_seconds, nanoseconds, time_zone_offset = struct.unpack(
          '>qih', golang_timestamp[1:15])

      # TODO: add support for version 2 time zone offset in seconds

    except struct.error as exception:
      raise ValueError((
          f'Unable to unpacked Golang time.Time timestamp with error: '
          f'{exception!s}'))

    # A time zone offset of -1 minute is a special representation for UTC.
    if time_zone_offset == -1:
      time_zone_offset = 0

    return number_of_seconds, nanoseconds, time_zone_offset

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
      raise ValueError(f'Year value not supported: {year!s}.')

    seconds = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds)

    seconds += self._GOLANG_TO_POSIX_BASE
    nanoseconds = microseconds * definitions.NANOSECONDS_PER_MICROSECOND

    self._normalized_timestamp = None
    self._number_of_seconds = seconds
    self._nanoseconds = nanoseconds
    self._time_zone_offset = time_zone_offset

  def CopyToDateTimeString(self):
    """Copies the Golang time value to a date and time string.

    Returns:
      str: date and time value formatted as: "YYYY-MM-DD hh:mm:ss.######" or
          None if the timestamp cannot be copied to a date and time string.
    """
    if self._number_of_seconds is None or self._number_of_seconds < 0:
      return None

    number_of_days, hours, minutes, seconds = self._GetTimeValues(
        self._number_of_seconds)

    year, month, day_of_month = self._GetDateValuesWithEpoch(
        number_of_days, self._EPOCH)

    return (f'{year:04d}-{month:02d}-{day_of_month:02d} '
            f'{hours:02d}:{minutes:02d}:{seconds:02d}.{self._nanoseconds:09d}')


factory.Factory.RegisterDateTimeValues(GolangTime)
