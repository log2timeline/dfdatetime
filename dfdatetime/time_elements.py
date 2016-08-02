# -*- coding: utf-8 -*-
"""Time elements implementation."""

import calendar

from dfdatetime import definitions
from dfdatetime import interface


class TimeElements(interface.DateTimeValues):
  """Class that implements time elements."""

  def __init__(self, time_elements_tuple=None):
    """Initializes a time elements object.

    Args:
      time_elements_tuple (Optional[tuple[int, int, int, int, int, int]]):
          time elements, contains year, month, day of month, hours, minutes and
          seconds
    """
    super(TimeElements, self).__init__()
    self._time_elements_tuple = time_elements_tuple
    if time_elements_tuple is None:
      self._timestamp = None
    else:
      self._timestamp = calendar.timegm(self._time_elements_tuple)
      self._timestamp = int(self._timestamp)
    self.precision = definitions.PRECISION_1_SECOND

  def CopyFromString(self, time_string):
    """Copies time elements from a string containing a date and time value.

    Args:
      time_string (str): date and time value formatted as:
          YYYY-MM-DD hh:mm:ss.######[+-]##:##

          Where # are numeric digits ranging from 0 to 9 and the seconds
          fraction can be either 3 or 6 digits. The time of day, seconds
          fraction and time zone offset are optional. The default time zone
          is UTC.
    """
    date_time_values = self._CopyDateTimeFromString(time_string)

    year = date_time_values.get(u'year', 0)
    month = date_time_values.get(u'month', 0)
    day_of_month = date_time_values.get(u'day_of_month', 0)
    hours = date_time_values.get(u'hours', 0)
    minutes = date_time_values.get(u'minutes', 0)
    seconds = date_time_values.get(u'seconds', 0)

    self._time_elements_tuple = (
        year, month, day_of_month, hours, minutes, seconds)
    self._timestamp = calendar.timegm(self._time_elements_tuple)
    self._timestamp = int(self._timestamp)

    self.time_zone = u'UTC'

  def CopyToStatTimeTuple(self):
    """Copies the time elements to a stat timestamp tuple.

    Returns:
      tuple[int, int]: a POSIX timestamp in seconds and the remainder in
          100 nano seconds or (None, None) on error.
    """
    if self._timestamp is None:
      return None, None
    return self._timestamp, None

  def GetPlasoTimestamp(self):
    """Retrieves a timestamp that is compatible with plaso.

    Returns:
      int: a POSIX timestamp in microseconds or None on error.
    """
    if self._timestamp is None:
      return
    return self._timestamp * 1000000
