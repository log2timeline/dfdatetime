# -*- coding: utf-8 -*-
"""WebKit time implementation."""

import decimal

from dfdatetime import definitions
from dfdatetime import factory
from dfdatetime import interface


class WebKitTimeEpoch(interface.DateTimeEpoch):
  """WebKit time epoch."""

  def __init__(self):
    """Initializes a WebKit time epoch."""
    super(WebKitTimeEpoch, self).__init__(1601, 1, 1)


class WebKitTime(interface.DateTimeValues):
  """WebKit timestamp.

  The WebKit timestamp is a signed 64-bit integer that contains the number of
  microseconds since 1601-01-01 00:00:00.

  Attributes:
    is_local_time (bool): True if the date and time value is in local time.
  """

  _EPOCH = WebKitTimeEpoch()

  # The difference between January 1, 1601 and January 1, 1970 in seconds.
  _WEBKIT_TO_POSIX_BASE = 11644473600

  def __init__(self, precision=None, time_zone_offset=None, timestamp=None):
    """Initializes a WebKit timestamp.

    Args:
      precision (Optional[str]): precision of the date and time value, which
          should be one of the PRECISION_VALUES in definitions.
      time_zone_offset (Optional[int]): time zone offset in number of minutes
          from UTC or None if not set.
      timestamp (Optional[int]): WebKit timestamp.
    """
    super(WebKitTime, self).__init__(
        precision=precision or definitions.PRECISION_1_MICROSECOND,
        time_zone_offset=time_zone_offset)
    self._timestamp = timestamp

  @property
  def timestamp(self):
    """decimal.Decimal: WebKit timestamp or None if not set."""
    return self._timestamp

  def _GetNormalizedTimestamp(self):
    """Retrieves the normalized timestamp.

    Returns:
      float: normalized timestamp, which contains the number of seconds since
          January 1, 1970 00:00:00 and a fraction of second used for increased
          precision, or None if the normalized timestamp cannot be determined.
    """
    if self._normalized_timestamp is None:
      if (self._timestamp is not None and self._timestamp >= self._INT64_MIN and
          self._timestamp <= self._INT64_MAX):
        self._normalized_timestamp = (
            decimal.Decimal(self._timestamp) /
            definitions.MICROSECONDS_PER_SECOND)
        self._normalized_timestamp -= self._WEBKIT_TO_POSIX_BASE

        if self._time_zone_offset:
          self._normalized_timestamp -= self._time_zone_offset * 60

    return self._normalized_timestamp

  def CopyFromDateTimeString(self, time_string):
    """Copies a WebKit timestamp from a date and time string.

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
    time_zone_offset = date_time_values.get('time_zone_offset', 0)

    timestamp = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds)
    timestamp += self._WEBKIT_TO_POSIX_BASE
    timestamp *= definitions.MICROSECONDS_PER_SECOND
    timestamp += date_time_values.get('microseconds', 0)

    self._normalized_timestamp = None
    self._timestamp = timestamp
    self._time_zone_offset = time_zone_offset

  def CopyToDateTimeString(self):
    """Copies the WebKit timestamp to a date and time string.

    Returns:
      str: date and time value formatted as: "YYYY-MM-DD hh:mm:ss.######" or
          None if the timestamp is missing or invalid.
    """
    if (self._timestamp is None or self._timestamp < self._INT64_MIN or
        self._timestamp > self._INT64_MAX):
      return None

    timestamp, microseconds = divmod(
        self._timestamp, definitions.MICROSECONDS_PER_SECOND)
    number_of_days, hours, minutes, seconds = self._GetTimeValues(timestamp)

    year, month, day_of_month = self._GetDateValuesWithEpoch(
        number_of_days, self._EPOCH)

    return (f'{year:04d}-{month:02d}-{day_of_month:02d} '
            f'{hours:02d}:{minutes:02d}:{seconds:02d}.{microseconds:06d}')


factory.Factory.RegisterDateTimeValues(WebKitTime)
