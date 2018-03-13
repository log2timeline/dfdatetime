# -*- coding: utf-8 -*-
"""POSIX timestamp implementation."""

from __future__ import unicode_literals

import decimal

from dfdatetime import definitions
from dfdatetime import interface


class PosixTimeEpoch(interface.DateTimeEpoch):
  """POSIX time epoch."""

  def __init__(self):
    """Initializes a POSIX time epoch."""
    super(PosixTimeEpoch, self).__init__(1970, 1, 1)


class PosixTime(interface.DateTimeValues):
  """POSIX timestamp.

  The POSIX timestamp is a signed integer that contains the number of
  seconds since 1970-01-01 00:00:00 (also known as the POSIX epoch).
  Negative values represent date and times predating the POSIX epoch.

  The POSIX timestamp was initially 32-bit though 64-bit variants
  are known to be used.

  Attributes:
    is_local_time (bool): True if the date and time value is in local time.
    precision (str): precision of the date and time value, which should
        be one of the PRECISION_VALUES in definitions.
  """

  _EPOCH = PosixTimeEpoch()

  def __init__(self, timestamp=None):
    """Initializes a POSIX timestamp.

    Args:
      timestamp (Optional[int]): POSIX timestamp.
    """
    super(PosixTime, self).__init__()
    self._timestamp = timestamp
    self.precision = definitions.PRECISION_1_SECOND

  @property
  def timestamp(self):
    """int: POSIX timestamp or None if timestamp is not set."""
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
      if self._timestamp is not None:
        normalized_timestamp = decimal.Decimal(self._timestamp)
        self._SetNormalizedTimestamp(normalized_timestamp)

    return self._normalized_timestamp

  def CopyFromDateTimeString(self, time_string):
    """Copies a POSIX timestamp from a date and time string.

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

    self._timestamp = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds)

    self.is_local_time = False

  def CopyToDateTimeString(self):
    """Copies the POSIX timestamp to a date and time string.

    Returns:
      str: date and time value formatted as:
          YYYY-MM-DD hh:mm:ss
    """
    if self._timestamp is None:
      return

    number_of_days, hours, minutes, seconds = self._GetTimeValues(
        self._timestamp)

    year, month, day_of_month = self._GetDateValuesWithEpoch(
        number_of_days, self._EPOCH)

    return '{0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}'.format(
        year, month, day_of_month, hours, minutes, seconds)

  def GetDate(self):
    """Retrieves the date represented by the date and time values.

    Returns:
       tuple[int, int, int]: year, month, day of month or (None, None, None)
           if the date and time values do not represent a date.
    """
    if self.timestamp is None:
      return None, None, None

    try:
      number_of_days, _, _, _ = self._GetTimeValues(self.timestamp)
      return self._GetDateValuesWithEpoch(number_of_days, self._EPOCH)

    except ValueError:
      return None, None, None


class PosixTimeInMicroseconds(interface.DateTimeValues):
  """POSIX timestamp in microseconds.

  Variant of the POSIX timestamp in microseconds.

  Attributes:
    is_local_time (bool): True if the date and time value is in local time.
    precision (str): precision of the date and time value, which should
        be one of the PRECISION_VALUES in definitions.
  """

  _EPOCH = PosixTimeEpoch()

  def __init__(self, timestamp=None):
    """Initializes a POSIX timestamp in microseconds.

    Args:
      timestamp (Optional[int]): POSIX timestamp in microseconds.
    """
    super(PosixTimeInMicroseconds, self).__init__()
    self._timestamp = timestamp
    self.precision = definitions.PRECISION_1_MICROSECOND

  @property
  def timestamp(self):
    """int: POSIX timestamp in microseconds or None if timestamp is not set."""
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
      if self._timestamp is not None:
        normalized_timestamp = (
            decimal.Decimal(self._timestamp) /
            definitions.MICROSECONDS_PER_SECOND)
        self._SetNormalizedTimestamp(normalized_timestamp)

    return self._normalized_timestamp

  def CopyFromDateTimeString(self, time_string):
    """Copies a POSIX timestamp from a date and time string.

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
    microseconds = date_time_values.get('microseconds', 0)

    timestamp = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds)
    timestamp *= definitions.MICROSECONDS_PER_SECOND
    timestamp += microseconds

    self._timestamp = timestamp
    self.is_local_time = False

  def CopyToDateTimeString(self):
    """Copies the POSIX timestamp to a date and time string.

    Returns:
      str: date and time value formatted as:
          YYYY-MM-DD hh:mm:ss.######
    """
    if self._timestamp is None:
      return

    timestamp, microseconds = divmod(
        self._timestamp, definitions.MICROSECONDS_PER_SECOND)
    number_of_days, hours, minutes, seconds = self._GetTimeValues(timestamp)

    year, month, day_of_month = self._GetDateValuesWithEpoch(
        number_of_days, self._EPOCH)

    return '{0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}.{6:06d}'.format(
        year, month, day_of_month, hours, minutes, seconds, microseconds)

  def GetDate(self):
    """Retrieves the date represented by the date and time values.

    Returns:
       tuple[int, int, int]: year, month, day of month or (None, None, None)
           if the date and time values do not represent a date.
    """
    if self.timestamp is None:
      return None, None, None

    try:
      timestamp, _ = divmod(self.timestamp, definitions.MICROSECONDS_PER_SECOND)
      number_of_days, _, _, _ = self._GetTimeValues(timestamp)
      return self._GetDateValuesWithEpoch(number_of_days, self._EPOCH)

    except ValueError:
      return None, None, None
