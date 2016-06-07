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
    timestamp: an integer containing the POSIX timestamp.
    micro_seconds: an integer containing the number of microseconds
  """

  def __init__(self, timestamp, micro_seconds=0):
    """Initializes the POSIX timestamp object.

    Args:
      timestamp: an integer containing the POSIX timestamp.
      micro_seconds: optional integer containing the number of microseconds.
    """
    super(PosixTime, self).__init__()
    self.micro_seconds = micro_seconds
    self.timestamp = timestamp

  def CopyToStatTimeTuple(self):
    """Copies the POSIX timestamp to a stat timestamp tuple.

    Returns:
      A tuple of an integer containing a POSIX timestamp in seconds
      and an integer containing the remainder in 100 nano seconds or
      None on error.
    """
    return self.timestamp, self.micro_seconds * 10

  def GetPlasoTimestamp(self):
    """Retrieves a timestamp that is compatible with plaso.

    Returns:
      An integer containing a POSIX timestamp in microseconds or
      None on error.
    """
    return (self.timestamp * 1000000) + self.micro_seconds
