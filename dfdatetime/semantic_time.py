# -*- coding: utf-8 -*-
"""Semantic time implementation."""

from __future__ import unicode_literals

from dfdatetime import interface


class SemanticTime(interface.DateTimeValues):
  """Semantic time.

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
    self._sort_order = 50
    self.string = string

  def __eq__(self, other):
    """Determines if the date time values are equal to other.

    Args:
      other (DateTimeValues): date time values to compare against.

    Returns:
      bool: True if the date time values are equal to other.
    """
    if isinstance(other, SemanticTime):
      other_sort_order = getattr(other, '_sort_order', None)
      return self._sort_order == other_sort_order

    return super(SemanticTime, self).__eq__(other)

  def __ge__(self, other):
    """Determines if the date time values are greater equal than other.

    Args:
      other (DateTimeValues): date time values to compare against.

    Returns:
      bool: True if the date time values are greater equal than other.
    """
    if isinstance(other, SemanticTime):
      other_sort_order = getattr(other, '_sort_order', None)
      return self._sort_order >= other_sort_order

    return super(SemanticTime, self).__eq__(other)

  def __gt__(self, other):
    """Determines if the date time values are greater than other.

    Args:
      other (DateTimeValues): date time values to compare against.

    Returns:
      bool: True if the date time values are greater than other.
    """
    if isinstance(other, SemanticTime):
      other_sort_order = getattr(other, '_sort_order', None)
      return self._sort_order > other_sort_order

    return super(SemanticTime, self).__eq__(other)

  def __le__(self, other):
    """Determines if the date time values are less equal than other.

    Args:
      other (DateTimeValues): date time values to compare against.

    Returns:
      bool: True if the date time values are less equal than other.
    """
    if isinstance(other, SemanticTime):
      other_sort_order = getattr(other, '_sort_order', None)
      return self._sort_order <= other_sort_order

    return super(SemanticTime, self).__eq__(other)

  def __lt__(self, other):
    """Determines if the date time values are less than other.

    Args:
      other (DateTimeValues): date time values to compare against.

    Returns:
      bool: True if the date time values are less than other.
    """
    if isinstance(other, SemanticTime):
      other_sort_order = getattr(other, '_sort_order', None)
      return self._sort_order < other_sort_order

    return super(SemanticTime, self).__eq__(other)

  def __ne__(self, other):
    """Determines if the date time values are not equal to other.

    Args:
      other (DateTimeValues): date time values to compare against.

    Returns:
      bool: True if the date time values are not equal to other.
    """
    if isinstance(other, SemanticTime):
      other_sort_order = getattr(other, '_sort_order', None)
      return self._sort_order != other_sort_order

    return super(SemanticTime, self).__eq__(other)

  def _GetNormalizedTimestamp(self):
    """Retrieves the normalized timestamp.

    Returns:
      float: normalized timestamp, which contains the number of seconds since
          January 1, 1970.
    """
    return None

  def CopyFromDateTimeString(self, time_string):
    """Copies semantic time from a date and time string.

    Args:
      time_string (str): semantic representation of the time, such as:
          "Never", "Not set".

    Raises:
      ValueError: because semantic time cannot be copied from a string.
    """
    self.string = time_string

  def CopyToDateTimeString(self):
    """Copies the date time value to a date and time string.

    Returns:
      str: semantic representation of the time, such as: "Never", "Not set".
    """
    return self.string

  def CopyToStatTimeTuple(self):
    """Copies the semantic timestamp to a stat timestamp tuple.

    Returns:
      tuple[int, int]: a POSIX timestamp in seconds and the remainder in
          100 nano seconds, which will always be None, None.
    """
    return None, None

  def GetDate(self):
    """Retrieves the date represented by the date and time values.

    Returns:
       tuple[int, int, int]: year, month, day of month or (None, None, None)
           if the date and time values do not represent a date.
    """
    return None, None, None

  def GetPlasoTimestamp(self):
    """Retrieves a timestamp that is compatible with plaso.

    Returns:
      int: a POSIX timestamp in microseconds, which will always be 0.
    """
    return 0


class InvalidTime(SemanticTime):
  """Semantic time that represents invalid."""

  def __init__(self):
    """Initializes a semantic time that represents invalid."""
    super(InvalidTime, self).__init__(string='Invalid')
    self._sort_order = 1


class Never(SemanticTime):
  """Semantic time that represents never."""

  def __init__(self):
    """Initializes a semantic time that represents never."""
    super(Never, self).__init__(string='Never')
    self._sort_order = 99


class NotSet(SemanticTime):
  """Semantic time that represents not set."""

  def __init__(self):
    """Initializes a semantic time that represents not set."""
    super(NotSet, self).__init__(string='Not set')
    self._sort_order = 2
