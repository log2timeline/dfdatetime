# -*- coding: utf-8 -*-
"""POSIX timestamp implementation."""

from dfdatetime import interface


class PosixTime(interface.DateTimeValues):
  """Class that implements a POSIX timestamp.

  The POSIX timestamp is a signed integer that contains the number of
  seconds since 1970-01-01 00:00:00 (also known as the POSIX epoch).
  Negative values represent date and times predating the POSIX epoch.

  The POSIX timestamp was initially 32-bit though 64-bit variants
  are known to be used.

  Attributes:
    timestamp (int): POSIX timestamp.
    micro_seconds (int): number of microseconds
  """

  def __init__(self, timestamp, micro_seconds=0):
    """Initializes the POSIX timestamp object.

    Args:
      timestamp (int): POSIX timestamp.
      micro_seconds (Optional[int]): number of microseconds.
    """
    super(PosixTime, self).__init__()
    self.micro_seconds = micro_seconds
    self.timestamp = timestamp

  def CopyFromString(self, time_string):
    """Copies a POSIX timestamp from a string containing a date and time value.

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

    # TODO: implement
    raise NotImplementedError()

  def CopyToStatTimeTuple(self):
    """Copies the POSIX timestamp to a stat timestamp tuple.

    Returns:
      tuple[int, int]: a POSIX timestamp in seconds and the remainder in
          100 nano seconds or (None, None) on error.
    """
    return self.timestamp, self.micro_seconds * 10

  def GetPlasoTimestamp(self):
    """Retrieves a timestamp that is compatible with plaso.

    Returns:
      int: a POSIX timestamp in microseconds or None on error.
    """
    return (self.timestamp * 1000000) + self.micro_seconds
