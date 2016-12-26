# -*- coding: utf-8 -*-
"""Date and time values interface."""

import abc
import calendar


class DateTimeValues(object):
  """Defines the date time values interface.

  This is the super class of different date and time representations.

  Attributes:
    is_local_time (bool): True if the date and time value is in local time.
    precision (str): precision of the date and time value, which should
        be one of the PRECISION_VALUES in definitions.
  """

  _DAYS_PER_MONTH = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

  # The number of seconds in a day
  _SECONDS_PER_DAY = 24 * 60 * 60

  def __init__(self):
    """Initializes date time values."""
    super(DateTimeValues, self).__init__()
    self.is_local_time = False
    self.precision = None

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
      raise ValueError(u'Date string too short.')

    if date_string[4] != u'-' or date_string[7] != u'-':
      raise ValueError(u'Invalid date string.')

    try:
      year = int(date_string[0:4], 10)
    except ValueError:
      raise ValueError(u'Unable to parse year.')

    try:
      month = int(date_string[5:7], 10)
    except ValueError:
      raise ValueError(u'Unable to parse month.')

    try:
      day_of_month = int(date_string[8:10], 10)
    except ValueError:
      raise ValueError(u'Unable to parse day of month.')

    days_per_month = self._GetDaysPerMonth(year, month)
    if day_of_month < 1 or day_of_month > days_per_month:
      raise ValueError(u'Day of month value out of bounds.')

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
          hours, minutes, seconds, microseconds.

    Raises:
      ValueError: if the time string is invalid or not supported.
    """
    if not time_string:
      raise ValueError(u'Invalid time string.')

    time_string_length = len(time_string)

    year, month, day_of_month = self._CopyDateFromString(time_string)

    if time_string_length <= 10:
      return {
          u'year': year,
          u'month': month,
          u'day_of_month': day_of_month}

    # If a time of day is specified the time string it should at least
    # contain 'YYYY-MM-DD hh:mm:ss'.
    if time_string[10] != u' ':
      raise ValueError(
          u'Invalid time string - space missing as date and time separator.')

    hours, minutes, seconds, microseconds, time_zone_offset = (
        self._CopyTimeFromString(time_string[11:]))

    if time_zone_offset:
      time_zone_hours, time_zone_minutes = divmod(time_zone_offset, 60)

      minutes += time_zone_minutes

      # Since divmod makes sure the sign of time_zone_minutes is positive
      # we only need to check the upper bound here, because time_zone_hours
      # remains signed it is corrected accordingly.
      if minutes >= 60:
        minutes -= 60
        hours += 1

      hours += time_zone_hours
      if hours < 0:
        hours += 24
        day_of_month -= 1

      elif hours >= 24:
        hours -= 24
        day_of_month += 1

      days_per_month = self._GetDaysPerMonth(year, month)
      if day_of_month < 1:
        month -= 1
        if month < 1:
          month = 12
          year -= 1

        day_of_month += self._GetDaysPerMonth(year, month)

      elif day_of_month > days_per_month:
        month += 1
        if month > 12:
          month = 1
          year += 1

        day_of_month -= days_per_month

    date_time_values = {
        u'year': year,
        u'month': month,
        u'day_of_month': day_of_month,
        u'hours': hours,
        u'minutes': minutes,
        u'seconds': seconds}

    if microseconds is not None:
      date_time_values[u'microseconds'] = microseconds
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

    if time_string_length < 8:
      raise ValueError(u'Time string too short.')

    # The time string should at least contain 'hh:mm:ss'.
    if time_string[2] != u':' or time_string[5] != u':':
      raise ValueError(u'Invalid time string.')

    try:
      hours = int(time_string[0:2], 10)
    except ValueError:
      raise ValueError(u'Unable to parse hours.')

    if hours not in range(0, 24):
      raise ValueError(u'Hours value out of bounds.')

    try:
      minutes = int(time_string[3:5], 10)
    except ValueError:
      raise ValueError(u'Unable to parse minutes.')

    if minutes not in range(0, 60):
      raise ValueError(u'Minutes value out of bounds.')

    try:
      seconds = int(time_string[6:8], 10)
    except ValueError:
      raise ValueError(u'Unable to parse day of seconds.')

    if seconds not in range(0, 60):
      raise ValueError(u'Seconds value out of bounds.')

    microseconds = None
    time_zone_offset = None

    if time_string_length > 8:
      if time_string[8] != u'.':
        time_zone_string_index = 8
      else:
        for time_zone_string_index in range(8, time_string_length):
          if time_string[time_zone_string_index] in (u'+', u'-'):
            break

          # The calculations that follow rely on the time zone string index
          # to point beyond the string in case no time zone offset was defined.
          if time_zone_string_index == time_string_length - 1:
            time_zone_string_index += 1

      if time_zone_string_index > 8:
        fraction_of_seconds_length = time_zone_string_index - 9
        if fraction_of_seconds_length not in (3, 6):
          raise ValueError(u'Invalid time string.')

        try:
          microseconds = int(time_string[9:time_zone_string_index], 10)
        except ValueError:
          raise ValueError(u'Unable to parse fraction of seconds.')

        if fraction_of_seconds_length == 3:
          microseconds *= 1000

      if time_zone_string_index < time_string_length:
        if (time_string_length - time_zone_string_index != 6 or
            time_string[time_zone_string_index + 3] != u':'):
          raise ValueError(u'Invalid time string.')

        try:
          time_zone_offset = int(time_string[
              time_zone_string_index + 1:time_zone_string_index + 3])
        except ValueError:
          raise ValueError(u'Unable to parse time zone hours offset.')

        if time_zone_offset not in range(0, 24):
          raise ValueError(u'Timezone hours offset value out of bounds.')

        time_zone_offset *= 60

        try:
          time_zone_offset += int(time_string[
              time_zone_string_index + 4:time_zone_string_index + 6])
        except ValueError:
          raise ValueError(u'Unable to parse time zone minutes offset.')

        # Note that when the sign of the time zone offset is negative
        # the difference needs to be added. We do so by flipping the sign.
        if time_string[time_zone_string_index] != u'-':
          time_zone_offset *= -1

    return hours, minutes, seconds, microseconds, time_zone_offset

  def _GetDayOfYear(self, year, month, day_of_month):
    """Retrieves the day of the year for a specific day of a month in a year.

    Args:
      year (int): year e.g. 1970.
      month (int): month where 1 represents January.
      day_of_month (int): day of the month where 1 represents the first day.

    Returns:
      int: day of year.

    Raises:
      ValueError: if the month or day of month value is out of bounds.
    """
    if month not in range(1, 13):
      raise ValueError(u'Month value out of bounds.')

    days_per_month = self._GetDaysPerMonth(year, month)
    if day_of_month < 1 or day_of_month > days_per_month:
      raise ValueError(u'Day of month value out of bounds.')

    day_of_year = day_of_month
    for past_month in range(1, month):
      day_of_year += self._GetDaysPerMonth(year, past_month)

    return day_of_year

  def _GetDaysPerMonth(self, year, month):
    """Retrieves the number of days in a month of a specific year.

    Args:
      year (int): year e.g. 1970.
      month (int): month ranging from 1 to 12.

    Returns:
      int: number of days in the month.

    Raises:
      ValueError: if the month value is out of bounds.
    """
    if month not in range(1, 13):
      raise ValueError(u'Month value out of bounds.')

    days_per_month = self._DAYS_PER_MONTH[month - 1]
    if month == 2 and self._IsLeapYear(year):
      days_per_month += 1

    return days_per_month

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
      self, year, month, day, hours, minutes, seconds):
    """Retrieves the number of seconds from the date and time elements.

    Args:
      year (int): year e.g. 1970.
      month (int): month of year.
      day(int): day of month.
      hours (int): hours.
      minutes (int): minutes.
      seconds (int): seconds.

    Returns:
      int: number of seconds since January 1, 1970 00:00:00 or None.
    """
    if not year or not month or not day:
      return

    # calendar.timegm requires the time tuple to contain at least
    # 6 integer values.
    time_elements_tuple = (
        year, month, day, hours or 0, minutes or 0, seconds or 0)

    try:
      number_of_seconds = calendar.timegm(time_elements_tuple)
    except ValueError:
      return

    return int(number_of_seconds)

  def _IsLeapYear(self, year):
    """Determines if a year is a leap year.

    Args:
      year (int): year e.g. 1970.

    Returns:
      bool: True if the year is a leap year.
    """
    return (year % 4 == 0 and year % 100 != 0) or year % 400 == 0

  @abc.abstractmethod
  def CopyFromString(self, time_string):
    """Copies a date time value from a string containing a date and time value.

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

  def CopyToStatTimeTuple(self):
    """Copies the date time value to a stat timestamp tuple.

    Returns:
      tuple[int, int]: a POSIX timestamp in seconds and the remainder in
          100 nano seconds or (None, None) on error.
    """

  # TODO: remove this method when there is no more need for it in plaso.
  @abc.abstractmethod
  def GetPlasoTimestamp(self):
    """Retrieves a timestamp that is compatible with plaso.

    Returns:
      int: a POSIX timestamp in microseconds or None on error.
    """
