# -*- coding: utf-8 -*-
"""Time elements implementation."""

import calendar

from dfdatetime import interface


class TimeElements(interface.DateTimeValues):
  """Class that implements time elements."""

  def __init__(self, time_elements_tuple):
    """Initializes a time elements object.

    Args:
      time_elements_tuple (tuple): time elements.
    """
    super(TimeElements, self).__init__()
    self._time_elements_tuple = time_elements_tuple
    self._timestamp = calendar.timegm(self._time_elements_tuple)

  def CopyFromString(self, time_string):
    """Copies time elements from a string containing a date and time value.

    Args:
      time_string (str): date and time value formatted as:
          YYYY-MM-DD hh:mm:ss.######[+-]##:##

          Where # are numeric digits ranging from 0 to 9 and the seconds
          fraction can be either 3 or 6 digits. The time of day, seconds
          fraction and timezone offset are optional. The default timezone
          is UTC.

    Raises:
      ValueError: if the time string is invalid or not supported.
    """
    if not time_string:
      raise ValueError(u'Invalid time string.')

    # TODO: implement.
    raise NotImplementedError()

  def CopyToStatTimeTuple(self):
    """Copies the time elements to a stat timestamp tuple.

    Returns:
      tuple[int, int]: a POSIX timestamp in seconds and the remainder in
          100 nano seconds or (None, None) on error.
    """
    return self._timestamp, 0

  def GetPlasoTimestamp(self):
    """Retrieves a timestamp that is compatible with plaso.

    Returns:
      int: a POSIX timestamp in microseconds or None on error.
    """
    return self._timestamp * 1000000
