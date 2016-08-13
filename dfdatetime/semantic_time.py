# -*- coding: utf-8 -*-
"""Semantic time implementation."""

from dfdatetime import interface


class SemanticTime(interface.DateTimeValues):
  """Class that implements semantic time.

  Attributes:
    string (str): semantic representation of the time, such as:
        "Never", "Not set".
  """

  def __init__(self):
    """Initializes a semantic time."""
    super(SemanticTime, self).__init__()
    self.string = None

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
