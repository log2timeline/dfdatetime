# -*- coding: utf-8 -*-
"""Delphi TDateTime implementation."""

from dfdatetime import definitions
from dfdatetime import interface


class DelphiDateTime(interface.DateTimeValues):
  """Class that implements a Delphi TDateTime timestamp.

  The Delphi TDateTime timestamp is a floating point value that contains
  the number of days since 1899-12-30 00:00:00 (also known as the epoch).
  Negative values represent date and times predating the epoch.

  The maximal correct date supported by TDateTime values is limited to:
  9999-12-31 23:59:59.999

  Also see:
    http://docwiki.embarcadero.com/Libraries/XE3/en/System.TDateTime

  Attributes:
    is_local_time (bool): True if the date and time value is in local time.
    precision (str): precision of the date and time value, which should
        be one of the PRECISION_VALUES in definitions.
    timestamp (float): Delphi TDateTime timestamp.
  """
  # The difference between Dec 30, 1899 and Jan 1, 1970 in days.
  _DELPHI_TO_POSIX_BASE = 25569

  # The number of seconds per day.
  _SECONDS_PER_DAY = 86400

  # The number of microseconds per day.
  _MICROSECONDS_PER_DAY = 86400000000

  def __init__(self, timestamp=None):
    """Initializes a Delphi TDateTime timestamp.

    Args:
      timestamp (Optional[float]): Delphi TDateTime timestamp.
    """
    super(DelphiDateTime, self).__init__()
    self.precision = definitions.PRECISION_1_MILLISECOND
    self.timestamp = timestamp

  def CopyFromString(self, time_string):
    """Copies a Delphi TDateTime timestamp from a string.

    Args:
      time_string (str): date and time value formatted as:
          YYYY-MM-DD hh:mm:ss.######[+-]##:##

          Where # are numeric digits ranging from 0 to 9 and the seconds
          fraction can be either 3 or 6 digits. The time of day, seconds
          fraction and time zone offset are optional. The default time zone
          is UTC.

    Raises:
      ValueError: if the time string is invalid or not supported.
    """
    date_time_values = self._CopyDateTimeFromString(time_string)

    year = date_time_values.get(u'year', 0)
    month = date_time_values.get(u'month', 0)
    day_of_month = date_time_values.get(u'day_of_month', 0)
    hours = date_time_values.get(u'hours', 0)
    minutes = date_time_values.get(u'minutes', 0)
    seconds = date_time_values.get(u'seconds', 0)
    microseconds = date_time_values.get(u'microseconds', None)

    if year > 9999:
      raise ValueError(u'Unsupported year value: {0:d}.'.format(year))

    timestamp = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds)

    timestamp = float(timestamp) / self._SECONDS_PER_DAY
    timestamp += self._DELPHI_TO_POSIX_BASE
    if microseconds is not None:
      timestamp += float(microseconds) / self._MICROSECONDS_PER_DAY

    self.timestamp = timestamp
    self.is_local_time = False

  def CopyToStatTimeTuple(self):
    """Copies the Delphi TDateTime timestamp to a stat timestamp tuple.

    Returns:
      tuple[int, int]: a POSIX timestamp in seconds and the remainder in
          100 nano seconds or (None, None) on error.
    """
    if self.timestamp is None:
      return None, None

    timestamp = (
        (self.timestamp - self._DELPHI_TO_POSIX_BASE) * self._SECONDS_PER_DAY)
    remainder = int((timestamp % 1) * 10000000)
    return int(timestamp), remainder

  def GetPlasoTimestamp(self):
    """Retrieves a timestamp that is compatible with plaso.

    Returns:
      int: a POSIX timestamp in microseconds or None on error.
    """
    if self.timestamp is None:
      return

    timestamp = (
        (self.timestamp - self._DELPHI_TO_POSIX_BASE) *
        self._MICROSECONDS_PER_DAY)
    return int(timestamp)
