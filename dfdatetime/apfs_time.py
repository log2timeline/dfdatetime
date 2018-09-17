# -*- coding: utf-8 -*-
"""Apple File System (APFS) time implementation."""

from __future__ import unicode_literals

import decimal

from dfdatetime import definitions
from dfdatetime import interface
from dfdatetime import posix_time


class APFSTime(interface.DateTimeValues):
  """Apple File System (APFS) timestamp.

  The APFS timestamp is a signed 64-bit integer that contains the number of
  nanoseconds since 1970-01-01 00:00:00.

  Attributes:
    is_local_time (bool): True if the date and time value is in local time.
  """

  _EPOCH = posix_time.PosixTimeEpoch()

  def __init__(self, timestamp=None):
    """Initializes an Apple File System (APFS) timestamp.

    Args:
      timestamp (Optional[int]): APFS timestamp.
    """
    super(APFSTime, self).__init__()
    self._precision = definitions.PRECISION_1_NANOSECOND
    self._timestamp = timestamp

  @property
  def timestamp(self):
    """int: APFS timestamp or None if timestamp is not set."""
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
      if (self._timestamp is not None and self._timestamp >= self._INT64_MIN and
          self._timestamp <= self._INT64_MAX):
        self._normalized_timestamp = (
            decimal.Decimal(self._timestamp) /
            definitions.NANOSECONDS_PER_SECOND)

    return self._normalized_timestamp

  def CopyFromDateTimeString(self, time_string):
    """Copies a APFS timestamp from a date and time string.

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
    microseconds = date_time_values.get('microseconds', None)

    timestamp = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds)
    timestamp *= definitions.NANOSECONDS_PER_SECOND

    if microseconds:
      nanoseconds = microseconds * definitions.MILLISECONDS_PER_SECOND
      timestamp += nanoseconds

    # Maximum value for APFS time is 2262-04-11 16:47:16.854775807
    if timestamp > self._INT64_MAX:
      raise ValueError('Date time value not supported.')

    self._normalized_timestamp = None
    self._timestamp = timestamp

  def CopyToDateTimeString(self):
    """Copies the APFS timestamp to a date and time string.

    Returns:
      str: date and time value formatted as: "YYYY-MM-DD hh:mm:ss.#########" or
          None if the timestamp is missing or invalid.
    """
    if (self._timestamp is None or self._timestamp < self._INT64_MIN or
        self._timestamp > self._INT64_MAX):
      return None

    timestamp, nanoseconds = divmod(
        self._timestamp, definitions.NANOSECONDS_PER_SECOND)
    number_of_days, hours, minutes, seconds = self._GetTimeValues(timestamp)

    year, month, day_of_month = self._GetDateValuesWithEpoch(
        number_of_days, self._EPOCH)

    return '{0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}.{6:09d}'.format(
        year, month, day_of_month, hours, minutes, seconds, nanoseconds)
