# -*- coding: utf-8 -*-
"""Time elements implementation."""

import decimal

from dfdatetime import definitions
from dfdatetime import factory
from dfdatetime import interface
from dfdatetime import precisions


class TimeElements(interface.DateTimeValues):
  """Time elements.

  Time elements contain separate values for year, month, day of month,
  hours, minutes and seconds.

  Attributes:
    is_local_time (bool): True if the date and time value is in local time.
  """

  # Maps the RFC 822, RFC 1123 and RFC 2822 definitions to their corresponding
  # integer values.
  _RFC_MONTH_MAPPINGS = {
      'Jan': 1,
      'Feb': 2,
      'Mar': 3,
      'Apr': 4,
      'May': 5,
      'Jun': 6,
      'Jul': 7,
      'Aug': 8,
      'Sep': 9,
      'Oct': 10,
      'Nov': 11,
      'Dec': 12}

  _RFC_TIME_ZONE_MAPPINGS = {
      'UT': 0,
      'GMT':  0,
      'EST': -5,
      'EDT': -4,
      'CST': -6,
      'CDT': -5,
      'MST': -7,
      'MDT': -6,
      'PST': -8,
      'PDT': -7,
      'A': -1,
      'B': -2,
      'C': -3,
      'D': -4,
      'E': -5,
      'F': -6,
      'G': -7,
      'H': -8,
      'I': -9,
      'K': -10,
      'L': -11,
      'M': -12,
      'N': 1,
      'O': 2,
      'P': 3,
      'Q': 4,
      'R': 5,
      'S': 6,
      'T': 7,
      'U': 8,
      'V': 9,
      'W': 10,
      'X': 11,
      'Y': 12,
      'Z': 0}

  _RFC_WEEKDAYS = frozenset(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])

  def __init__(
      self, precision=None, time_elements_tuple=None, time_zone_offset=None):
    """Initializes time elements.

    Args:
      precision (Optional[str]): precision of the date and time value, which
          should be one of the PRECISION_VALUES in definitions.
      time_elements_tuple (Optional[tuple[int, int, int, int, int, int]]):
          time elements, contains year, month, day of month, hours, minutes and
          seconds.
      time_zone_offset (Optional[int]): time zone offset in number of minutes
          from UTC or None if not set.

    Raises:
      ValueError: if the time elements tuple is invalid.
    """
    super(TimeElements, self).__init__(
        precision=precision or definitions.PRECISION_1_SECOND,
        time_zone_offset=time_zone_offset)
    self._number_of_seconds = None
    self._time_elements_tuple = time_elements_tuple

    if time_elements_tuple:
      number_of_elements = len(time_elements_tuple)
      if number_of_elements < 6:
        raise ValueError((
            f'Invalid time elements tuple at least 6 elements required,'
            f'got: {number_of_elements:d}'))

      self._number_of_seconds = self._GetNumberOfSecondsFromElements(
          time_elements_tuple[0], time_elements_tuple[1],
          time_elements_tuple[2], time_elements_tuple[3],
          time_elements_tuple[4], time_elements_tuple[5])

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
        self._normalized_timestamp = decimal.Decimal(self._number_of_seconds)

        if self._time_zone_offset:
          self._normalized_timestamp -= self._time_zone_offset * 60

    return self._normalized_timestamp

  def _CopyDateTimeFromStringISO8601(self, time_string):
    """Copies a date and time from an ISO 8601 date and time string.

    Args:
      time_string (str): time value formatted as:
          hh:mm:ss.######[+-]##:##

          Where # are numeric digits ranging from 0 to 9 and the seconds
          fraction can be either 3 or 6 digits. The fraction of second and
          time zone offset are optional.

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
    # contain 'YYYY-MM-DDThh'.
    if time_string[10] != 'T':
      raise ValueError('Invalid time string - missing date and time separator.')

    hours, minutes, seconds, microseconds, time_zone_offset = (
        self._CopyTimeFromStringISO8601(time_string[11:]))

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

  def _CopyDateTimeFromStringRFC822(self, time_string):
    """Copies a date and time from a RFC 822 date and time string.

    Args:
      time_string (str): date and time value formatted as:
          DAY, D MONTH YY hh:mm:ss ZONE

          Where weekday (DAY) and seconds (ss) are optional and day of
          month (D) can consist of 1 or 2 digits.

    Returns:
      dict[str, int]: date and time values, such as year, month, day of month,
          hours, minutes, seconds, time zone offset in minutes.

    Raises:
      ValueError: if the time string is invalid or not supported.
    """
    if not time_string:
      raise ValueError('Invalid time string.')

    string_segments = time_string.split(' ')

    if len(string_segments) not in (5, 6):
      raise ValueError('Unsupported number of time string segments.')

    weekday_string = string_segments[0]
    if weekday_string.endswith(','):
      weekday_string = weekday_string[:-1]
      if weekday_string not in self._RFC_WEEKDAYS:
        raise ValueError(f'Invalid weekday: {weekday_string:s}.')

      string_segments.pop(0)

    day_of_month_string = string_segments[0]

    day_of_month = 0
    if len(day_of_month_string) in (1, 2):
      try:
        day_of_month = int(day_of_month_string, 10)
      except ValueError:
        pass

    if day_of_month == 0:
      raise ValueError(f'Invalid day of month: {day_of_month_string:s}.')

    month_string = string_segments[1]

    month = self._RFC_MONTH_MAPPINGS.get(month_string)
    if not month:
      raise ValueError(f'Invalid month: {month_string:s}.')

    year_string = string_segments[2]

    year = None
    if len(year_string) == 2:
      try:
        year = int(year_string, 10)
      except ValueError:
        pass

    if year is None:
      raise ValueError(f'Invalid year: {0:s}.')

    year += 1900

    hours, minutes, seconds, time_zone_offset = self._CopyTimeFromStringRFC(
        string_segments[3], string_segments[4])

    date_time_values = {
        'year': year,
        'month': month,
        'day_of_month': day_of_month,
        'hours': hours,
        'minutes': minutes,
        'time_zone_offset': time_zone_offset}

    if seconds is not None:
      date_time_values['seconds'] = seconds

    return date_time_values

  def _CopyDateTimeFromStringRFC1123(self, time_string):
    """Copies a date and time from a RFC 1123 date and time string.

    Args:
      time_string (str): date and time value formatted as:
          DAY, D MONTH YYYY hh:mm:ss ZONE

          Where weekday (DAY) and seconds (ss) are optional and day of
          month (D) can consist of 1 or 2 digits.

    Returns:
      dict[str, int]: date and time values, such as year, month, day of month,
          hours, minutes, seconds, time zone offset in minutes.

    Raises:
      ValueError: if the time string is invalid or not supported.
    """
    if not time_string:
      raise ValueError('Invalid time string.')

    string_segments = time_string.split(' ')

    if len(string_segments) not in (5, 6):
      raise ValueError('Unsupported number of time string segments.')

    weekday_string = string_segments[0]
    if weekday_string.endswith(','):
      weekday_string = weekday_string[:-1]
      if weekday_string not in self._RFC_WEEKDAYS:
        raise ValueError(f'Invalid weekday: {weekday_string:s}.')

      string_segments.pop(0)

    day_of_month_string = string_segments[0]

    day_of_month = 0
    if len(day_of_month_string) in (1, 2):
      try:
        day_of_month = int(day_of_month_string, 10)
      except ValueError:
        pass

    if day_of_month == 0:
      raise ValueError(f'Invalid day of month: {day_of_month_string:s}.')

    month_string = string_segments[1]

    month = self._RFC_MONTH_MAPPINGS.get(month_string)
    if not month:
      raise ValueError(f'Invalid month: {month_string:s}.')

    year_string = string_segments[2]

    year = None
    if len(year_string) == 4:
      try:
        year = int(year_string, 10)
      except ValueError:
        pass

    if year is None:
      raise ValueError(f'Invalid year: {year_string:s}.')

    hours, minutes, seconds, time_zone_offset = self._CopyTimeFromStringRFC(
        string_segments[3], string_segments[4])

    date_time_values = {
        'year': year,
        'month': month,
        'day_of_month': day_of_month,
        'hours': hours,
        'minutes': minutes,
        'time_zone_offset': time_zone_offset}

    if seconds is not None:
      date_time_values['seconds'] = seconds

    return date_time_values

  def _CopyFromDateTimeValues(self, date_time_values):
    """Copies time elements from date and time values.

    Args:
      date_time_values  (dict[str, int]): date and time values, such as year,
          month, day of month, hours, minutes, seconds, microseconds, time zone
          offset in minutes.
    """
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
    self._time_elements_tuple = (
        year, month, day_of_month, hours, minutes, seconds)
    self._time_zone_offset = time_zone_offset

  def _CopyTimeFromStringISO8601(self, time_string):
    """Copies a time from an ISO 8601 time string.

    Args:
      time_string (str): time value formatted as:
          hh:mm:ss.######[+-]##:##

          Where # are numeric digits ranging from 0 to 9 and the seconds
          fraction can be either 3 or 6 digits. The faction of second and
          time zone offset are optional.

    Returns:
      tuple[int, int, int, int, int]: hours, minutes, seconds, microseconds,
          time zone offset in minutes.

    Raises:
      ValueError: if the time string is invalid or not supported.
    """
    if time_string.endswith('Z'):
      time_string = ''.join([time_string[:-1], '+00:00'])

    time_string_length = len(time_string)

    # The time string should at least contain 'hh'.
    if time_string_length < 2:
      raise ValueError('Time string too short.')

    try:
      hours = int(time_string[0:2], 10)
    except ValueError:
      raise ValueError('Unable to parse hours.')

    if hours not in range(0, 24):
      raise ValueError(f'Hours value: {hours:d} out of bounds.')

    minutes = None
    seconds = None
    microseconds = None
    time_zone_offset = None

    time_string_index = 2

    # Minutes are either specified as 'hhmm', 'hh:mm' or as a fractional part
    # 'hh[.,]###'.
    if (time_string_index + 1 < time_string_length and
        time_string[time_string_index] not in ('.', ',')):
      if time_string[time_string_index] == ':':
        time_string_index += 1

      if time_string_index + 2 > time_string_length:
        raise ValueError('Time string too short.')

      try:
        minutes = time_string[time_string_index:time_string_index + 2]
        minutes = int(minutes, 10)
      except ValueError:
        raise ValueError('Unable to parse minutes.')

      time_string_index += 2

    # Seconds are either specified as 'hhmmss', 'hh:mm:ss' or as a fractional
    # part 'hh:mm[.,]###' or 'hhmm[.,]###'.
    if (time_string_index + 1 < time_string_length and
        time_string[time_string_index] not in ('.', ',')):
      if time_string[time_string_index] == ':':
        time_string_index += 1

      if time_string_index + 2 > time_string_length:
        raise ValueError('Time string too short.')

      try:
        seconds = time_string[time_string_index:time_string_index + 2]
        seconds = int(seconds, 10)
      except ValueError:
        raise ValueError('Unable to parse day of seconds.')

      time_string_index += 2

    time_zone_string_index = time_string_index
    while time_zone_string_index < time_string_length:
      if time_string[time_zone_string_index] in ('+', '-'):
        break

      time_zone_string_index += 1

    # The calculations that follow rely on the time zone string index
    # to point beyond the string in case no time zone offset was defined.
    if time_zone_string_index == time_string_length - 1:
      time_zone_string_index += 1

    if (time_string_length > time_string_index and
        time_string[time_string_index] in ('.', ',')):
      time_string_index += 1
      time_fraction_length = time_zone_string_index - time_string_index

      try:
        time_fraction = time_string[time_string_index:time_zone_string_index]
        time_fraction = int(time_fraction, 10)
        time_fraction = (
            decimal.Decimal(time_fraction) /
            decimal.Decimal(10 ** time_fraction_length))
      except ValueError:
        raise ValueError('Unable to parse time fraction.')

      if minutes is None:
        time_fraction *= 60
        minutes = int(time_fraction)
        time_fraction -= minutes

      if seconds is None:
        time_fraction *= 60
        seconds = int(time_fraction)
        time_fraction -= seconds

      time_fraction *= definitions.MICROSECONDS_PER_SECOND
      microseconds = int(time_fraction)

    if minutes is not None and minutes not in range(0, 60):
      raise ValueError(f'Minutes value: {minutes:d} out of bounds.')

    # TODO: support a leap second?
    if seconds is not None and seconds not in range(0, 60):
      raise ValueError(f'Seconds value: {seconds:d} out of bounds.')

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

  def _CopyTimeFromStringRFC(self, time_string, time_zone_string):
    """Copies a time from a RFC 822, RFC 1123 or RFC 2822 time string.

    Args:
      time_string (str): time value formatted as: hh:mm[:ss], where seconds (ss)
          are optional.
      time_zone_string (str): time zone value formatted as predefined time zone
          indicator or [+-]HHMM

    Returns:
      tuple[int, int, int, int]: hours, minutes, seconds, time zone offset in
          minutes.

    Raises:
      ValueError: if the time string is invalid or not supported.
    """
    time_string_length = len(time_string)

    # The time string should at least contain 'hh:mm'.
    if time_string_length < 5:
      raise ValueError('Time string too short.')

    if time_string_length > 8:
      raise ValueError('Time string too long.')

    if time_string[2] != ':':
      raise ValueError('Invalid hours and minutes separator.')

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

    seconds = None

    if time_string_length > 5:
      if time_string_length < 8:
        raise ValueError('Time string too short.')

      if time_string[5] != ':':
        raise ValueError('Invalid minutes and seconds separator.')

      try:
        seconds = int(time_string[6:8], 10)
      except ValueError:
        raise ValueError('Unable to parse seconds.')

      if seconds not in range(0, 60):
        raise ValueError(f'Seconds value: {seconds:d} out of bounds.')

    if time_string_length < 5:
      raise ValueError('Time string too short.')

    time_zone_string_length = len(time_zone_string)
    if time_zone_string_length > 5:
      raise ValueError('Time zone string too long.')

    if time_zone_string_length < 5:
      hours_from_utc = self._RFC_TIME_ZONE_MAPPINGS.get(time_zone_string, None)
      minutes_from_utc = 0
      if hours_from_utc is None:
        raise ValueError(f'Invalid time zone: {time_zone_string:s}.')

    else:
      if time_zone_string[0] not in ('+', '-'):
        raise ValueError(f'Invalid time zone: {time_zone_string:s}.')

      try:
        hours_from_utc = int(time_zone_string[1:3], 10)
      except ValueError:
        raise ValueError('Unable to parse time zone hours offset.')

      if hours_from_utc not in range(0, 15):
        raise ValueError('Time zone hours offset value out of bounds.')

      try:
        minutes_from_utc = int(time_zone_string[3:5], 10)
      except ValueError:
        raise ValueError('Unable to parse time zone minutes offset.')

      if minutes_from_utc not in range(0, 60):
        raise ValueError('Time zone minutes offset value out of bounds.')

    time_zone_offset = (hours_from_utc * 60) + minutes_from_utc
    if time_zone_string[0] == '-':
      time_zone_offset = -time_zone_offset

    return hours, minutes, seconds, time_zone_offset

  @property
  def day_of_month(self):
    """int: day of month or None if not set."""
    if not self._time_elements_tuple:
      return None
    return self._time_elements_tuple[2]

  @property
  def hours(self):
    """int: number of hours or None if not set."""
    if not self._time_elements_tuple:
      return None
    return self._time_elements_tuple[3]

  @property
  def minutes(self):
    """int: number of minutes or None if not set."""
    if not self._time_elements_tuple:
      return None
    return self._time_elements_tuple[4]

  @property
  def month(self):
    """int: month or None if not set."""
    if not self._time_elements_tuple:
      return None
    return self._time_elements_tuple[1]

  @property
  def seconds(self):
    """int: number of seconds or None if not set."""
    if not self._time_elements_tuple:
      return None
    return self._time_elements_tuple[5]

  @property
  def year(self):
    """int: year or None if not set."""
    if not self._time_elements_tuple:
      return None
    return self._time_elements_tuple[0]

  def CopyFromDatetime(self, datetime_object):
    """Copies time elements from a Python datetime object.

    A naive datetime object is considered in local time.

    Args:
      datetime_object (datetime.datetime): Python datetime object.
    """
    year, month, day_of_month, hours, minutes, seconds, _, _, _ = (
        datetime_object.utctimetuple())

    date_time_values = {
        'year': year,
        'month': month,
        'day_of_month': day_of_month,
        'hours': hours,
        'minutes': minutes,
        'seconds': seconds}

    self._CopyFromDateTimeValues(date_time_values)

    self.is_local_time = bool(datetime_object.tzinfo is None)

  def CopyFromDateTimeString(self, time_string):
    """Copies time elements from a date and time string.

    Args:
      time_string (str): date and time value formatted as:
          YYYY-MM-DD hh:mm:ss.######[+-]##:##

          Where # are numeric digits ranging from 0 to 9 and the seconds
          fraction can be either 3 or 6 digits. The time of day, seconds
          fraction and time zone offset are optional. The default time zone
          is UTC.
    """
    date_time_values = self._CopyDateTimeFromString(time_string)

    self._CopyFromDateTimeValues(date_time_values)

  def CopyFromStringISO8601(self, time_string):
    """Copies time elements from an ISO 8601 date and time string.

    Currently not supported:
    * Duration notation: "P..."
    * Week notation "2016-W33"
    * Date with week number notation "2016-W33-3"
    * Date without year notation "--08-17"
    * Ordinal date notation "2016-230"

    Args:
      time_string (str): date and time value formatted as:
          YYYY-MM-DDThh:mm:ss.######[+-]##:##

          Where # are numeric digits ranging from 0 to 9 and the seconds
          fraction can be either 3 or 6 digits. The time of day, seconds
          fraction and time zone offset are optional. The default time zone
          is UTC.

    Raises:
      ValueError: if the time string is invalid or not supported.
    """
    date_time_values = self._CopyDateTimeFromStringISO8601(time_string)

    self._CopyFromDateTimeValues(date_time_values)

  def CopyFromStringRFC822(self, time_string):
    """Copies time elements from a RFC 822 date and time string.

    Args:
      time_string (str): date and time value formatted as:
          DAY, D MONTH YY hh:mm:ss ZONE

          Where weekday (DAY) and seconds (ss) are optional and day of
          month (D) can consist of 1 or 2 digits.

    Raises:
      ValueError: if the time string is invalid or not supported.
    """
    date_time_values = self._CopyDateTimeFromStringRFC822(time_string)

    self._CopyFromDateTimeValues(date_time_values)

  def CopyFromStringRFC1123(self, time_string):
    """Copies time elements from a RFC 1123 date and time string.

    Args:
      time_string (str): date and time value formatted as:
          DAY, D MONTH YYYY hh:mm:ss ZONE

          Where weekday (DAY) and seconds (ss) are optional and day of
          month (D) can consist of 1 or 2 digits.

    Raises:
      ValueError: if the time string is invalid or not supported.
    """
    date_time_values = self._CopyDateTimeFromStringRFC1123(time_string)

    self._CopyFromDateTimeValues(date_time_values)

  def CopyFromStringTuple(self, time_elements_tuple):
    """Copies time elements from string-based time elements tuple.

    Args:
      time_elements_tuple (Optional[tuple[str, str, str, str, str, str]]):
          time elements, contains year, month, day of month, hours, minutes and
          seconds.

    Raises:
      ValueError: if the time elements tuple is invalid.
    """
    number_of_elements = len(time_elements_tuple)
    if number_of_elements < 6:
      raise ValueError((
          f'Invalid time elements tuple at least 6 elements required,'
          f'got: {number_of_elements:d}'))

    year_string = time_elements_tuple[0]
    month_string = time_elements_tuple[1]
    day_of_month_string = time_elements_tuple[2]
    hours_string = time_elements_tuple[3]
    minutes_string = time_elements_tuple[4]
    seconds_string = time_elements_tuple[5]

    try:
      year = int(year_string, 10)
    except (TypeError, ValueError):
      raise ValueError(f'Invalid year value: {year_string!s}')

    try:
      month = int(month_string, 10)
    except (TypeError, ValueError):
      raise ValueError(f'Invalid month value: {month_string!s}')

    try:
      day_of_month = int(day_of_month_string, 10)
    except (TypeError, ValueError):
      raise ValueError(f'Invalid day of month value: {day_of_month_string!s}')

    try:
      hours = int(hours_string, 10)
    except (TypeError, ValueError):
      raise ValueError(f'Invalid hours value: {hours_string!s}')

    try:
      minutes = int(minutes_string, 10)
    except (TypeError, ValueError):
      raise ValueError(f'Invalid minutes value: {minutes_string!s}')

    try:
      seconds = int(seconds_string, 10)
    except (TypeError, ValueError):
      raise ValueError(f'Invalid seconds value: {seconds_string!s}')

    self._normalized_timestamp = None
    self._number_of_seconds = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds)
    self._time_elements_tuple = (
        year, month, day_of_month, hours, minutes, seconds)

  def CopyToDateTimeString(self):
    """Copies the time elements to a date and time string.

    Returns:
      str: date and time value formatted as: "YYYY-MM-DD hh:mm:ss" or None
          if time elements are missing.
    """
    if self._number_of_seconds is None:
      return None

    year, month, day_of_month, hours, minutes, seconds = (
        self._time_elements_tuple)

    return (
        f'{year:04d}-{month:02d}-{day_of_month:02d} '
        f'{hours:02d}:{minutes:02d}:{seconds:02d}')


class TimeElementsWithFractionOfSecond(TimeElements):
  """Time elements with a fraction of second interface.

  Attributes:
    fraction_of_second (decimal.Decimal): fraction of second, which must be a
        value between 0.0 and 1.0.
    is_local_time (bool): True if the date and time value is in local time.
  """

  def __init__(
      self, fraction_of_second=None, precision=None, time_elements_tuple=None,
      time_zone_offset=None):
    """Initializes time elements.

    Args:
      fraction_of_second (Optional[decimal.Decimal]): fraction of second, which
          must be a value between 0.0 and 1.0.
      precision (Optional[str]): precision of the date and time value, which
          should be one of the PRECISION_VALUES in definitions.
      time_elements_tuple (Optional[tuple[int, int, int, int, int, int]]):
          time elements, contains year, month, day of month, hours, minutes and
          seconds.
      time_zone_offset (Optional[int]): time zone offset in number of minutes
          from UTC or None if not set.

    Raises:
      ValueError: if the time elements tuple is invalid or fraction of second
          value is out of bounds.
    """
    if fraction_of_second is not None:
      if fraction_of_second < 0.0 or fraction_of_second >= 1.0:
        raise ValueError(
            f'Fraction of second value: {fraction_of_second:f} out of bounds.')

    super(TimeElementsWithFractionOfSecond, self).__init__(
        precision=precision or definitions.PRECISION_1_SECOND,
        time_elements_tuple=time_elements_tuple,
        time_zone_offset=time_zone_offset)
    self.fraction_of_second = fraction_of_second

  def _GetNormalizedTimestamp(self):
    """Retrieves the normalized timestamp.

    Returns:
      decimal.Decimal: normalized timestamp, which contains the number of
          seconds since January 1, 1970 00:00:00 and a fraction of second used
          for increased precision, or None if the normalized timestamp cannot be
          determined.
    """
    if self._normalized_timestamp is None:
      if (self._number_of_seconds is not None and
          self.fraction_of_second is not None):
        self._normalized_timestamp = (
            decimal.Decimal(self._number_of_seconds) + self.fraction_of_second)

        if self._time_zone_offset:
          self._normalized_timestamp -= self._time_zone_offset * 60

    return self._normalized_timestamp

  def _CopyFromDateTimeValues(self, date_time_values):
    """Copies time elements from date and time values.

    Args:
      date_time_values  (dict[str, int]): date and time values, such as year,
          month, day of month, hours, minutes, seconds, microseconds, time zone
          offset in minutes.

    Raises:
      ValueError: if no helper can be created for the current precision.
    """
    year = date_time_values.get('year', 0)
    month = date_time_values.get('month', 0)
    day_of_month = date_time_values.get('day_of_month', 0)
    hours = date_time_values.get('hours', 0)
    minutes = date_time_values.get('minutes', 0)
    seconds = date_time_values.get('seconds', 0)
    microseconds = date_time_values.get('microseconds', 0)
    time_zone_offset = date_time_values.get('time_zone_offset', 0)

    precision_helper = precisions.PrecisionHelperFactory.CreatePrecisionHelper(
        self._precision)

    fraction_of_second = precision_helper.CopyMicrosecondsToFractionOfSecond(
        microseconds)

    self._normalized_timestamp = None
    self._number_of_seconds = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds)
    self._time_elements_tuple = (
        year, month, day_of_month, hours, minutes, seconds)
    self._time_zone_offset = time_zone_offset

    self.fraction_of_second = fraction_of_second

  def CopyFromDatetime(self, datetime_object):
    """Copies time elements from a Python datetime object.

    A naive datetime object is considered in local time.

    Args:
      datetime_object (datetime.datetime): Python datetime object.
    """
    super(TimeElementsWithFractionOfSecond, self).CopyFromDatetime(
        datetime_object)

    precision_helper = precisions.PrecisionHelperFactory.CreatePrecisionHelper(
        self._precision)

    fraction_of_second = precision_helper.CopyMicrosecondsToFractionOfSecond(
        datetime_object.microsecond)
    self.fraction_of_second = fraction_of_second

  def CopyFromStringTuple(self, time_elements_tuple):
    """Copies time elements from string-based time elements tuple.

    Args:
      time_elements_tuple (Optional[tuple[str, str, str, str, str, str, str]]):
          time elements, contains year, month, day of month, hours, minutes,
          seconds and fraction of seconds.

    Raises:
      ValueError: if the time elements tuple is invalid.
    """
    number_of_elements = len(time_elements_tuple)
    if number_of_elements < 7:
      raise ValueError((
          f'Invalid time elements tuple at least 7 elements required,'
          f'got: {number_of_elements:d}'))

    super(TimeElementsWithFractionOfSecond, self).CopyFromStringTuple(
        time_elements_tuple)

    fraction_of_second_string = time_elements_tuple[6]

    try:
      fraction_of_second = decimal.Decimal(fraction_of_second_string)
    except (TypeError, ValueError):
      raise ValueError(
          f'Invalid fraction of second value: {fraction_of_second_string!s}')

    if fraction_of_second < 0.0 or fraction_of_second >= 1.0:
      raise ValueError(
          f'Fraction of second value: {fraction_of_second:f} out of bounds.')

    self.fraction_of_second = fraction_of_second

  def CopyToDateTimeString(self):
    """Copies the time elements to a date and time string.

    Returns:
      str: date and time value formatted as: "YYYY-MM-DD hh:mm:ss" or
          "YYYY-MM-DD hh:mm:ss.######" or None if time elements are missing.

    Raises:
      ValueError: if the precision value is unsupported.
    """
    if self._number_of_seconds is None or self.fraction_of_second is None:
      return None

    precision_helper = precisions.PrecisionHelperFactory.CreatePrecisionHelper(
        self._precision)

    return precision_helper.CopyToDateTimeString(
        self._time_elements_tuple, self.fraction_of_second)


class TimeElementsInMilliseconds(TimeElementsWithFractionOfSecond):
  """Time elements in milliseconds.

  Attributes:
    fraction_of_second (decimal.Decimal): fraction of second, which must be a
        value between 0.0 and 1.0.
    is_local_time (bool): True if the date and time value is in local time.
    precision (str): precision of the date of the date and time value, that
        represents 1 millisecond (PRECISION_1_MILLISECOND).
  """

  def __init__(
      self, precision=None, time_elements_tuple=None, time_zone_offset=None):
    """Initializes time elements.

    Args:
      precision (Optional[str]): precision of the date and time value, which
          should be one of the PRECISION_VALUES in definitions.
      time_elements_tuple (Optional[tuple[int, int, int, int, int, int, int]]):
          time elements, contains year, month, day of month, hours, minutes,
          seconds and milliseconds.
      time_zone_offset (Optional[int]): time zone offset in number of minutes
          from UTC or None if not set.

    Raises:
      ValueError: if the time elements tuple is invalid.
    """
    fraction_of_second = None
    if time_elements_tuple:
      number_of_elements = len(time_elements_tuple)
      if number_of_elements < 7:
        raise ValueError((
            f'Invalid time elements tuple at least 7 elements required,'
            f'got: {number_of_elements:d}'))

      milliseconds = time_elements_tuple[6]
      time_elements_tuple = time_elements_tuple[:6]

      if (milliseconds < 0 or
          milliseconds >= definitions.MILLISECONDS_PER_SECOND):
        raise ValueError('Invalid number of milliseconds.')

      fraction_of_second = (
          decimal.Decimal(milliseconds) / definitions.MILLISECONDS_PER_SECOND)

    super(TimeElementsInMilliseconds, self).__init__(
        fraction_of_second=fraction_of_second,
        precision=precision or definitions.PRECISION_1_MILLISECOND,
        time_elements_tuple=time_elements_tuple,
        time_zone_offset=time_zone_offset)

  @property
  def milliseconds(self):
    """int: number of milliseconds."""
    return int(self.fraction_of_second * definitions.MILLISECONDS_PER_SECOND)

  def CopyFromStringTuple(self, time_elements_tuple):
    """Copies time elements from string-based time elements tuple.

    Args:
      time_elements_tuple (Optional[tuple[str, str, str, str, str, str, str]]):
          time elements, contains year, month, day of month, hours, minutes,
          seconds and milliseconds.

    Raises:
      ValueError: if the time elements tuple is invalid.
    """
    number_of_elements = len(time_elements_tuple)
    if len(time_elements_tuple) < 7:
      raise ValueError((
          f'Invalid time elements tuple at least 7 elements required,'
          f'got: {number_of_elements:d}'))

    year, month, day_of_month, hours, minutes, seconds, milliseconds = (
        time_elements_tuple)

    try:
      milliseconds = int(milliseconds, 10)
    except (TypeError, ValueError):
      raise ValueError(f'Invalid millisecond value: {milliseconds!s}')

    if milliseconds < 0 or milliseconds >= definitions.MILLISECONDS_PER_SECOND:
      raise ValueError('Invalid number of milliseconds.')

    fraction_of_second = (
        decimal.Decimal(milliseconds) / definitions.MILLISECONDS_PER_SECOND)

    time_elements_tuple = (
        year, month, day_of_month, hours, minutes, seconds,
        str(fraction_of_second))

    super(TimeElementsInMilliseconds, self).CopyFromStringTuple(
        time_elements_tuple)


class TimeElementsInMicroseconds(TimeElementsWithFractionOfSecond):
  """Time elements in microseconds.

  Attributes:
    fraction_of_second (decimal.Decimal): fraction of second, which must be a
        value between 0.0 and 1.0.
    is_local_time (bool): True if the date and time value is in local time.
    precision (str): precision of the date of the date and time value, that
        represents 1 microsecond (PRECISION_1_MICROSECOND).
  """

  def __init__(
      self, precision=None, time_elements_tuple=None, time_zone_offset=None):
    """Initializes time elements.

    Args:
      precision (Optional[str]): precision of the date and time value, which
          should be one of the PRECISION_VALUES in definitions.
      time_elements_tuple (Optional[tuple[int, int, int, int, int, int, int]]):
          time elements, contains year, month, day of month, hours, minutes,
          seconds and microseconds.
      time_zone_offset (Optional[int]): time zone offset in number of minutes
          from UTC or None if not set.

    Raises:
      ValueError: if the time elements tuple is invalid.
    """
    fraction_of_second = None
    if time_elements_tuple:
      number_of_elements = len(time_elements_tuple)
      if number_of_elements < 7:
        raise ValueError((
            f'Invalid time elements tuple at least 7 elements required,'
            f'got: {number_of_elements:d}'))

      microseconds = time_elements_tuple[6]
      time_elements_tuple = time_elements_tuple[:6]

      if (microseconds < 0 or
          microseconds >= definitions.MICROSECONDS_PER_SECOND):
        raise ValueError('Invalid number of microseconds.')

      fraction_of_second = (
          decimal.Decimal(microseconds) / definitions.MICROSECONDS_PER_SECOND)

    super(TimeElementsInMicroseconds, self).__init__(
        fraction_of_second=fraction_of_second,
        precision=precision or definitions.PRECISION_1_MICROSECOND,
        time_elements_tuple=time_elements_tuple,
        time_zone_offset=time_zone_offset)

  @property
  def microseconds(self):
    """int: number of microseconds."""
    return int(self.fraction_of_second * definitions.MICROSECONDS_PER_SECOND)

  def CopyFromStringTuple(self, time_elements_tuple):
    """Copies time elements from string-based time elements tuple.

    Args:
      time_elements_tuple (Optional[tuple[str, str, str, str, str, str, str]]):
          time elements, contains year, month, day of month, hours, minutes,
          seconds and microseconds.

    Raises:
      ValueError: if the time elements tuple is invalid.
    """
    number_of_elements = len(time_elements_tuple)
    if len(time_elements_tuple) < 7:
      raise ValueError((
          f'Invalid time elements tuple at least 7 elements required,'
          f'got: {number_of_elements:d}'))

    year, month, day_of_month, hours, minutes, seconds, microseconds = (
        time_elements_tuple)

    try:
      microseconds = int(microseconds, 10)
    except (TypeError, ValueError):
      raise ValueError(f'Invalid microsecond value: {microseconds!s}')

    if microseconds < 0 or microseconds >= definitions.MICROSECONDS_PER_SECOND:
      raise ValueError('Invalid number of microseconds.')

    fraction_of_second = (
        decimal.Decimal(microseconds) / definitions.MICROSECONDS_PER_SECOND)

    time_elements_tuple = (
        year, month, day_of_month, hours, minutes, seconds,
        str(fraction_of_second))

    super(TimeElementsInMicroseconds, self).CopyFromStringTuple(
        time_elements_tuple)


factory.Factory.RegisterDateTimeValues(TimeElements)
factory.Factory.RegisterDateTimeValues(TimeElementsInMilliseconds)
factory.Factory.RegisterDateTimeValues(TimeElementsInMicroseconds)
