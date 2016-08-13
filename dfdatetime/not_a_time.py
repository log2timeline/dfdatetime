# -*- coding: utf-8 -*-
"""Not a time implementation."""

from dfdatetime import interface


class NotATime(interface.DateTimeValues):
  """Class that implements not a time."""

  def CopyFromString(self, time_string):
    """Copies not at time from a string containing a date and time value.

    Args:
      time_string (str): date and time value formatted as:
          YYYY-MM-DD hh:mm:ss.######[+-]##:##

          Where # are numeric digits ranging from 0 to 9 and the seconds
          fraction can be either 3 or 6 digits. The time of day, seconds
          fraction and time zone offset are optional. The default time zone
          is UTC.

    Raises:
      ValueError: because not a time cannot be copied from a string.
    """
    raise ValueError(u'Cannot copy not a time from a time string.')

  def CopyToStatTimeTuple(self):
    """Copies the fake timestamp to a stat timestamp tuple.

    Returns:
      tuple[int, int]: a POSIX timestamp in seconds and the remainder in
          100 nano seconds.
    """
    return 0, 0

  def GetPlasoTimestamp(self):
    """Retrieves a timestamp that is compatible with plaso.

    Returns:
      int: a POSIX timestamp in microseconds.
    """
    return 0
