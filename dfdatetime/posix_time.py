# -*- coding: utf-8 -*-
"""POSIX timestamp implementation."""

import decimal

from dfdatetime import definitions
from dfdatetime import factory
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
  """

  _EPOCH = PosixTimeEpoch()

  def __init__(self, precision=None, time_zone_offset=None, timestamp=None):
    """Initializes a POSIX timestamp.

    Args:
      precision (Optional[str]): precision of the date and time value, which
          should be one of the PRECISION_VALUES in definitions.
      time_zone_offset (Optional[int]): time zone offset in number of minutes
          from UTC or None if not set.
      timestamp (Optional[int]): POSIX timestamp.
    """
    super(PosixTime, self).__init__(
        precision=precision or definitions.PRECISION_1_SECOND,
        time_zone_offset=time_zone_offset)
    self._timestamp = timestamp

  @property
  def timestamp(self):
    """int: POSIX timestamp or None if not set."""
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
        self._normalized_timestamp = decimal.Decimal(self._timestamp)

        if self._time_zone_offset:
          self._normalized_timestamp -= self._time_zone_offset * 60

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
    time_zone_offset = date_time_values.get('time_zone_offset', 0)

    self._timestamp = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds)
    self._time_zone_offset = time_zone_offset

  def CopyToDateTimeString(self):
    """Copies the POSIX timestamp to a date and time string.

    Returns:
      str: date and time value formatted as: "YYYY-MM-DD hh:mm:ss" or None
          if the timestamp is missing.
    """
    if self._timestamp is None:
      return None

    number_of_days, hours, minutes, seconds = self._GetTimeValues(
        self._timestamp)

    year, month, day_of_month = self._GetDateValuesWithEpoch(
        number_of_days, self._EPOCH)

    return (f'{year:04d}-{month:02d}-{day_of_month:02d} '
            f'{hours:02d}:{minutes:02d}:{seconds:02d}')


class PosixTimeInMilliseconds(interface.DateTimeValues):
  """POSIX timestamp in milliseconds.

  Variant of the POSIX timestamp in milliseconds.

  Attributes:
    is_local_time (bool): True if the date and time value is in local time.
  """

  _EPOCH = PosixTimeEpoch()

  def __init__(self, precision=None, time_zone_offset=None, timestamp=None):
    """Initializes a POSIX timestamp in milliseconds.

    Args:
      precision (Optional[str]): precision of the date and time value, which
          should be one of the PRECISION_VALUES in definitions.
      time_zone_offset (Optional[int]): time zone offset in number of minutes
          from UTC or None if not set.
      timestamp (Optional[int]): POSIX timestamp in milliseconds.
    """
    super(PosixTimeInMilliseconds, self).__init__(
        precision=precision or definitions.PRECISION_1_MILLISECOND,
        time_zone_offset=time_zone_offset)
    self._timestamp = timestamp

  @property
  def timestamp(self):
    """int: POSIX timestamp in milliseconds or None if not set."""
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
        self._normalized_timestamp = (
            decimal.Decimal(self._timestamp) /
            definitions.MILLISECONDS_PER_SECOND)

        if self._time_zone_offset:
          self._normalized_timestamp -= self._time_zone_offset * 60

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
    time_zone_offset = date_time_values.get('time_zone_offset', 0)

    timestamp = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds)
    timestamp *= definitions.MILLISECONDS_PER_SECOND

    if microseconds:
      milliseconds, _ = divmod(
          microseconds, definitions.MILLISECONDS_PER_SECOND)
      timestamp += milliseconds

    self._timestamp = timestamp
    self._time_zone_offset = time_zone_offset

  def CopyToDateTimeString(self):
    """Copies the POSIX timestamp to a date and time string.

    Returns:
      str: date and time value formatted as: "YYYY-MM-DD hh:mm:ss.######" or
          None if the timestamp is missing.
    """
    if self._timestamp is None:
      return None

    timestamp, milliseconds = divmod(
        self._timestamp, definitions.MILLISECONDS_PER_SECOND)
    number_of_days, hours, minutes, seconds = self._GetTimeValues(timestamp)

    year, month, day_of_month = self._GetDateValuesWithEpoch(
        number_of_days, self._EPOCH)

    return (f'{year:04d}-{month:02d}-{day_of_month:02d} '
            f'{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}')


class PosixTimeInMicroseconds(interface.DateTimeValues):
  """POSIX timestamp in microseconds.

  Variant of the POSIX timestamp in microseconds.

  Attributes:
    is_local_time (bool): True if the date and time value is in local time.
  """

  _EPOCH = PosixTimeEpoch()

  def __init__(self, precision=None, time_zone_offset=None, timestamp=None):
    """Initializes a POSIX timestamp in microseconds.

    Args:
      precision (Optional[str]): precision of the date and time value, which
          should be one of the PRECISION_VALUES in definitions.
      time_zone_offset (Optional[int]): time zone offset in number of minutes
          from UTC or None if not set.
      timestamp (Optional[int]): POSIX timestamp in microseconds.
    """
    super(PosixTimeInMicroseconds, self).__init__(
        precision=precision or definitions.PRECISION_1_MICROSECOND,
        time_zone_offset=time_zone_offset)
    self._timestamp = timestamp

  @property
  def timestamp(self):
    """int: POSIX timestamp in microseconds or None if not set."""
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
        self._normalized_timestamp = (
            decimal.Decimal(self._timestamp) /
            definitions.MICROSECONDS_PER_SECOND)

        if self._time_zone_offset:
          self._normalized_timestamp -= self._time_zone_offset * 60

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
    time_zone_offset = date_time_values.get('time_zone_offset', 0)

    timestamp = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds)
    timestamp *= definitions.MICROSECONDS_PER_SECOND
    timestamp += microseconds

    self._timestamp = timestamp
    self._time_zone_offset = time_zone_offset

  def CopyToDateTimeString(self):
    """Copies the POSIX timestamp to a date and time string.

    Returns:
      str: date and time value formatted as: "YYYY-MM-DD hh:mm:ss.######" or
          None if the timestamp is missing.
    """
    if self._timestamp is None:
      return None

    timestamp, microseconds = divmod(
        self._timestamp, definitions.MICROSECONDS_PER_SECOND)
    number_of_days, hours, minutes, seconds = self._GetTimeValues(timestamp)

    year, month, day_of_month = self._GetDateValuesWithEpoch(
        number_of_days, self._EPOCH)

    return (f'{year:04d}-{month:02d}-{day_of_month:02d} '
            f'{hours:02d}:{minutes:02d}:{seconds:02d}.{microseconds:06d}')


class PosixTimeInNanoseconds(interface.DateTimeValues):
  """POSIX timestamp in nanoseconds.

  Variant of the POSIX timestamp in nanoseconds.

  Attributes:
    is_local_time (bool): True if the date and time value is in local time.
  """

  _EPOCH = PosixTimeEpoch()

  def __init__(self, precision=None, time_zone_offset=None, timestamp=None):
    """Initializes a POSIX timestamp in nanoseconds.

    Args:
      precision (Optional[str]): precision of the date and time value, which
          should be one of the PRECISION_VALUES in definitions.
      time_zone_offset (Optional[int]): time zone offset in number of minutes
          from UTC or None if not set.
      timestamp (Optional[int]): POSIX timestamp in nanoseconds.
    """
    super(PosixTimeInNanoseconds, self).__init__(
        precision=precision or definitions.PRECISION_1_NANOSECOND,
        time_zone_offset=time_zone_offset)
    self._timestamp = timestamp

  @property
  def timestamp(self):
    """int: POSIX timestamp or None if not set."""
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
        self._normalized_timestamp = (
            decimal.Decimal(self._timestamp) /
            definitions.NANOSECONDS_PER_SECOND)

        if self._time_zone_offset:
          self._normalized_timestamp -= self._time_zone_offset * 60

    return self._normalized_timestamp

  def _CopyFromDateTimeString(self, time_string):
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
    microseconds = date_time_values.get('microseconds', None)
    time_zone_offset = date_time_values.get('time_zone_offset', 0)

    timestamp = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds)
    timestamp *= definitions.NANOSECONDS_PER_SECOND

    if microseconds:
      nanoseconds = microseconds * definitions.MILLISECONDS_PER_SECOND
      timestamp += nanoseconds

    self._normalized_timestamp = None
    self._timestamp = timestamp
    self._time_zone_offset = time_zone_offset

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
    self._CopyFromDateTimeString(time_string)

  def _CopyToDateTimeString(self):
    """Copies the POSIX timestamp to a date and time string.

    Returns:
      str: date and time value formatted as: "YYYY-MM-DD hh:mm:ss.#########" or
          None if the timestamp is missing or invalid.
    """
    if self._timestamp is None:
      return None

    timestamp, nanoseconds = divmod(
        self._timestamp, definitions.NANOSECONDS_PER_SECOND)
    number_of_days, hours, minutes, seconds = self._GetTimeValues(timestamp)

    year, month, day_of_month = self._GetDateValuesWithEpoch(
        number_of_days, self._EPOCH)

    return (f'{year:04d}-{month:02d}-{day_of_month:02d} '
            f'{hours:02d}:{minutes:02d}:{seconds:02d}.{nanoseconds:09d}')

  def CopyToDateTimeString(self):
    """Copies the POSIX timestamp to a date and time string.

    Returns:
      str: date and time value formatted as: "YYYY-MM-DD hh:mm:ss.#########" or
          None if the timestamp is missing or invalid.
    """
    return self._CopyToDateTimeString()


factory.Factory.RegisterDateTimeValues(PosixTime)
factory.Factory.RegisterDateTimeValues(PosixTimeInMilliseconds)
factory.Factory.RegisterDateTimeValues(PosixTimeInMicroseconds)
factory.Factory.RegisterDateTimeValues(PosixTimeInNanoseconds)
