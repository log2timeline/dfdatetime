# -*- coding: utf-8 -*-
"""SYSTEMTIME structure implementation."""

from dfdatetime import definitions
from dfdatetime import interface


class Systemtime(interface.DateTimeValues):
  """Class that implements a SYSTEMTIME structure.

  The SYSTEMTIME structure is 16 bytes of size and contains:

  struct {
      WORD year,
      WORD month,
      WORD day_of_week,
      WORD day_of_month,
      WORD hour,
      WORD minute,
      WORD second,
      WORD millisecond
  }

  Attributes:
    year (int): year, 1601 through 30827.
    month (int): month of year, 1 through 12.
    day_of_week (int): day of week, 0 through 6.
    day_of_month (int): day of month, 1 through 31.
    hours (int): hours, 0 through 23.
    minutes (int): minutes, 0 through 59.
    seconds (int): seconds, 0 through 59.
    milliseconds (int): milliseconds, 0 through 999.
  """

  def __init__(self, system_time_tuple=None):
    """Initializes a SYSTEMTIME structure.

    Args:
      system_time_tuple
          (Optional[tuple[int, int, int, int, int, int, int, int]]):
          system time, contains year, month, day of week, day of month,
          hours, minutes, seconds and milliseconds.

    Raises:
      ValueError: if the system time is invalid.
    """
    super(Systemtime, self).__init__()
    self._number_of_seconds = None
    self.day_of_month = None
    self.day_of_week = None
    self.hours = None
    self.milliseconds = None
    self.minutes = None
    self.month = None
    self.precision = definitions.PRECISION_1_MILLISECOND
    self.seconds = None
    self.year = None

    if system_time_tuple:
      if len(system_time_tuple) < 8:
        raise ValueError(u'Invalid system time tuple 8 elements required.')

      if system_time_tuple[0] < 1601 or system_time_tuple[0] > 30827:
        raise ValueError(u'Year value out of bounds.')

      if system_time_tuple[1] not in range(1, 13):
        raise ValueError(u'Month value out of bounds.')

      if system_time_tuple[2] not in range(0, 7):
        raise ValueError(u'Day of week value out of bounds.')

      days_per_month = self._GetDaysPerMonth(
          system_time_tuple[0], system_time_tuple[1])
      if system_time_tuple[3] < 1 or system_time_tuple[3] > days_per_month:
        raise ValueError(u'Day of month value out of bounds.')

      if system_time_tuple[4] not in range(0, 24):
        raise ValueError(u'Hours value out of bounds.')

      if system_time_tuple[5] not in range(0, 60):
        raise ValueError(u'Minutes value out of bounds.')

      # TODO: support a leap second?
      if system_time_tuple[6] not in range(0, 60):
        raise ValueError(u'Seconds value out of bounds.')

      if system_time_tuple[7] < 0 or system_time_tuple[7] > 999:
        raise ValueError(u'Milliseconds value out of bounds.')

      self.day_of_month = system_time_tuple[3]
      self.day_of_week = system_time_tuple[2]
      self.hours = system_time_tuple[4]
      self.milliseconds = system_time_tuple[7]
      self.minutes = system_time_tuple[5]
      self.month = system_time_tuple[1]
      self.seconds = system_time_tuple[6]
      self.year = system_time_tuple[0]

      self._number_of_seconds = self._GetNumberOfSecondsFromElements(
          self.year, self.month, self.day_of_month, self.hours, self.minutes,
          self.seconds)

  def CopyFromString(self, time_string):
    """Copies a SYSTEMTIME from a string containing a date and time value.

    Args:
      time_string (str): date and time value formatted as:
          YYYY-MM-DD hh:mm:ss.######[+-]##:##

          Where # are numeric digits ranging from 0 to 9 and the seconds
          fraction can be either 3 or 6 digits. The time of day, seconds
          fraction and time zone offset are optional. The default time zone
          is UTC.

    Raises:
      ValueError: if the date string is invalid or not supported.
    """
    date_time_values = self._CopyDateTimeFromString(time_string)

    year = date_time_values.get(u'year', 0)
    month = date_time_values.get(u'month', 0)
    day_of_month = date_time_values.get(u'day_of_month', 0)
    hours = date_time_values.get(u'hours', 0)
    minutes = date_time_values.get(u'minutes', 0)
    seconds = date_time_values.get(u'seconds', 0)

    microseconds = date_time_values.get(u'microseconds', 0)
    milliseconds, _ = divmod(microseconds, 1000)

    if year < 1601 or year > 30827:
      raise ValueError(u'Unsupported year value: {0:d}.'.format(year))

    self._number_of_seconds = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds)

    self.year = year
    self.month = month
    self.day_of_month = day_of_month
    # TODO: calculate day of week on demand.
    self.day_of_week = None
    self.hours = hours
    self.minutes = minutes
    self.seconds = seconds
    self.milliseconds = milliseconds

    self.is_local_time = False

  def CopyToStatTimeTuple(self):
    """Copies the SYSTEMTIME structure to a stat timestamp tuple.

    Returns:
      tuple[int, int]: a POSIX timestamp in seconds and the remainder in
          100 nano seconds or (None, None) on error.
    """
    if self._number_of_seconds is None:
      return None, None

    return self._number_of_seconds, self.milliseconds * 10000

  def GetPlasoTimestamp(self):
    """Retrieves a timestamp that is compatible with plaso.

    Returns:
      int: a POSIX timestamp in microseconds or None on error.
    """
    if self._number_of_seconds is None:
      return

    return ((self._number_of_seconds * 1000) + self.milliseconds) * 1000
