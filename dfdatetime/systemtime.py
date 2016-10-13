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
      WORD day,
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

  def __init__(
      self, day_of_month=0, day_of_week=0, hours=0, milliseconds=0,
      minutes=0, month=0, seconds=0, year=0):
    """Initializes a SYSTEMTIME structure.

    Args:
      day_of_month (Optional[int]): day of month, 1 through 31.
      day_of_week (Optional[int]): day of week, 0 through 6.
      hours (Optional[int]): hours, 0 through 23.
      milliseconds (Optional[int]): milliseconds, 0 through 999.
      minutes (Optional[int]): minutes, 0 through 59.
      month (Optional[int]): month of year, 1 through 12.
      seconds (Optional[int]): seconds, 0 through 59.
      year (Optional[int]): year, 1601 through 30827.
    """
    super(Systemtime, self).__init__()
    self._number_of_seconds = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds)
    self.day_of_month = day_of_month
    self.day_of_week = day_of_week
    self.hours = hours
    self.milliseconds = milliseconds
    self.minutes = minutes
    self.month = month
    self.precision = definitions.PRECISION_1_MILLISECOND
    self.seconds = seconds
    self.year = year

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

    return self._number_of_seconds, self.milliseconds * 1000

  def GetPlasoTimestamp(self):
    """Retrieves a timestamp that is compatible with plaso.

    Returns:
      int: a POSIX timestamp in microseconds or None on error.
    """
    if self._number_of_seconds is None:
      return

    return ((self._number_of_seconds * 1000) + self.milliseconds) * 1000
