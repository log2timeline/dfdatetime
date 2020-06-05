# -*- coding: utf-8 -*-
"""RFC2579 date-time implementation."""

from __future__ import unicode_literals

import decimal

from typing import Optional, Tuple, Union  # pylint: disable=unused-import

from dfdatetime import definitions
from dfdatetime import interface


class RFC2579DateTime(interface.DateTimeValues):
  """RFC2579 date-time.

  The RFC2579 date-time structure is 11 bytes of size and contains:

  struct {
      uin16_t year,
      uint8_t month,
      uint8_t day_of_month,
      uint8_t hours,
      uint8_t minutes,
      uint8_t seconds,
      uint8_t deciseconds,
      char direction_from_utc,
      uint8_t hours_from_utc,
      uint8_t minutes_from_utc
  }

  Also see:
    https://tools.ietf.org/html/rfc2579

  Attributes:
    year (int): year, 0 through 65536.
    month (int): month of year, 1 through 12.
    day_of_month (int): day of month, 1 through 31.
    hours (int): hours, 0 through 23.
    minutes (int): minutes, 0 through 59.
    seconds (int): seconds, 0 through 59, where 60 is used to represent
        a leap-second.
    deciseconds (int): deciseconds, 0 through 9.
  """

  # TODO: make attributes read-only.

  # pylint: disable=missing-type-doc

  def __init__(self, rfc2579_date_time_tuple: (
      'Optional[Tuple[int, int, int, int, int, int, int, str, int, '
      'int]]') = None):  # pylint: disable=bad-whitespace
    """Initializes a RFC2579 date-time.

    Args:
      rfc2579_date_time_tuple:
          (Optional[tuple[int, int, int, int, int, int, int, str, int, int]]):
          RFC2579 date-time time, contains year, month, day of month, hours,
          minutes, seconds, deciseconds and time zone offset.

    Raises:
      ValueError: if the system time is invalid.
    """
    super(RFC2579DateTime, self).__init__()
    self._number_of_seconds: 'Union[int, None]' = None
    self._precision: 'str' = definitions.PRECISION_100_MILLISECONDS
    self.day_of_month: 'Union[int, None]' = None
    self.hours: 'Union[int, None]' = None
    self.deciseconds: 'Union[int, None]' = None
    self.minutes: 'Union[int, None]' = None
    self.month: 'Union[int, None]' = None
    self.seconds: 'Union[int, None]' = None
    self.year: 'Union[int, None]' = None

    if rfc2579_date_time_tuple:
      if len(rfc2579_date_time_tuple) < 10:
        raise ValueError(
            'Invalid RFC2579 date-time tuple 10 elements required.')

      if rfc2579_date_time_tuple[0] < 0 or rfc2579_date_time_tuple[0] > 65536:
        raise ValueError('Year value out of bounds.')

      if rfc2579_date_time_tuple[1] not in range(1, 13):
        raise ValueError('Month value out of bounds.')

      days_per_month = self._GetDaysPerMonth(
          rfc2579_date_time_tuple[0], rfc2579_date_time_tuple[1])
      if (rfc2579_date_time_tuple[2] < 1 or
          rfc2579_date_time_tuple[2] > days_per_month):
        raise ValueError('Day of month value out of bounds.')

      if rfc2579_date_time_tuple[3] not in range(0, 24):
        raise ValueError('Hours value out of bounds.')

      if rfc2579_date_time_tuple[4] not in range(0, 60):
        raise ValueError('Minutes value out of bounds.')

      # TODO: support a leap second?
      if rfc2579_date_time_tuple[5] not in range(0, 60):
        raise ValueError('Seconds value out of bounds.')

      if rfc2579_date_time_tuple[6] < 0 or rfc2579_date_time_tuple[6] > 9:
        raise ValueError('Deciseconds value out of bounds.')

      if rfc2579_date_time_tuple[7] not in ('+', '-'):
        raise ValueError('Direction from UTC value out of bounds.')

      if rfc2579_date_time_tuple[8] not in range(0, 14):
        raise ValueError('Hours from UTC value out of bounds.')

      if rfc2579_date_time_tuple[9] not in range(0, 60):
        raise ValueError('Minutes from UTC value out of bounds.')

      time_zone_offset = (
          (rfc2579_date_time_tuple[8] * 60) + rfc2579_date_time_tuple[9])

      if rfc2579_date_time_tuple[7] == '-':
        time_zone_offset = -time_zone_offset

      self._time_zone_offset = time_zone_offset

      self.year = rfc2579_date_time_tuple[0]
      self.month = rfc2579_date_time_tuple[1]
      self.day_of_month = rfc2579_date_time_tuple[2]
      self.hours = rfc2579_date_time_tuple[3]
      self.minutes = rfc2579_date_time_tuple[4]
      self.seconds = rfc2579_date_time_tuple[5]
      self.deciseconds = rfc2579_date_time_tuple[6]

      self._number_of_seconds = self._GetNumberOfSecondsFromElements(
          self.year, self.month, self.day_of_month, self.hours, self.minutes,
          self.seconds, time_zone_offset=self._time_zone_offset)

  def _GetNormalizedTimestamp(self) -> 'Union[decimal.Decimal, None]':
    """Retrieves the normalized timestamp.

    Returns:
      decimal.Decimal: normalized timestamp, which contains the number of
          seconds since January 1, 1970 00:00:00 and a fraction of second
          used for increased precision, or None if the normalized timestamp
          cannot be determined.
    """
    if self._normalized_timestamp is None:
      if self._number_of_seconds is not None:
        self._normalized_timestamp = (
            decimal.Decimal(self.deciseconds or 0) /
            definitions.DECISECONDS_PER_SECOND)
        self._normalized_timestamp += decimal.Decimal(self._number_of_seconds)

    return self._normalized_timestamp

  def CopyFromDateTimeString(self, time_string: 'str') -> 'None':
    """Copies a RFC2579 date-time from a date and time string.

    Args:
      time_string (str): date and time value formatted as:
          YYYY-MM-DD hh:mm:ss.######[+-]##:##

          Where # are numeric digits ranging from 0 to 9 and the seconds
          fraction can be either 3 or 6 digits. The time of day, seconds
          fraction and time zone offset are optional. The default time zone
          is UTC.

    Raises:
      ValueError: if the date string is invalid or not supported.
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

    deciseconds, _ = divmod(
        microseconds, definitions.MICROSECONDS_PER_DECISECOND)

    if year < 0 or year > 65536:
      raise ValueError('Unsupported year value: {0:d}.'.format(year))

    self._normalized_timestamp = None
    self._number_of_seconds = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds,
        time_zone_offset=time_zone_offset)
    self._time_zone_offset = time_zone_offset

    self.year = year
    self.month = month
    self.day_of_month = day_of_month
    self.hours = hours
    self.minutes = minutes
    self.seconds = seconds
    self.deciseconds = deciseconds

  def CopyToDateTimeString(self) -> 'Union[str, None]':
    """Copies the RFC2579 date-time to a date and time string.

    Returns:
      str: date and time value formatted as: "YYYY-MM-DD hh:mm:ss.#" or
          None if the number of seconds is missing.
    """
    if self._number_of_seconds is None:
      return None

    return '{0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}.{6:01d}'.format(
        self.year or 0, self.month or 0, self.day_of_month or 0,
        self.hours or 0, self.minutes or 0, self.seconds or 0,
        self.deciseconds or 0)
