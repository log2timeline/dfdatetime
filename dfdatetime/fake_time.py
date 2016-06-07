# -*- coding: utf-8 -*-
"""Fake timestamp implementation."""

import calendar
import time

from dfdatetime import interface


class FakeTime(interface.DateTimeValues):
  """Class that implements a fake timestamp."""

  def __init__(self):
    """Initializes the fake timestamp object."""
    super(FakeTime, self).__init__()
    self._time_elements = time.gmtime()
    self._timestamp = calendar.timegm(self._time_elements)

  def CopyToStatTimeTuple(self):
    """Copies the fake timestamp to a stat timestamp tuple.

    Returns:
      A tuple of an integer containing a POSIX timestamp in seconds
      and an integer containing the remainder in 100 nano seconds.
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
