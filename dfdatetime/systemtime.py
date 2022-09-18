# -*- coding: utf-8 -*-
"""SYSTEMTIME structure implementation."""

import decimal

from dfdatetime import definitions
from dfdatetime import factory
from dfdatetime import interface


class Systemtime(interface.DateTimeValues):
  """SYSTEMTIME structure.

  The SYSTEMTIME structure is 16 bytes of size and contains:

  struct {
      WORD year,
      WORD month,
      WORD day_of_week,
      WORD day_of_month,
      WORD hour,
      WORD minute,
      WORD second,
      WORD millisecond
  }

  Attributes:
    year (int): year, 1601 through 30827.
    month (int): month of year, 1 through 12.
    day_of_week (int): day of week, 0 through 6.
    day_of_month (int): day of month, 1 through 31.
    hours (int): hours, 0 through 23.
    minutes (int): minutes, 0 through 59.
    seconds (int): seconds, 0 through 59.
    milliseconds (int): milliseconds, 0 through 999.
  """

  # TODO: make attributes read-only.

  def __init__(
      self, precision=None, system_time_tuple=None, time_zone_offset=None):
    """Initializes a SYSTEMTIME structure.

    Args:
      precision (Optional[str]): precision of the date and time value, which
          should be one of the PRECISION_VALUES in definitions.
      system_time_tuple
          (Optional[tuple[int, int, int, int, int, int, int, int]]):
          system time, contains year, month, day of week, day of month,
          hours, minutes, seconds and milliseconds.
      time_zone_offset (Optional[int]): time zone offset in number of minutes
          from UTC or None if not set.

    Raises:
      ValueError: if the system time is invalid.
    """
    super(Systemtime, self).__init__(
        precision=precision or definitions.PRECISION_1_MILLISECOND,
        time_zone_offset=time_zone_offset)
    self._number_of_seconds = None
    self.day_of_month = None
    self.day_of_week = None
    self.hours = None
    self.milliseconds = None
    self.minutes = None
    self.month = None
    self.seconds = None
    self.year = None

    if system_time_tuple:
      if len(system_time_tuple) < 8:
        raise ValueError('Invalid system time tuple 8 elements required.')

      if system_time_tuple[0] < 1601 or system_time_tuple[0] > 30827:
        raise ValueError('Year value out of bounds.')

      if system_time_tuple[1] not in range(1, 13):
        raise ValueError('Month value out of bounds.')

      if system_time_tuple[2] not in range(0, 7):
        raise ValueError('Day of week value out of bounds.')

      days_per_month = self._GetDaysPerMonth(
          system_time_tuple[0], system_time_tuple[1])
      if system_time_tuple[3] < 1 or system_time_tuple[3] > days_per_month:
        raise ValueError('Day of month value out of bounds.')

      if system_time_tuple[4] not in range(0, 24):
        raise ValueError('Hours value out of bounds.')

      if system_time_tuple[5] not in range(0, 60):
        raise ValueError('Minutes value out of bounds.')

      # TODO: support a leap second?
      if system_time_tuple[6] not in range(0, 60):
        raise ValueError('Seconds value out of bounds.')

      if system_time_tuple[7] < 0 or system_time_tuple[7] > 999:
        raise ValueError('Milliseconds value out of bounds.')

      self.day_of_month = system_time_tuple[3]
      self.day_of_week = system_time_tuple[2]
      self.hours = system_time_tuple[4]
      self.milliseconds = system_time_tuple[7]
      self.minutes = system_time_tuple[5]
      self.month = system_time_tuple[1]
      self.seconds = system_time_tuple[6]
      self.year = system_time_tuple[0]

      self._number_of_seconds = self._GetNumberOfSecondsFromElements(
          self.year, self.month, self.day_of_month, self.hours, self.minutes,
          self.seconds)

  def _GetNormalizedTimestamp(self):
    """Retrieves the normalized timestamp.

    Returns:
      decimal.Decimal: normalized timestamp, which contains the number of
          seconds since January 1, 1970 00:00:00 and a fraction of second used
          for increased precision, or None if the normalized timestamp cannot be
          determined.
    """
    if self._normalized_timestamp is None:
      if self._number_of_seconds is not None:
        self._normalized_timestamp = (
            decimal.Decimal(self.milliseconds) /
            definitions.MILLISECONDS_PER_SECOND)
        self._normalized_timestamp += decimal.Decimal(self._number_of_seconds)

        if self._time_zone_offset:
          self._normalized_timestamp -= self._time_zone_offset * 60

    return self._normalized_timestamp

  def CopyFromDateTimeString(self, time_string):
    """Copies a SYSTEMTIME structure from a date and time string.

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

    milliseconds, _ = divmod(
        microseconds, definitions.MICROSECONDS_PER_MILLISECOND)

    if year < 1601 or year > 30827:
      raise ValueError(f'Unsupported year value: {year:d}.')

    self._normalized_timestamp = None
    self._number_of_seconds = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds)
    self._time_zone_offset = time_zone_offset

    self.year = year
    self.month = month
    self.day_of_month = day_of_month
    # TODO: calculate day of week on demand.
    self.day_of_week = None
    self.hours = hours
    self.minutes = minutes
    self.seconds = seconds
    self.milliseconds = milliseconds

  def CopyToDateTimeString(self):
    """Copies the SYSTEMTIME structure to a date and time string.

    Returns:
      str: date and time value formatted as: "YYYY-MM-DD hh:mm:ss.###" or
          None if the number of seconds is missing.
    """
    if self._number_of_seconds is None:
      return None

    return (f'{self.year:04d}-{self.month:02d}-{self.day_of_month:02d} '
            f'{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}'
            f'.{self.milliseconds:03d}')


factory.Factory.RegisterDateTimeValues(Systemtime)
