# -*- coding: utf-8 -*-
"""Time elements implementation."""

from dfdatetime import definitions
from dfdatetime import interface


class TimeElements(interface.DateTimeValues):
  """Class that implements time elements.

  Time elements contain separate values for year, month, day of month,
  hours, minutes and seconds.

  Attributes:
    is_local_time (bool): True if the date and time value is in local time.
    precision (str): precision of the date and time value, which should
        be one of the PRECISION_VALUES in definitions.
  """

  def __init__(self, time_elements_tuple=None):
    """Initializes time elements.

    Args:
      time_elements_tuple (Optional[tuple[int, int, int, int, int, int]]):
          time elements, contains year, month, day of month, hours, minutes and
          seconds.
    """
    super(TimeElements, self).__init__()
    if time_elements_tuple is None:
      self._number_of_seconds = None
    else:
      self._number_of_seconds = self._GetNumberOfSecondsFromElements(
          *time_elements_tuple)
    self._time_elements_tuple = time_elements_tuple
    self.precision = definitions.PRECISION_1_SECOND

  def CopyFromString(self, time_string):
    """Copies time elements from a string containing a date and time value.

    Args:
      time_string (str): date and time value formatted as:
          YYYY-MM-DD hh:mm:ss.######[+-]##:##

          Where # are numeric digits ranging from 0 to 9 and the seconds
          fraction can be either 3 or 6 digits. The time of day, seconds
          fraction and time zone offset are optional. The default time zone
          is UTC.
    """
    date_time_values = self._CopyDateTimeFromString(time_string)

    year = date_time_values.get(u'year', 0)
    month = date_time_values.get(u'month', 0)
    day_of_month = date_time_values.get(u'day_of_month', 0)
    hours = date_time_values.get(u'hours', 0)
    minutes = date_time_values.get(u'minutes', 0)
    seconds = date_time_values.get(u'seconds', 0)

    self._time_elements_tuple = (
        year, month, day_of_month, hours, minutes, seconds)
    self._number_of_seconds = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds)

    self.is_local_time = False

  def CopyFromStringISO8601(self, time_string):
    """Copies time elements from a ISO 8601 date and time string.

    Currently not supported:
    * Duration notation: "P..."
    * Week notation "2016-W33"
    * Date with week number notation "2016-W33-3"
    * Date without year notation "--08-17"
    * Ordinal date notation "2016-230"
    * Seconds fraction of a size other than 3 or 6

    Args:
      time_string (str): date and time value formatted as:
          YYYY-MM-DDThh:mm:ss.######[+-]##:##

          Where # are numeric digits ranging from 0 to 9 and the seconds
          fraction can be either 3 or 6 digits. The time of day, seconds
          fraction and time zone offset are optional. The default time zone
          is UTC.

    Raises:
      ValueError: if the time string is invalid or not supported.
    """
    if not time_string:
      raise ValueError(u'Invalid time string.')

    time_string_length = len(time_string)
    if time_string_length >= 11:
      if time_string[10] != u'T':
        raise ValueError(u'Invalid time string.')

      # Replace "T" by " ".
      time_string = u'{0:s} {1:s}'.format(time_string[:10], time_string[11:])

    if time_string_length >= 20 and time_string[19] == u',':
      # Replace "," by ".".
      time_string = u'{0:s}.{1:s}'.format(time_string[:19], time_string[20:])

    if time_string.endswith(u'Z'):
      time_string = time_string[:-1]

    self.CopyFromString(time_string)

  def CopyToStatTimeTuple(self):
    """Copies the time elements to a stat timestamp tuple.

    Returns:
      tuple[int, int]: a POSIX timestamp in seconds and the remainder in
          100 nano seconds or (None, None) on error.
    """
    if self._number_of_seconds is None:
      return None, None
    return self._number_of_seconds, None

  def GetPlasoTimestamp(self):
    """Retrieves a timestamp that is compatible with plaso.

    Returns:
      int: a POSIX timestamp in microseconds or None on error.
    """
    if self._number_of_seconds is None:
      return
    return self._number_of_seconds * 1000000
