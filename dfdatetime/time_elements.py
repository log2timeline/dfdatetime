# -*- coding: utf-8 -*-
"""Time elements implementation."""

from __future__ import unicode_literals

import decimal

from dfdatetime import definitions
from dfdatetime import interface
from dfdatetime import precisions


class TimeElements(interface.DateTimeValues):
  """Time elements.

  Time elements contain separate values for year, month, day of month,
  hours, minutes and seconds.

  Attributes:
    is_local_time (bool): True if the date and time value is in local time.
  """

  def __init__(self, time_elements_tuple=None):
    """Initializes time elements.

    Args:
      time_elements_tuple (Optional[tuple[int, int, int, int, int, int]]):
          time elements, contains year, month, day of month, hours, minutes and
          seconds.

    Raises:
      ValueError: if the time elements tuple is invalid.
    """
    super(TimeElements, self).__init__()
    self._number_of_seconds = None
    self._precision = definitions.PRECISION_1_SECOND
    self._time_elements_tuple = time_elements_tuple

    if time_elements_tuple:
      if len(time_elements_tuple) < 6:
        raise ValueError((
            'Invalid time elements tuple at least 6 elements required,'
            'got: {0:d}').format(len(time_elements_tuple)))

      self._number_of_seconds = self._GetNumberOfSecondsFromElements(
          *time_elements_tuple)

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
      tuple[int, int, int, int, int]: hours, minutes, seconds, microseconds,
          time zone offset in minutes.

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
      raise ValueError(
          'Invalid time string - missing as date and time separator.')

    hours, minutes, seconds, microseconds, time_zone_offset = (
        self._CopyTimeFromStringISO8601(time_string[11:]))

    if time_zone_offset:
      year, month, day_of_month, hours, minutes = self._AdjustForTimeZoneOffset(
          year, month, day_of_month, hours, minutes, time_zone_offset)

    date_time_values = {
        'year': year,
        'month': month,
        'day_of_month': day_of_month,
        'hours': hours,
        'minutes': minutes,
        'seconds': seconds}

    if microseconds is not None:
      date_time_values['microseconds'] = microseconds
    return date_time_values

  def _CopyFromDateTimeValues(self, date_time_values):
    """Copies time elements from date and time values.

    Args:
      date_time_values  (dict[str, int]): date and time values, such as year,
          month, day of month, hours, minutes, seconds, microseconds.
    """
    year = date_time_values.get('year', 0)
    month = date_time_values.get('month', 0)
    day_of_month = date_time_values.get('day_of_month', 0)
    hours = date_time_values.get('hours', 0)
    minutes = date_time_values.get('minutes', 0)
    seconds = date_time_values.get('seconds', 0)

    self._normalized_timestamp = None
    self._number_of_seconds = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds)
    self._time_elements_tuple = (
        year, month, day_of_month, hours, minutes, seconds)

    self.is_local_time = False

  def _CopyTimeFromStringISO8601(self, time_string):
    """Copies a time from an ISO 8601 date and time string.

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
      time_string = time_string[:-1]

    time_string_length = len(time_string)

    # The time string should at least contain 'hh'.
    if time_string_length < 2:
      raise ValueError('Time string too short.')

    try:
      hours = int(time_string[0:2], 10)
    except ValueError:
      raise ValueError('Unable to parse hours.')

    if hours not in range(0, 24):
      raise ValueError('Hours value: {0:d} out of bounds.'.format(hours))

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
      raise ValueError('Minutes value: {0:d} out of bounds.'.format(minutes))

    # TODO: support a leap second?
    if seconds is not None and seconds not in range(0, 60):
      raise ValueError('Seconds value: {0:d} out of bounds.'.format(seconds))

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

      # Note that when the sign of the time zone offset is negative
      # the difference needs to be added. We do so by flipping the sign.
      if time_string[time_zone_string_index] != '-':
        time_zone_offset = -time_zone_offset

    return hours, minutes, seconds, microseconds, time_zone_offset

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

  def CopyFromStringTuple(self, time_elements_tuple):
    """Copies time elements from string-based time elements tuple.

    Args:
      time_elements_tuple (Optional[tuple[str, str, str, str, str, str]]):
          time elements, contains year, month, day of month, hours, minutes and
          seconds.

    Raises:
      ValueError: if the time elements tuple is invalid.
    """
    if len(time_elements_tuple) < 6:
      raise ValueError((
          'Invalid time elements tuple at least 6 elements required,'
          'got: {0:d}').format(len(time_elements_tuple)))

    try:
      year = int(time_elements_tuple[0], 10)
    except (TypeError, ValueError):
      raise ValueError('Invalid year value: {0!s}'.format(
          time_elements_tuple[0]))

    try:
      month = int(time_elements_tuple[1], 10)
    except (TypeError, ValueError):
      raise ValueError('Invalid month value: {0!s}'.format(
          time_elements_tuple[1]))

    try:
      day_of_month = int(time_elements_tuple[2], 10)
    except (TypeError, ValueError):
      raise ValueError('Invalid day of month value: {0!s}'.format(
          time_elements_tuple[2]))

    try:
      hours = int(time_elements_tuple[3], 10)
    except (TypeError, ValueError):
      raise ValueError('Invalid hours value: {0!s}'.format(
          time_elements_tuple[3]))

    try:
      minutes = int(time_elements_tuple[4], 10)
    except (TypeError, ValueError):
      raise ValueError('Invalid minutes value: {0!s}'.format(
          time_elements_tuple[4]))

    try:
      seconds = int(time_elements_tuple[5], 10)
    except (TypeError, ValueError):
      raise ValueError('Invalid seconds value: {0!s}'.format(
          time_elements_tuple[5]))

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

    return '{0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}'.format(
        self._time_elements_tuple[0], self._time_elements_tuple[1],
        self._time_elements_tuple[2], self._time_elements_tuple[3],
        self._time_elements_tuple[4], self._time_elements_tuple[5])


class TimeElementsWithFractionOfSecond(TimeElements):
  """Time elements with a fraction of second interface.

  Attributes:
    fraction_of_second (decimal.Decimal): fraction of second, which must be a
        value between 0.0 and 1.0.
    is_local_time (bool): True if the date and time value is in local time.
  """

  def __init__(self, fraction_of_second=None, time_elements_tuple=None):
    """Initializes time elements.

    Args:
      fraction_of_second (Optional[decimal.Decimal]): fraction of second, which
          must be a value between 0.0 and 1.0.
      time_elements_tuple (Optional[tuple[int, int, int, int, int, int]]):
          time elements, contains year, month, day of month, hours, minutes and
          seconds.

    Raises:
      ValueError: if the time elements tuple is invalid or fraction of second
          value is out of bounds.
    """
    if fraction_of_second is not None:
      if fraction_of_second < 0.0 or fraction_of_second >= 1.0:
        raise ValueError(
            'Fraction of second value: {0:f} out of bounds.'.format(
                fraction_of_second))

    super(TimeElementsWithFractionOfSecond, self).__init__(
        time_elements_tuple=time_elements_tuple)
    self._precision = None
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

    return self._normalized_timestamp

  def _CopyFromDateTimeValues(self, date_time_values):
    """Copies time elements from date and time values.

    Args:
      date_time_values  (dict[str, int]): date and time values, such as year,
          month, day of month, hours, minutes, seconds, microseconds.

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

    precision_helper = precisions.PrecisionHelperFactory.CreatePrecisionHelper(
        self._precision)

    fraction_of_second = precision_helper.CopyMicrosecondsToFractionOfSecond(
        microseconds)

    self._normalized_timestamp = None
    self._number_of_seconds = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds)
    self._time_elements_tuple = (
        year, month, day_of_month, hours, minutes, seconds)
    self.fraction_of_second = fraction_of_second
    self.is_local_time = False

  def CopyFromStringTuple(self, time_elements_tuple):
    """Copies time elements from string-based time elements tuple.

    Args:
      time_elements_tuple (Optional[tuple[str, str, str, str, str, str, str]]):
          time elements, contains year, month, day of month, hours, minutes,
          seconds and fraction of seconds.

    Raises:
      ValueError: if the time elements tuple is invalid.
    """
    if len(time_elements_tuple) < 7:
      raise ValueError((
          'Invalid time elements tuple at least 7 elements required,'
          'got: {0:d}').format(len(time_elements_tuple)))

    super(TimeElementsWithFractionOfSecond, self).CopyFromStringTuple(
        time_elements_tuple)

    try:
      fraction_of_second = decimal.Decimal(time_elements_tuple[6])
    except (TypeError, ValueError):
      raise ValueError('Invalid fraction of second value: {0!s}'.format(
          time_elements_tuple[6]))

    if fraction_of_second < 0.0 or fraction_of_second >= 1.0:
      raise ValueError('Fraction of second value: {0:f} out of bounds.'.format(
          fraction_of_second))

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

  def __init__(self, time_elements_tuple=None):
    """Initializes time elements.

    Args:
      time_elements_tuple (Optional[tuple[int, int, int, int, int, int, int]]):
          time elements, contains year, month, day of month, hours, minutes,
          seconds and milliseconds.

    Raises:
      ValueError: if the time elements tuple is invalid.
    """
    fraction_of_second = None
    if time_elements_tuple:
      if len(time_elements_tuple) < 7:
        raise ValueError((
            'Invalid time elements tuple at least 7 elements required,'
            'got: {0:d}').format(len(time_elements_tuple)))

      milliseconds = time_elements_tuple[6]
      time_elements_tuple = time_elements_tuple[:6]

      if (milliseconds < 0 or
          milliseconds >= definitions.MILLISECONDS_PER_SECOND):
        raise ValueError('Invalid number of milliseconds.')

      fraction_of_second = (
          decimal.Decimal(milliseconds) / definitions.MILLISECONDS_PER_SECOND)

    super(TimeElementsInMilliseconds, self).__init__(
        fraction_of_second=fraction_of_second,
        time_elements_tuple=time_elements_tuple)
    self._precision = definitions.PRECISION_1_MILLISECOND

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
    if len(time_elements_tuple) < 7:
      raise ValueError((
          'Invalid time elements tuple at least 7 elements required,'
          'got: {0:d}').format(len(time_elements_tuple)))

    year, month, day_of_month, hours, minutes, seconds, milliseconds = (
        time_elements_tuple)

    try:
      milliseconds = int(milliseconds, 10)
    except (TypeError, ValueError):
      raise ValueError('Invalid millisecond value: {0!s}'.format(milliseconds))

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

  def __init__(self, time_elements_tuple=None):
    """Initializes time elements.

    Args:
      time_elements_tuple (Optional[tuple[int, int, int, int, int, int, int]]):
          time elements, contains year, month, day of month, hours, minutes,
          seconds and microseconds.

    Raises:
      ValueError: if the time elements tuple is invalid.
    """
    fraction_of_second = None
    if time_elements_tuple:
      if len(time_elements_tuple) < 7:
        raise ValueError((
            'Invalid time elements tuple at least 7 elements required,'
            'got: {0:d}').format(len(time_elements_tuple)))

      microseconds = time_elements_tuple[6]
      time_elements_tuple = time_elements_tuple[:6]

      if (microseconds < 0 or
          microseconds >= definitions.MICROSECONDS_PER_SECOND):
        raise ValueError('Invalid number of microseconds.')

      fraction_of_second = (
          decimal.Decimal(microseconds) / definitions.MICROSECONDS_PER_SECOND)

    super(TimeElementsInMicroseconds, self).__init__(
        fraction_of_second=fraction_of_second,
        time_elements_tuple=time_elements_tuple)
    self._precision = definitions.PRECISION_1_MICROSECOND

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
    if len(time_elements_tuple) < 7:
      raise ValueError((
          'Invalid time elements tuple at least 7 elements required,'
          'got: {0:d}').format(len(time_elements_tuple)))

    year, month, day_of_month, hours, minutes, seconds, microseconds = (
        time_elements_tuple)

    try:
      microseconds = int(microseconds, 10)
    except (TypeError, ValueError):
      raise ValueError('Invalid microsecond value: {0!s}'.format(microseconds))

    if microseconds < 0 or microseconds >= definitions.MICROSECONDS_PER_SECOND:
      raise ValueError('Invalid number of microseconds.')

    fraction_of_second = (
        decimal.Decimal(microseconds) / definitions.MICROSECONDS_PER_SECOND)

    time_elements_tuple = (
        year, month, day_of_month, hours, minutes, seconds,
        str(fraction_of_second))

    super(TimeElementsInMicroseconds, self).CopyFromStringTuple(
        time_elements_tuple)
