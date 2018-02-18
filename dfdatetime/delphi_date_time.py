# -*- coding: utf-8 -*-
"""Delphi TDateTime implementation."""

from __future__ import unicode_literals

from dfdatetime import definitions
from dfdatetime import interface


class DelphiDateTimeEpoch(interface.DateTimeEpoch):
  """Delphi TDateTime epoch."""

  def __init__(self):
    """Initializes a Delphi TDateTime epoch."""
    super(DelphiDateTimeEpoch, self).__init__(1899, 12, 30)


class DelphiDateTime(interface.DateTimeValues):
  """Delphi TDateTime timestamp.

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

  _EPOCH = DelphiDateTimeEpoch()

  def __init__(self, timestamp=None):
    """Initializes a Delphi TDateTime timestamp.

    Args:
      timestamp (Optional[float]): Delphi TDateTime timestamp.
    """
    super(DelphiDateTime, self).__init__()
    self.precision = definitions.PRECISION_1_MILLISECOND
    self.timestamp = timestamp

  def CopyFromDateTimeString(self, time_string):
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

    year = date_time_values.get('year', 0)
    month = date_time_values.get('month', 0)
    day_of_month = date_time_values.get('day_of_month', 0)
    hours = date_time_values.get('hours', 0)
    minutes = date_time_values.get('minutes', 0)
    seconds = date_time_values.get('seconds', 0)
    microseconds = date_time_values.get('microseconds', None)

    if year > 9999:
      raise ValueError('Unsupported year value: {0:d}.'.format(year))

    timestamp = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds)

    timestamp = float(timestamp) / definitions.SECONDS_PER_DAY
    timestamp += self._DELPHI_TO_POSIX_BASE
    if microseconds is not None:
      timestamp += float(microseconds) / definitions.MICROSECONDS_PER_DAY

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

    timestamp = definitions.SECONDS_PER_DAY * (
        self.timestamp - self._DELPHI_TO_POSIX_BASE)
    remainder = int((timestamp % 1) * self._100NS_PER_SECOND)
    return int(timestamp), remainder

  def CopyToDateTimeString(self):
    """Copies the Delphi TDateTime timestamp to a date and time string.

    Returns:
      str: date and time value formatted as:
          YYYY-MM-DD hh:mm:ss.######
    """
    if self.timestamp is None:
      return

    number_of_seconds = self.timestamp * definitions.SECONDS_PER_DAY

    number_of_days, hours, minutes, seconds = self._GetTimeValues(
        int(number_of_seconds))

    year, month, day_of_month = self._GetDateValuesWithEpoch(
        number_of_days, self._EPOCH)

    microseconds = int(
        (number_of_seconds % 1) * definitions.MICROSECONDS_PER_SECOND)

    return '{0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}.{6:06d}'.format(
        year, month, day_of_month, hours, minutes, seconds, microseconds)

  def GetDate(self):
    """Retrieves the date represented by the date and time values.

    Returns:
       tuple[int, int, int]: year, month, day of month or (None, None, None)
           if the date and time values do not represent a date.
    """
    if self.timestamp is None:
      return None, None, None

    try:
      number_of_seconds = self.timestamp * definitions.SECONDS_PER_DAY
      number_of_days, _, _, _ = self._GetTimeValues(int(number_of_seconds))
      return self._GetDateValuesWithEpoch(number_of_days, self._EPOCH)

    except ValueError:
      return None, None, None

  def GetPlasoTimestamp(self):
    """Retrieves a timestamp that is compatible with plaso.

    Returns:
      int: a POSIX timestamp in microseconds or None on error.
    """
    if self.timestamp is None:
      return

    timestamp = (
        (self.timestamp - self._DELPHI_TO_POSIX_BASE) *
        definitions.MICROSECONDS_PER_DAY)
    return int(timestamp)
