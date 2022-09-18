# -*- coding: utf-8 -*-
"""Fake timestamp implementation."""

import decimal
import time

from dfdatetime import definitions
from dfdatetime import interface
from dfdatetime import posix_time


class FakeTime(interface.DateTimeValues):
  """Fake timestamp.

  The fake timestamp is intended for testing purposes. On initialization
  it contains the current time in UTC in microsecond precision.

  Attributes:
    is_local_time (bool): True if the date and time value is in local time.
  """

  _EPOCH = posix_time.PosixTimeEpoch()

  def __init__(self, precision=None, time_zone_offset=None):
    """Initializes a fake timestamp.

    Args:
      precision (Optional[str]): precision of the date and time value, which
          should be one of the PRECISION_VALUES in definitions.
      time_zone_offset (Optional[int]): time zone offset in number of minutes
          from UTC or None if not set.
    """
    # Note that time.time() and divmod return floating point values.
    timestamp, fraction_of_second = divmod(time.time(), 1)

    super(FakeTime, self).__init__(
        precision=precision or definitions.PRECISION_1_MICROSECOND,
        time_zone_offset=time_zone_offset)
    self._microseconds = int(
        fraction_of_second * definitions.MICROSECONDS_PER_SECOND)
    self._number_of_seconds = int(timestamp)

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
            decimal.Decimal(self._microseconds) /
            definitions.MICROSECONDS_PER_SECOND)
        self._normalized_timestamp += decimal.Decimal(self._number_of_seconds)

        if self._time_zone_offset:
          self._normalized_timestamp -= self._time_zone_offset * 60

    return self._normalized_timestamp

  def CopyFromDateTimeString(self, time_string):
    """Copies a fake timestamp from a date and time string.

    Args:
      time_string (str): date and time value formatted as:
          YYYY-MM-DD hh:mm:ss.######[+-]##:##

          Where # are numeric digits ranging from 0 to 9 and the seconds
          fraction can be either 3 or 6 digits. The time of day, seconds
          fraction and time zone offset are optional. The default time zone
          is UTC.
    """
    date_time_values = self._CopyDateTimeFromString(time_string)

    year = date_time_values.get('year', 0)
    month = date_time_values.get('month', 0)
    day_of_month = date_time_values.get('day_of_month', 0)
    hours = date_time_values.get('hours', 0)
    minutes = date_time_values.get('minutes', 0)
    seconds = date_time_values.get('seconds', 0)
    time_zone_offset = date_time_values.get('time_zone_offset', 0)

    self._normalized_timestamp = None
    self._number_of_seconds = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds)
    self._microseconds = date_time_values.get('microseconds', None)
    self._time_zone_offset = time_zone_offset

  def CopyToDateTimeString(self):
    """Copies the fake timestamp to a date and time string.

    Returns:
      str: date and time value formatted as: "YYYY-MM-DD hh:mm:ss" or
          "YYYY-MM-DD hh:mm:ss.######" or None if the number of seconds
          is missing.
    """
    if self._number_of_seconds is None:
      return None

    number_of_days, hours, minutes, seconds = self._GetTimeValues(
        self._number_of_seconds)

    year, month, day_of_month = self._GetDateValuesWithEpoch(
        number_of_days, self._EPOCH)

    date_time_string = (
        f'{year:04d}-{month:02d}-{day_of_month:02d} '
        f'{hours:02d}:{minutes:02d}:{seconds:02d}')

    if self._microseconds is not None:
      date_time_string = '.'.join([
          date_time_string, f'{self._microseconds:06d}'])

    return date_time_string
