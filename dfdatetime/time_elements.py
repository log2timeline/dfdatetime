# -*- coding: utf-8 -*-
"""Time elements implementation."""

from __future__ import unicode_literals

from dfdatetime import definitions
from dfdatetime import interface


class TimeElements(interface.DateTimeValues):
  """Time elements.

  Time elements contain separate values for year, month, day of month,
  hours, minutes and seconds.

  Attributes:
    is_local_time (bool): True if the date and time value is in local time.
    precision (str): precision of the date and time value, which should
        be one of the PRECISION_VALUES in definitions.
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
    self._time_elements_tuple = time_elements_tuple
    self.precision = definitions.PRECISION_1_SECOND

    if time_elements_tuple:
      if len(time_elements_tuple) < 6:
        raise ValueError('Invalid time elements tuple 6 elements required.')

      self._number_of_seconds = self._GetNumberOfSecondsFromElements(
          *time_elements_tuple)

  def _CopyDateTimeFromStringISO8601(self, time_string):
    """Copies a date and time from an ISO 8601 date and time string.

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
          fraction can be either 3 or 6 digits. The seconds fraction and
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
        time_fraction = float(time_fraction) / float(10 ** time_fraction_length)
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

      time_fraction *= 1000000
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

  def CopyFromString(self, time_string):
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
      raise ValueError('Invalid time elements tuple 6 elements required.')

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

    self._number_of_seconds = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds)
    self._time_elements_tuple = (
        year, month, day_of_month, hours, minutes, seconds)

  def CopyToStatTimeTuple(self):
    """Copies the time elements to a stat timestamp tuple.

    Returns:
      tuple[int, int]: a POSIX timestamp in seconds and the remainder in
          100 nano seconds or (None, None) on error.
    """
    if self._number_of_seconds is None:
      return None, None
    return self._number_of_seconds, None

  def CopyToDateTimeString(self):
    """Copies the time elements to a date and time string.

    Returns:
      str: date and time value formatted as:
          YYYY-MM-DD hh:mm:ss
    """
    if self._number_of_seconds is None:
      return

    return '{0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}'.format(
        self._time_elements_tuple[0], self._time_elements_tuple[1],
        self._time_elements_tuple[2], self._time_elements_tuple[3],
        self._time_elements_tuple[4], self._time_elements_tuple[5])

  def GetPlasoTimestamp(self):
    """Retrieves a timestamp that is compatible with plaso.

    Returns:
      int: a POSIX timestamp in microseconds or None on error.
    """
    if self._number_of_seconds is None:
      return
    return self._number_of_seconds * 1000000


class TimeElementsInMilliseconds(TimeElements):
  """Time elements in milliseconds.

  Attributes:
    is_local_time (bool): True if the date and time value is in local time.
    precision (str): precision of the date and time value, which should
        be one of the PRECISION_VALUES in definitions.
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
    milliseconds = None
    if time_elements_tuple:
      if len(time_elements_tuple) < 7:
        raise ValueError('Invalid time elements tuple 7 elements required.')

      milliseconds = time_elements_tuple[6]
      time_elements_tuple = time_elements_tuple[:6]

      if milliseconds < 0 or milliseconds > 999:
        raise ValueError('Invalid number of milliseconds.')

    super(TimeElementsInMilliseconds, self).__init__(
        time_elements_tuple=time_elements_tuple)
    self._milliseconds = milliseconds
    self.precision = definitions.PRECISION_1_MILLISECOND

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
    microseconds = date_time_values.get('microseconds', 0)
    milliseconds, _ = divmod(microseconds, 1000)

    self._number_of_seconds = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds)
    self._milliseconds = milliseconds
    self._time_elements_tuple = (
        year, month, day_of_month, hours, minutes, seconds, milliseconds)

    self.is_local_time = False

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
      raise ValueError('Invalid time elements tuple 7 elements required.')

    super(TimeElementsInMilliseconds, self).CopyFromStringTuple(
        time_elements_tuple)
    try:
      self._milliseconds = int(time_elements_tuple[6], 10)
    except (TypeError, ValueError):
      raise ValueError('Invalid milliseconds value: {0!s}'.format(
          time_elements_tuple[6]))

  def CopyToStatTimeTuple(self):
    """Copies the time elements to a stat timestamp tuple.

    Returns:
      tuple[int, int]: a POSIX timestamp in seconds and the remainder in
          100 nano seconds or (None, None) on error.
    """
    if self._number_of_seconds is None or self._milliseconds is None:
      return None, None

    return self._number_of_seconds, self._milliseconds * 10000

  def CopyToDateTimeString(self):
    """Copies the time elements to a date and time string.

    Returns:
      str: date and time value formatted as:
          YYYY-MM-DD hh:mm:ss.###
    """
    if self._number_of_seconds is None or self._milliseconds is None:
      return

    return '{0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}.{6:03d}'.format(
        self._time_elements_tuple[0], self._time_elements_tuple[1],
        self._time_elements_tuple[2], self._time_elements_tuple[3],
        self._time_elements_tuple[4], self._time_elements_tuple[5],
        self._milliseconds)

  def GetPlasoTimestamp(self):
    """Retrieves a timestamp that is compatible with plaso.

    Returns:
      int: a POSIX timestamp in microseconds or None on error.
    """
    if self._number_of_seconds is None or self._milliseconds is None:
      return

    return ((self._number_of_seconds * 1000) + self._milliseconds) * 1000


class TimeElementsInMicroseconds(TimeElements):
  """Time elements in microseconds.

  Attributes:
    is_local_time (bool): True if the date and time value is in local time.
    precision (str): precision of the date and time value, which should
        be one of the PRECISION_VALUES in definitions.
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
    microseconds = None
    if time_elements_tuple:
      if len(time_elements_tuple) < 7:
        raise ValueError('Invalid time elements tuple 7 elements required.')

      microseconds = time_elements_tuple[6]
      time_elements_tuple = time_elements_tuple[:6]

      if microseconds < 0 or microseconds > 999999:
        raise ValueError('Invalid number of microseconds.')

    super(TimeElementsInMicroseconds, self).__init__(
        time_elements_tuple=time_elements_tuple)
    self._microseconds = microseconds
    self.precision = definitions.PRECISION_1_MICROSECOND

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
    microseconds = date_time_values.get('microseconds', 0)

    self._number_of_seconds = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds)
    self._microseconds = microseconds
    self._time_elements_tuple = (
        year, month, day_of_month, hours, minutes, seconds, microseconds)

    self.is_local_time = False

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
      raise ValueError('Invalid time elements tuple 7 elements required.')

    super(TimeElementsInMicroseconds, self).CopyFromStringTuple(
        time_elements_tuple)
    try:
      self._microseconds = int(time_elements_tuple[6], 10)
    except (TypeError, ValueError):
      raise ValueError('Invalid microseconds value: {0!s}'.format(
          time_elements_tuple[6]))

  def CopyToStatTimeTuple(self):
    """Copies the time elements to a stat timestamp tuple.

    Returns:
      tuple[int, int]: a POSIX timestamp in seconds and the remainder in
          100 nano seconds or (None, None) on error.
    """
    if self._number_of_seconds is None or self._microseconds is None:
      return None, None

    return self._number_of_seconds, self._microseconds * 10

  def CopyToDateTimeString(self):
    """Copies the time elements to a date and time string.

    Returns:
      str: date and time value formatted as:
          YYYY-MM-DD hh:mm:ss.######
    """
    if self._number_of_seconds is None or self._microseconds is None:
      return

    return '{0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}.{6:06d}'.format(
        self._time_elements_tuple[0], self._time_elements_tuple[1],
        self._time_elements_tuple[2], self._time_elements_tuple[3],
        self._time_elements_tuple[4], self._time_elements_tuple[5],
        self._microseconds)

  def GetPlasoTimestamp(self):
    """Retrieves a timestamp that is compatible with plaso.

    Returns:
      int: a POSIX timestamp in microseconds or None on error.
    """
    if self._number_of_seconds is None or self._microseconds is None:
      return

    return (self._number_of_seconds * 1000000) + self._microseconds
