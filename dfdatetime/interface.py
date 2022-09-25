# -*- coding: utf-8 -*-
"""Date and time interfaces."""

import abc
import calendar
import decimal

from dfdatetime import definitions


class DateTimeEpoch(object):
  """Date and time epoch interface.

  This is the super class of different epoch representations.

  Attributes:
    year (int): year that is the start of the epoch e.g. 1970.
    month (int): month that is the start of the epoch, where 1 represents
        January.
    day_of_month (int): day of the month that is the start of the epoch,
        where 1 represents the first day.
  """

  def __init__(self, year, month, day_of_month):
    """Initializes a date time epoch.

    Args:
      year (int): year that is the start of the epoch e.g. 1970.
      month (int): month that is the start of the epoch, where 1 represents
          January.
      day_of_month (int): day of the month that is the start of the epoch,
          where 1 represents the first day.
    """
    super(DateTimeEpoch, self).__init__()
    self.day_of_month = day_of_month
    self.month = month
    self.year = year


class NormalizedTimeEpoch(DateTimeEpoch):
  """dfDateTime normalized time epoch."""

  def __init__(self):
    """Initializes a dfDateTime normalized time epoch."""
    super(NormalizedTimeEpoch, self).__init__(1970, 1, 1)


class DateTimeValues(object):
  """Date and time values interface.

  This is the super class of different date and time representations.

  Attributes:
    is_local_time (bool): True if the date and time value is in local time.
  """

  # pylint: disable=redundant-returns-doc

  _DAYS_PER_MONTH = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

  _EPOCH_NORMALIZED_TIME = NormalizedTimeEpoch()

  _100_MILLISECONDS_PER_SECOND = 10
  _10_MILLISECONDS_PER_SECOND = 100
  _1_MILLISECOND_PER_SECOND = 1000
  _100_MICROSECONDS_PER_SECOND = 10000
  _10_MICROSECONDS_PER_SECOND = 100000
  _1_MICROSECOND_PER_SECOND = 1000000
  _100_NANOSECONDS_PER_SECOND = 10000000
  _10_NANOSECONDS_PER_SECOND = 100000000
  _1_NANOSECOND_PER_SECOND = definitions.NANOSECONDS_PER_SECOND

  _100_NANOSECONDS_PER_MICROSECOND = 10

  _INT64_MIN = -(1 << 63)
  _INT64_MAX = (1 << 63) - 1

  _UINT32_MAX = (1 << 32) - 1
  _UINT60_MAX = (1 << 60) - 1
  _UINT64_MAX = (1 << 64) - 1

  _REMAINDER_MULTIPLIER = {
      definitions.PRECISION_1_MILLISECOND: _1_MILLISECOND_PER_SECOND,
      definitions.PRECISION_10_MILLISECONDS: _10_MILLISECONDS_PER_SECOND,
      definitions.PRECISION_100_MILLISECONDS: _100_MILLISECONDS_PER_SECOND,
      definitions.PRECISION_1_MICROSECOND: _1_MICROSECOND_PER_SECOND,
      definitions.PRECISION_10_MICROSECONDS: _10_MICROSECONDS_PER_SECOND,
      definitions.PRECISION_100_MICROSECONDS: _100_MICROSECONDS_PER_SECOND,
      definitions.PRECISION_1_NANOSECOND: _1_NANOSECOND_PER_SECOND,
      definitions.PRECISION_10_NANOSECONDS: _10_NANOSECONDS_PER_SECOND,
      definitions.PRECISION_100_NANOSECONDS: _100_NANOSECONDS_PER_SECOND}

  def __init__(self, precision=None, time_zone_offset=None):
    """Initializes date time values.

    Args:
      precision (Optional[str]): precision of the date and time value, which
          should be one of the PRECISION_VALUES in definitions.
      time_zone_offset (Optional[int]): time zone offset in number of minutes
          from UTC or None if not set.
    """
    super(DateTimeValues, self).__init__()
    self._cached_date_time_values = None
    self._normalized_timestamp = None
    self._precision = precision
    self._time_zone_offset = time_zone_offset

    self.is_local_time = False

  @property
  def precision(self):
    """precision (str): precision of the date and time value, which should
        be one of the PRECISION_VALUES in definitions.
    """
    return self._precision

  @property
  def time_zone_offset(self):
    """time_zone_offset (int): time zone offset in number of minutes from UTC
        or None if not set.
    """
    return self._time_zone_offset

  def __eq__(self, other):
    """Determines if the date time values are equal to other.

    Args:
      other (DateTimeValues): date time values to compare against.

    Returns:
      bool: True if the date time values are equal to other.
    """
    if not isinstance(other, DateTimeValues):
      return False

    normalized_timestamp = self._GetNormalizedTimestamp()
    other_normalized_timestamp = other._GetNormalizedTimestamp()  # pylint: disable=protected-access

    if normalized_timestamp is None and other_normalized_timestamp is not None:
      return False

    if normalized_timestamp is not None and other_normalized_timestamp is None:
      return False

    return normalized_timestamp == other_normalized_timestamp

  def __ge__(self, other):
    """Determines if the date time values are greater than or equal to other.

    Args:
      other (DateTimeValues): date time values to compare against.

    Returns:
      bool: True if the date time values are greater than or equal to other.

    Raises:
      ValueError: if other is not an instance of DateTimeValues.
    """
    if not isinstance(other, DateTimeValues):
      raise ValueError('Other not an instance of DateTimeValues')

    normalized_timestamp = self._GetNormalizedTimestamp()
    other_normalized_timestamp = other._GetNormalizedTimestamp()  # pylint: disable=protected-access

    if normalized_timestamp is None:
      return other_normalized_timestamp is None

    if other_normalized_timestamp is None:
      return True

    return normalized_timestamp >= other_normalized_timestamp

  def __gt__(self, other):
    """Determines if the date time values are greater than other.

    Args:
      other (DateTimeValues): date time values to compare against.

    Returns:
      bool: True if the date time values are greater than other.

    Raises:
      ValueError: if other is not an instance of DateTimeValues.
    """
    if not isinstance(other, DateTimeValues):
      raise ValueError('Other not an instance of DateTimeValues')

    normalized_timestamp = self._GetNormalizedTimestamp()
    other_normalized_timestamp = other._GetNormalizedTimestamp()  # pylint: disable=protected-access

    if normalized_timestamp is None:
      return False

    if other_normalized_timestamp is None:
      return True

    return normalized_timestamp > other_normalized_timestamp

  def __le__(self, other):
    """Determines if the date time values are greater than or equal to other.

    Args:
      other (DateTimeValues): date time values to compare against.

    Returns:
      bool: True if the date time values are greater than or equal to other.

    Raises:
      ValueError: if other is not an instance of DateTimeValues.
    """
    if not isinstance(other, DateTimeValues):
      raise ValueError('Other not an instance of DateTimeValues')

    normalized_timestamp = self._GetNormalizedTimestamp()
    other_normalized_timestamp = other._GetNormalizedTimestamp()  # pylint: disable=protected-access

    if normalized_timestamp is None:
      return True

    if other_normalized_timestamp is None:
      return False

    return normalized_timestamp <= other_normalized_timestamp

  def __lt__(self, other):
    """Determines if the date time values are less than other.

    Args:
      other (DateTimeValues): date time values to compare against.

    Returns:
      bool: True if the date time values are less than other.

    Raises:
      ValueError: if other is not an instance of DateTimeValues.
    """
    if not isinstance(other, DateTimeValues):
      raise ValueError('Other not an instance of DateTimeValues')

    normalized_timestamp = self._GetNormalizedTimestamp()
    other_normalized_timestamp = other._GetNormalizedTimestamp()  # pylint: disable=protected-access

    if normalized_timestamp is None:
      return other_normalized_timestamp is not None

    if other_normalized_timestamp is None:
      return False

    return normalized_timestamp < other_normalized_timestamp

  def __ne__(self, other):
    """Determines if the date time values are not equal to other.

    Args:
      other (DateTimeValues): date time values to compare against.

    Returns:
      bool: True if the date time values are not equal to other.
    """
    if not isinstance(other, DateTimeValues):
      return True

    normalized_timestamp = self._GetNormalizedTimestamp()
    other_normalized_timestamp = other._GetNormalizedTimestamp()  # pylint: disable=protected-access

    if normalized_timestamp is None and other_normalized_timestamp is not None:
      return True

    if normalized_timestamp is not None and other_normalized_timestamp is None:
      return True

    return normalized_timestamp != other_normalized_timestamp

  def _CopyDateFromString(self, date_string):
    """Copies a date from a string.

    Args:
      date_string (str): date value formatted as: YYYY-MM-DD

    Returns:
      tuple[int, int, int]: year, month, day of month.

    Raises:
      ValueError: if the date string is invalid or not supported.
    """
    date_string_length = len(date_string)

    # The date string should at least contain 'YYYY-MM-DD'.
    if date_string_length < 10:
      raise ValueError('Date string too short.')

    if date_string[4] != '-' or date_string[7] != '-':
      raise ValueError('Invalid date string.')

    try:
      year = int(date_string[0:4], 10)
    except ValueError:
      raise ValueError('Unable to parse year.')

    try:
      month = int(date_string[5:7], 10)
    except ValueError:
      raise ValueError('Unable to parse month.')

    try:
      day_of_month = int(date_string[8:10], 10)
    except ValueError:
      raise ValueError('Unable to parse day of month.')

    days_per_month = self._GetDaysPerMonth(year, month)
    if day_of_month < 1 or day_of_month > days_per_month:
      raise ValueError('Day of month value out of bounds.')

    return year, month, day_of_month

  def _CopyDateTimeFromString(self, time_string):
    """Copies a date and time from a string.

    Args:
      time_string (str): date and time value formatted as:
          YYYY-MM-DD hh:mm:ss.######[+-]##:##

          Where # are numeric digits ranging from 0 to 9 and the seconds
          fraction can be either 3 or 6 digits. The time of day, seconds
          fraction and time zone offset are optional. The default time zone
          is UTC.

    Returns:
      dict[str, int]: date and time values, such as year, month, day of month,
          hours, minutes, seconds, microseconds, time zone offset in minutes.

    Raises:
      ValueError: if the time string is invalid or not supported.
    """
    if not time_string:
      raise ValueError('Invalid time string.')

    time_string_length = len(time_string)

    year, month, day_of_month = self._CopyDateFromString(time_string)

    if time_string_length <= 10:
      return {
          'year': year,
          'month': month,
          'day_of_month': day_of_month}

    # If a time of day is specified the time string it should at least
    # contain 'YYYY-MM-DD hh:mm:ss'.
    if time_string[10] != ' ':
      raise ValueError(
          'Invalid time string - space missing as date and time separator.')

    hours, minutes, seconds, microseconds, time_zone_offset = (
        self._CopyTimeFromString(time_string[11:]))

    date_time_values = {
        'year': year,
        'month': month,
        'day_of_month': day_of_month,
        'hours': hours,
        'minutes': minutes,
        'seconds': seconds}

    if microseconds is not None:
      date_time_values['microseconds'] = microseconds
    if time_zone_offset is not None:
      date_time_values['time_zone_offset'] = time_zone_offset

    return date_time_values

  def _CopyTimeFromString(self, time_string):
    """Copies a time from a string.

    Args:
      time_string (str): time value formatted as:
          hh:mm:ss.######[+-]##:##

          Where # are numeric digits ranging from 0 to 9 and the seconds
          fraction can be either 3 or 6 digits. The seconds fraction and
          time zone offset are optional.

    Returns:
      tuple[int, int, int, int, int]: hours, minutes, seconds, microseconds,
          time zone offset in minutes.

    Raises:
      ValueError: if the time string is invalid or not supported.
    """
    time_string_length = len(time_string)

    # The time string should at least contain 'hh:mm:ss'.
    if time_string_length < 8:
      raise ValueError('Time string too short.')

    if time_string[2] != ':' or time_string[5] != ':':
      raise ValueError('Invalid time string.')

    try:
      hours = int(time_string[0:2], 10)
    except ValueError:
      raise ValueError('Unable to parse hours.')

    if hours not in range(0, 24):
      raise ValueError(f'Hours value: {hours:d} out of bounds.')

    try:
      minutes = int(time_string[3:5], 10)
    except ValueError:
      raise ValueError('Unable to parse minutes.')

    if minutes not in range(0, 60):
      raise ValueError(f'Minutes value: {minutes:d} out of bounds.')

    try:
      seconds = int(time_string[6:8], 10)
    except ValueError:
      raise ValueError('Unable to parse day of seconds.')

    # TODO: support a leap second?
    if seconds not in range(0, 60):
      raise ValueError(f'Seconds value: {seconds:d} out of bounds.')

    microseconds = None
    time_zone_offset = None

    time_zone_string_index = 8
    while time_zone_string_index < time_string_length:
      if time_string[time_zone_string_index] in ('+', '-'):
        break

      time_zone_string_index += 1

    # The calculations that follow rely on the time zone string index
    # to point beyond the string in case no time zone offset was defined.
    if time_zone_string_index == time_string_length - 1:
      time_zone_string_index += 1

    if time_string_length > 8 and time_string[8] == '.':
      time_fraction_length = time_zone_string_index - 9
      if time_fraction_length not in (3, 6):
        raise ValueError('Invalid time string.')

      try:
        time_fraction = time_string[9:time_zone_string_index]
        time_fraction = int(time_fraction, 10)
      except ValueError:
        raise ValueError('Unable to parse time fraction.')

      if time_fraction_length == 3:
        time_fraction *= 1000

      microseconds = time_fraction

    if time_zone_string_index < time_string_length:
      if (time_string_length - time_zone_string_index != 6 or
          time_string[time_zone_string_index + 3] != ':'):
        raise ValueError('Invalid time string.')

      try:
        hours_from_utc = int(time_string[
            time_zone_string_index + 1:time_zone_string_index + 3])
      except ValueError:
        raise ValueError('Unable to parse time zone hours offset.')

      if hours_from_utc not in range(0, 15):
        raise ValueError('Time zone hours offset value out of bounds.')

      try:
        minutes_from_utc = int(time_string[
            time_zone_string_index + 4:time_zone_string_index + 6])
      except ValueError:
        raise ValueError('Unable to parse time zone minutes offset.')

      if minutes_from_utc not in range(0, 60):
        raise ValueError('Time zone minutes offset value out of bounds.')

      # pylint: disable=invalid-unary-operand-type
      time_zone_offset = (hours_from_utc * 60) + minutes_from_utc

      if time_string[time_zone_string_index] == '-':
        time_zone_offset = -time_zone_offset

    return hours, minutes, seconds, microseconds, time_zone_offset

  def _GetDateValues(
      self, number_of_days, epoch_year, epoch_month, epoch_day_of_month):
    """Determines date values.

    Args:
      number_of_days (int): number of days since epoch.
      epoch_year (int): year that is the start of the epoch e.g. 1970.
      epoch_month (int): month that is the start of the epoch, where
          1 represents January.
      epoch_day_of_month (int): day of month that is the start of the epoch,
          where 1 represents the first day.

    Returns:
       tuple[int, int, int]: year, month, day of month.

    Raises:
      ValueError: if the epoch year, month or day of month values are out
          of bounds.
    """
    if epoch_year < 0:
      raise ValueError(f'Epoch year value: {epoch_year:d} out of bounds.')

    if epoch_month not in range(1, 13):
      raise ValueError(f'Epoch month value: {epoch_month:d} out of bounds.')

    epoch_days_per_month = self._GetDaysPerMonth(epoch_year, epoch_month)
    if epoch_day_of_month < 1 or epoch_day_of_month > epoch_days_per_month:
      raise ValueError(
          f'Epoch day of month value: {epoch_day_of_month:d} out of bounds.')

    before_epoch = number_of_days < 0

    year = epoch_year
    month = epoch_month
    if before_epoch:
      month -= 1
      if month <= 0:
        month = 12
        year -= 1

    number_of_days += epoch_day_of_month
    if before_epoch:
      number_of_days *= -1

    # Align with the start of the year.
    while month > 1:
      days_per_month = self._GetDaysPerMonth(year, month)
      if number_of_days < days_per_month:
        break

      if before_epoch:
        month -= 1
      else:
        month += 1

      if month > 12:
        month = 1
        year += 1

      number_of_days -= days_per_month

    # Align with the start of the next century.
    _, remainder = divmod(year, 100)
    for _ in range(remainder, 100):
      days_in_year = self._GetNumberOfDaysInYear(year)
      if number_of_days < days_in_year:
        break

      if before_epoch:
        year -= 1
      else:
        year += 1

      number_of_days -= days_in_year

    days_in_century = self._GetNumberOfDaysInCentury(year)
    while number_of_days > days_in_century:
      if before_epoch:
        year -= 100
      else:
        year += 100

      number_of_days -= days_in_century
      days_in_century = self._GetNumberOfDaysInCentury(year)

    days_in_year = self._GetNumberOfDaysInYear(year)
    while number_of_days > days_in_year:
      if before_epoch:
        year -= 1
      else:
        year += 1

      number_of_days -= days_in_year
      days_in_year = self._GetNumberOfDaysInYear(year)

    days_per_month = self._GetDaysPerMonth(year, month)
    while number_of_days > days_per_month:
      if before_epoch:
        month -= 1
      else:
        month += 1

      if month <= 0:
        month = 12
        year -= 1
      elif month > 12:
        month = 1
        year += 1

      number_of_days -= days_per_month
      days_per_month = self._GetDaysPerMonth(year, month)

    if before_epoch:
      days_per_month = self._GetDaysPerMonth(year, month)
      number_of_days = days_per_month - number_of_days

    elif number_of_days == 0:
      number_of_days = 31
      month = 12
      year -= 1

    return year, month, number_of_days

  def _GetDateValuesWithEpoch(self, number_of_days, date_time_epoch):
    """Determines date values.

    Args:
      number_of_days (int): number of days since epoch.
      date_time_epoch (DateTimeEpoch): date and time of the epoch.

    Returns:
       tuple[int, int, int]: year, month, day of month.
    """
    return self._GetDateValues(
        number_of_days, date_time_epoch.year, date_time_epoch.month,
        date_time_epoch.day_of_month)

  def _GetDateWithTimeOfDay(self):
    """Retrieves the date with time of day.

    Note that the date and time are adjusted to UTC.

    Returns:
       tuple[int, int, int, int, int, int]: year, month, day of month, hours,
           minutes, seconds or (None, None, None, None, None, None)
           if the date and time values do not represent a date or time of day.
    """
    normalized_timestamp = self._GetNormalizedTimestamp()
    if normalized_timestamp is None:
      return None, None, None, None, None, None

    if (not self._cached_date_time_values or
        self._cached_date_time_values[0] != normalized_timestamp):
      number_of_days, hours, minutes, seconds = self._GetTimeValues(
          normalized_timestamp)

      try:
        year, month, day_of_month = self._GetDateValuesWithEpoch(
            number_of_days, self._EPOCH_NORMALIZED_TIME)

      except ValueError:
        return None, None, None, None, None, None

      self._cached_date_time_values = (
          normalized_timestamp, year, month, day_of_month, hours, minutes,
          seconds)

    return self._cached_date_time_values[1:]

  def _GetDayOfYear(self, year, month, day_of_month):
    """Retrieves the day of the year for a specific day of a month in a year.

    Args:
      year (int): year e.g. 1970.
      month (int): month, where 1 represents January.
      day_of_month (int): day of the month, where 1 represents the first day.

    Returns:
      int: day of year.

    Raises:
      ValueError: if the month or day of month value is out of bounds.
    """
    if month not in range(1, 13):
      raise ValueError('Month value out of bounds.')

    days_per_month = self._GetDaysPerMonth(year, month)
    if day_of_month < 1 or day_of_month > days_per_month:
      raise ValueError('Day of month value out of bounds.')

    day_of_year = day_of_month
    for past_month in range(1, month):
      day_of_year += self._GetDaysPerMonth(year, past_month)

    return day_of_year

  def _GetDaysPerMonth(self, year, month):
    """Retrieves the number of days in a month of a specific year.

    Args:
      year (int): year e.g. 1970.
      month (int): month, where 1 represents January.

    Returns:
      int: number of days in the month.

    Raises:
      ValueError: if the month value is out of bounds.
    """
    if month not in range(1, 13):
      raise ValueError('Month value out of bounds.')

    days_per_month = self._DAYS_PER_MONTH[month - 1]
    if month == 2 and self._IsLeapYear(year):
      days_per_month += 1

    return days_per_month

  @abc.abstractmethod
  def _GetNormalizedTimestamp(self):
    """Retrieves the normalized timestamp.

    Returns:
      decimal.Decimal: normalized timestamp, which contains the number of
          seconds since January 1, 1970 00:00:00 and a fraction of second used
          for increased precision, or None if the normalized timestamp cannot be
          determined.
    """

  def _GetNumberOfDaysInCentury(self, year):
    """Retrieves the number of days in a century.

    Args:
      year (int): year in the century e.g. 1970.

    Returns:
      int: number of (remaining) days in the century.

    Raises:
      ValueError: if the year value is out of bounds.
    """
    if year < 0:
      raise ValueError('Year value out of bounds.')

    year, _ = divmod(year, 100)

    if self._IsLeapYear(year):
      return 36525
    return 36524

  def _GetNumberOfDaysInYear(self, year):
    """Retrieves the number of days in a specific year.

    Args:
      year (int): year e.g. 1970.

    Returns:
      int: number of days in the year.
    """
    if self._IsLeapYear(year):
      return 366
    return 365

  def _GetNumberOfSecondsFromElements(
      self, year, month, day_of_month, hours, minutes, seconds):
    """Retrieves the number of seconds from the date and time elements.

    Args:
      year (int): year e.g. 1970.
      month (int): month, where 1 represents January.
      day_of_month (int): day of the month, where 1 represents the first day.
      hours (int): hours.
      minutes (int): minutes.
      seconds (int): seconds.

    Returns:
      int: number of seconds since January 1, 1970 00:00:00 or None if year,
          month or day of month are not set.

    Raises:
      ValueError: if the time elements are invalid.
    """
    if not year or not month or not day_of_month:
      return None

    # calendar.timegm does not sanity check the time elements.
    if hours is None:
      hours = 0
    elif hours not in range(0, 24):
      raise ValueError(f'Hours value: {hours!s} out of bounds.')

    if minutes is None:
      minutes = 0
    elif minutes not in range(0, 60):
      raise ValueError(f'Minutes value: {minutes!s} out of bounds.')

    # TODO: support a leap second?
    if seconds is None:
      seconds = 0
    elif seconds not in range(0, 60):
      raise ValueError(f'Seconds value: {seconds!s} out of bounds.')

    # Note that calendar.timegm() does not raise when date is: 2013-02-29.
    days_per_month = self._GetDaysPerMonth(year, month)
    if day_of_month < 1 or day_of_month > days_per_month:
      raise ValueError(f'Day of month value: {day_of_month:d} out of bounds.')

    # calendar.timegm requires the time tuple to contain at least
    # 6 integer values.
    time_elements_tuple = (year, month, day_of_month, hours, minutes, seconds)

    number_of_seconds = calendar.timegm(time_elements_tuple)

    return int(number_of_seconds)

  def _GetTimeValues(self, number_of_seconds):
    """Determines time values.

    Args:
      number_of_seconds (int|decimal.Decimal): number of seconds.

    Returns:
       tuple[int, int, int, int]: days, hours, minutes, seconds.
    """
    number_of_seconds = int(number_of_seconds)
    number_of_minutes, seconds = divmod(number_of_seconds, 60)
    number_of_hours, minutes = divmod(number_of_minutes, 60)
    number_of_days, hours = divmod(number_of_hours, 24)
    return number_of_days, hours, minutes, seconds

  def _IsLeapYear(self, year):
    """Determines if a year is a leap year.

    Args:
      year (int): year e.g. 1970.

    Returns:
      bool: True if the year is a leap year.
    """
    # pylint: disable=consider-using-ternary
    return (year % 4 == 0 and year % 100 != 0) or year % 400 == 0

  @abc.abstractmethod
  def CopyFromDateTimeString(self, time_string):
    """Copies a date time value from a date and time string.

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

  def CopyToPosixTimestamp(self):
    """Copies the date time value to a POSIX timestamp.

    Returns:
      int: a POSIX timestamp in seconds or None if no timestamp is available.
    """
    normalized_timestamp = self._GetNormalizedTimestamp()
    if normalized_timestamp is None:
      return None

    return int(normalized_timestamp)

  def CopyToPosixTimestampWithFractionOfSecond(self):
    """Copies the date time value to a POSIX timestamp with fraction of second.

    Returns:
      tuple[int, int]: a POSIX timestamp in seconds with fraction of second or
          None, None if no timestamp is available.
    """
    normalized_timestamp = self._GetNormalizedTimestamp()
    if normalized_timestamp is None:
      return None, None

    remainder_multiplier = self._REMAINDER_MULTIPLIER.get(self._precision, None)
    if remainder_multiplier:
      remainder = int((normalized_timestamp % 1) * remainder_multiplier)
    else:
      remainder = None

    return int(normalized_timestamp), remainder

  @abc.abstractmethod
  def CopyToDateTimeString(self):
    """Copies the date time value to a date and time string.

    Returns:
      str: date and time value formatted as: "YYYY-MM-DD hh:mm:ss.######" or
          None if the timestamp cannot be copied to a date and time string.
    """

  def CopyToDateTimeStringISO8601(self):
    """Copies the date time value to an ISO 8601 date and time string.

    Returns:
      str: date and time value formatted as an ISO 8601 date and time string or
          None if the timestamp cannot be copied to a date and time string.
    """
    date_time_string = self.CopyToDateTimeString()
    if date_time_string:
      date_time_string = date_time_string.replace(' ', 'T')

      if self._time_zone_offset is not None or not self.is_local_time:
        time_zone_offset_hours, time_zone_offset_minutes = divmod(
            self._time_zone_offset or 0, 60)
        if time_zone_offset_hours >= 0:
          time_zone_offset_sign = '+'
        else:
          time_zone_offset_sign = '-'
          time_zone_offset_hours *= -1

        time_zone_string = (
            f'{time_zone_offset_hours:02d}:{time_zone_offset_minutes:02d}')
        date_time_string = time_zone_offset_sign.join([
            date_time_string, time_zone_string])

    return date_time_string

  def GetDate(self):
    """Retrieves the date represented by the date and time values.

    Note that the date is adjusted to UTC.

    Returns:
       tuple[int, int, int]: year, month, day of month or (None, None, None)
           if the date and time values do not represent a date.
    """
    year, month, day_of_month, _, _, _ = self._GetDateWithTimeOfDay()
    return year, month, day_of_month

  def GetDateWithTimeOfDay(self):
    """Retrieves the date with time of day.

    Note that the date and time are adjusted to UTC.

    Returns:
       tuple[int, int, int, int, int, int]: year, month, day of month, hours,
           minutes, seconds or (None, None, None, None, None, None)
           if the date and time values do not represent a date or time of day.
    """
    return self._GetDateWithTimeOfDay()

  # TODO: remove this method when there is no more need for it in plaso.
  def GetPlasoTimestamp(self):
    """Retrieves a timestamp that is compatible with Plaso.

    Returns:
      int: a POSIX timestamp in microseconds or None if no timestamp is
          available.
    """
    normalized_timestamp = self._GetNormalizedTimestamp()
    if normalized_timestamp is None:
      return None

    normalized_timestamp *= definitions.MICROSECONDS_PER_SECOND
    normalized_timestamp = normalized_timestamp.quantize(
        1, rounding=decimal.ROUND_HALF_UP)
    return int(normalized_timestamp)

  def GetTimeOfDay(self):
    """Retrieves the time of day represented by the date and time values.

    Note that the time is adjusted to UTC.

    Returns:
       tuple[int, int, int]: hours, minutes, seconds or (None, None, None)
           if the date and time values do not represent a time of day.
    """
    _, _, _, hours, minutes, seconds = self._GetDateWithTimeOfDay()
    return hours, minutes, seconds
