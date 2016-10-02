# -*- coding: utf-8 -*-
"""Semantic time implementation."""

from dfdatetime import interface


class SemanticTime(interface.DateTimeValues):
  """Class that implements semantic time.

  Semantic time is term to describe date and time values that have specific
  meaning such as: "Never", "Yesterday", "Not set".

  Attributes:
    is_local_time (bool): True if the date and time value is in local time.
    precision (str): precision of the date and time value, which should
        be one of the PRECISION_VALUES in definitions.
    string (str): semantic representation of the time, such as:
        "Never", "Not set".
  """

  def __init__(self, string=None):
    """Initializes a semantic time.

    Args:
      string (str): semantic representation of the time, such as:
          "Never", "Not set".
    """
    super(SemanticTime, self).__init__()
    self.string = string

  def CopyFromString(self, time_string):
    """Copies semantic time from a string containing a date and time value.

    Args:
      time_string (str): semantic representation of the time, such as:
          "Never", "Not set".

    Raises:
      ValueError: because semantic time cannot be copied from a string.
    """
    self.string = time_string

  def CopyToStatTimeTuple(self):
    """Copies the semantic timestamp to a stat timestamp tuple.

    Returns:
      tuple[int, int]: a POSIX timestamp in seconds and the remainder in
          100 nano seconds, which will always be 0, 0.
    """
    return 0, 0

  def GetPlasoTimestamp(self):
    """Retrieves a timestamp that is compatible with plaso.

    Returns:
      int: a POSIX timestamp in microseconds, which will always be 0.
    """
    return 0
