# -*- coding: utf-8 -*-
"""Java java.util.Date timestamp implementation."""

from __future__ import unicode_literals

import decimal

from dfdatetime import definitions
from dfdatetime import posix_time


class JavaTime(posix_time.PosixTimeInMilliseconds):
  """Java java.util.Date timestamp.

  The Java java.util.Date timestamp is a signed integer that contains the
  number of milliseconds since 1970-01-01 00:00:00 (also known as the POSIX
  epoch). Negative values represent date and times predating the POSIX epoch.

  Also see:
    https://docs.oracle.com/javase/8/docs/api/java/util/Date.html

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
            definitions.MILLISECONDS_PER_SECOND)

    return self._normalized_timestamp

  def CopyToDateTimeString(self):
    """Copies the POSIX timestamp to a date and time string.

    Returns:
      str: date and time value formatted as: "YYYY-MM-DD hh:mm:ss.######" or
          None if the timestamp is missing.
    """
    if (self._timestamp is None or self._timestamp < self._INT64_MIN or
        self._timestamp > self._INT64_MAX):
      return None

    return super(JavaTime, self).CopyToDateTimeString()
