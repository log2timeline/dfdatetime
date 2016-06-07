# -*- coding: utf-8 -*-
"""Time elements implementation."""

import calendar

from dfdatetime import interface


class TimeElements(interface.DateTimeValues):
  """Class that implements time elements."""

  def __init__(self, time_elements_tuple):
    """Initializes a time elements object.

    Args:
      time_elements_tuple: a named tuple containg the time elements.
    """
    super(TimeElements, self).__init__()
    self._time_elements_tuple = time_elements_tuple
    self._timestamp = calendar.timegm(self._time_elements_tuple)

  def CopyToStatTimeTuple(self):
    """Copies the time elements to a stat timestamp tuple.

    Returns:
      A tuple of an integer containing a POSIX timestamp in seconds
      and an integer containing the remainder in 100 nano seconds or
      Currently the remainder will always be 0.
    """
    return self._timestamp, 0

  def GetPlasoTimestamp(self):
    """Retrieves a timestamp that is compatible with plaso.

    Returns:
      An integer containing a POSIX timestamp in microseconds or
      None on error.
    """
    return self._timestamp * 1000000
