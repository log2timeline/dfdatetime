# -*- coding: utf-8 -*-
"""Apple File System (APFS) time implementation."""

import decimal

from dfdatetime import definitions
from dfdatetime import factory
from dfdatetime import posix_time


class APFSTime(posix_time.PosixTimeInNanoseconds):
  """Apple File System (APFS) timestamp.

  The APFS timestamp is a signed 64-bit integer that contains the number of
  nanoseconds since 1970-01-01 00:00:00.

  Attributes:
    is_local_time (bool): True if the date and time value is in local time.
  """

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

        if self._time_zone_offset:
          self._normalized_timestamp -= self._time_zone_offset * 60

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

    Raises:
      ValueError: if the date and time value is not supported.
    """
    super(APFSTime, self)._CopyFromDateTimeString(time_string)

    if (self._timestamp is None or self._timestamp < self._INT64_MIN or
        self._timestamp > self._INT64_MAX):
      raise ValueError('Date time value not supported.')

  def CopyToDateTimeString(self):
    """Copies the APFS timestamp to a date and time string.

    Returns:
      str: date and time value formatted as: "YYYY-MM-DD hh:mm:ss.#########" or
          None if the timestamp is missing or invalid.
    """
    if (self._timestamp is None or self._timestamp < self._INT64_MIN or
        self._timestamp > self._INT64_MAX):
      return None

    return super(APFSTime, self)._CopyToDateTimeString()


factory.Factory.RegisterDateTimeValues(APFSTime)
