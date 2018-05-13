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
  """

  _SORT_ORDER = 50

  def __init__(self, string=None):
    """Initializes a semantic time.

    Args:
      string (str): semantic representation of the time, such as:
          "Never", "Not set".
    """
    super(SemanticTime, self).__init__()
    self._string = string

  @property
  def string(self):
    """str: semantic representation of the time, such as: "Never"."""
    return self._string

  def __eq__(self, other):
    """Determines if the date time values are equal to other.

    Args:
      other (DateTimeValues): date time values to compare against.

    Returns:
      bool: True if the date time values are equal to other.
    """
    if not isinstance(other, SemanticTime):
      return False

    return self._SORT_ORDER == other._SORT_ORDER  # pylint: disable=protected-access

  def __ge__(self, other):
    """Determines if the date time values are greater than or equal to other.

    Args:
      other (DateTimeValues): date time values to compare against.

    Returns:
      bool: True if the date time values are greater than or equal to other.

    Raises:
      ValueError: if other is not an instance of DateTimeValues.
    """
    if not isinstance(other, interface.DateTimeValues):
      raise ValueError('Other not an instance of DateTimeValues')

    if not isinstance(other, SemanticTime):
      return False

    return self._SORT_ORDER >= other._SORT_ORDER  # pylint: disable=protected-access

  def __gt__(self, other):
    """Determines if the date time values are greater than other.

    Args:
      other (DateTimeValues): date time values to compare against.

    Returns:
      bool: True if the date time values are greater than other.

    Raises:
      ValueError: if other is not an instance of DateTimeValues.
    """
    if not isinstance(other, interface.DateTimeValues):
      raise ValueError('Other not an instance of DateTimeValues')

    if not isinstance(other, SemanticTime):
      return False

    return self._SORT_ORDER > other._SORT_ORDER  # pylint: disable=protected-access

  def __le__(self, other):
    """Determines if the date time values are greater than or equal to other.

    Args:
      other (DateTimeValues): date time values to compare against.

    Returns:
      bool: True if the date time values are greater than or equal to other.

    Raises:
      ValueError: if other is not an instance of DateTimeValues.
    """
    if not isinstance(other, interface.DateTimeValues):
      raise ValueError('Other not an instance of DateTimeValues')

    if not isinstance(other, SemanticTime):
      return True

    return self._SORT_ORDER <= other._SORT_ORDER  # pylint: disable=protected-access

  def __lt__(self, other):
    """Determines if the date time values are less than other.

    Args:
      other (DateTimeValues): date time values to compare against.

    Returns:
      bool: True if the date time values are less than other.

    Raises:
      ValueError: if other is not an instance of DateTimeValues.
    """
    if not isinstance(other, interface.DateTimeValues):
      raise ValueError('Other not an instance of DateTimeValues')

    if not isinstance(other, SemanticTime):
      return True

    return self._SORT_ORDER < other._SORT_ORDER  # pylint: disable=protected-access

  def __ne__(self, other):
    """Determines if the date time values are not equal to other.

    Args:
      other (DateTimeValues): date time values to compare against.

    Returns:
      bool: True if the date time values are not equal to other.
    """
    if not isinstance(other, SemanticTime):
      return True

    return self._SORT_ORDER != other._SORT_ORDER  # pylint: disable=protected-access

  def _GetNormalizedTimestamp(self):
    """Retrieves the normalized timestamp.

    Returns:
      decimal.Decimal: normalized timestamp, which contains the number of
          seconds since January 1, 1970 00:00:00 and a fraction of second used
          for increased precision, or None if the normalized timestamp cannot be
          determined.
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
    self._string = time_string

  def CopyToDateTimeString(self):
    """Copies the date time value to a date and time string.

    Returns:
      str: semantic representation of the time, such as: "Never", "Not set".
    """
    return self._string

  def CopyToDateTimeStringISO8601(self):
    """Copies the date time value to an ISO 8601 date and time string.

    Returns:
      str: date and time value formatted as an ISO 8601 date and time string,
          which always be None since semantic time cannot be represented in
          ISO 8601.
    """
    return None

  def CopyToStatTimeTuple(self):
    """Copies the semantic timestamp to a stat timestamp tuple.

    Returns:
      tuple[int, int]: a POSIX timestamp in seconds and the remainder in
          100 nano seconds, which will always be None, None.
    """
    return None, None

  def GetPlasoTimestamp(self):
    """Retrieves a timestamp that is compatible with plaso.

    Returns:
      int: a POSIX timestamp in microseconds, which will always be 0.
    """
    return 0


class InvalidTime(SemanticTime):
  """Semantic time that represents invalid."""

  _SORT_ORDER = 1

  def __init__(self):
    """Initializes a semantic time that represents invalid."""
    super(InvalidTime, self).__init__(string='Invalid')


class Never(SemanticTime):
  """Semantic time that represents never."""

  _SORT_ORDER = 99

  def __init__(self):
    """Initializes a semantic time that represents never."""
    super(Never, self).__init__(string='Never')

  def __eq__(self, other):
    """Determines if the date time values are equal to other.

    Args:
      other (DateTimeValues): date time values to compare against.

    Returns:
      bool: True if the date time values are equal to other.
    """
    return isinstance(other, Never)

  def __ge__(self, other):
    """Determines if the date time values are greater than or equal to other.

    Args:
      other (DateTimeValues): date time values to compare against.

    Returns:
      bool: True if the date time values are greater than or equal to other.

    Raises:
      ValueError: if other is not an instance of DateTimeValues.
    """
    if not isinstance(other, interface.DateTimeValues):
      raise ValueError('Other not an instance of DateTimeValues')

    return True

  def __gt__(self, other):
    """Determines if the date time values are greater than other.

    Args:
      other (DateTimeValues): date time values to compare against.

    Returns:
      bool: True if the date time values are greater than other.

    Raises:
      ValueError: if other is not an instance of DateTimeValues.
    """
    if not isinstance(other, interface.DateTimeValues):
      raise ValueError('Other not an instance of DateTimeValues')

    return not isinstance(other, Never)

  def __le__(self, other):
    """Determines if the date time values are less than or equal to other.

    Args:
      other (DateTimeValues): date time values to compare against.

    Returns:
      bool: True if the date time values are greater than or equal to other.

    Raises:
      ValueError: if other is not an instance of DateTimeValues.
    """
    if not isinstance(other, interface.DateTimeValues):
      raise ValueError('Other not an instance of DateTimeValues')

    return isinstance(other, Never)

  def __lt__(self, other):
    """Determines if the date time values are less than other.

    Args:
      other (DateTimeValues): date time values to compare against.

    Returns:
      bool: True if the date time values are less than other.

    Raises:
      ValueError: if other is not an instance of DateTimeValues.
    """
    if not isinstance(other, interface.DateTimeValues):
      raise ValueError('Other not an instance of DateTimeValues')

    return False

  def __ne__(self, other):
    """Determines if the date time values are not equal to other.

    Args:
      other (DateTimeValues): date time values to compare against.

    Returns:
      bool: True if the date time values are not equal to other.
    """
    return not isinstance(other, Never)


class NotSet(SemanticTime):
  """Semantic time that represents not set."""

  _SORT_ORDER = 2

  def __init__(self):
    """Initializes a semantic time that represents not set."""
    super(NotSet, self).__init__(string='Not set')
