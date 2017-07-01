# -*- coding: utf-8 -*-
"""RFC2579 date-time implementation."""

from __future__ import unicode_literals

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
      uint8_t minuted_from_utc
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

  def __init__(self, rfc2579_date_time_tuple=None):
    """Initializes a RFC2579 date-time.

    Args:
      rfc2579_date_time_tuple:
          (Optional[tuple[int, int, int, int, int, int, int]]):
          RFC2579 date-time time, contains year, month, day of month, hours,
          minutes, seconds and deciseconds.

    Raises:
      ValueError: if the system time is invalid.
    """
    super(RFC2579DateTime, self).__init__()
    self._number_of_seconds = None
    self.day_of_month = None
    self.hours = None
    self.deciseconds = None
    self.minutes = None
    self.month = None
    self.precision = definitions.PRECISION_100_MILLISECONDS
    self.seconds = None
    self.year = None

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

      # Note that when the sign of the time zone offset is negative
      # the difference needs to be added. We do so by flipping the sign.
      if rfc2579_date_time_tuple[7] != '-':
        time_zone_offset = -time_zone_offset

      self.year, self.month, self.day_of_month, self.hours, self.minutes = (
          self._AdjustForTimeZoneOffset(
              rfc2579_date_time_tuple[0], rfc2579_date_time_tuple[1],
              rfc2579_date_time_tuple[2], rfc2579_date_time_tuple[3],
              rfc2579_date_time_tuple[4], time_zone_offset))

      self.deciseconds = rfc2579_date_time_tuple[6]
      self.seconds = rfc2579_date_time_tuple[5]

      self._number_of_seconds = self._GetNumberOfSecondsFromElements(
          self.year, self.month, self.day_of_month, self.hours, self.minutes,
          self.seconds)

  def CopyFromString(self, time_string):
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
    deciseconds, _ = divmod(microseconds, 100000)

    if year < 0 or year > 65536:
      raise ValueError('Unsupported year value: {0:d}.'.format(year))

    self._number_of_seconds = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds)

    self.year = year
    self.month = month
    self.day_of_month = day_of_month
    self.hours = hours
    self.minutes = minutes
    self.seconds = seconds
    self.deciseconds = deciseconds

    self.is_local_time = False

  def CopyToStatTimeTuple(self):
    """Copies the RFC2579 date-time to a stat timestamp tuple.

    Returns:
      tuple[int, int]: a POSIX timestamp in seconds and the remainder in
          100 nano seconds or (None, None) on error.
    """
    if self._number_of_seconds is None:
      return None, None

    return self._number_of_seconds, self.deciseconds * 1000000

  def GetPlasoTimestamp(self):
    """Retrieves a timestamp that is compatible with plaso.

    Returns:
      int: a POSIX timestamp in microseconds or None on error.
    """
    if self._number_of_seconds is None:
      return

    return ((self._number_of_seconds * 10) + self.deciseconds) * 100000
