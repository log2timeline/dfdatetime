# -*- coding: utf-8 -*-
"""OLE automation date (or Floatingtime or Application time) implementation."""

from __future__ import unicode_literals

import decimal

from dfdatetime import definitions
from dfdatetime import interface


class OLEAutomationDateEpoch(interface.DateTimeEpoch):
  """OLE automation date epoch."""

  def __init__(self):
    """Initializes a OLE automation date epoch."""
    super(OLEAutomationDateEpoch, self).__init__(1899, 12, 30)


class OLEAutomationDate(interface.DateTimeValues):
  """OLE Automation date.

  The OLE Automation date is a floating point value that contains the number of
  days since 1899-12-30 (also known as the OLE Automation date epoch), and the
  fractional part represents the fraction of a day since midnight. Negative
  values represent date and times predating the OLE Automation date epoch.

  Also see:
    https://msdn.microsoft.com/en-us/library/system.datetime.tooadate(v=vs.110).aspx

  Attributes:
    is_local_time (bool): True if the date and time value is in local time.
  """
  _EPOCH = OLEAutomationDateEpoch()

  # The difference between December 30, 1899 and January 1, 1970 in days.
  _OLE_AUTOMATION_DATE_TO_POSIX_BASE = 25569

  def __init__(self, timestamp=None):
    """Initializes an OLE Automation date.

    Args:
      timestamp (Optional[float]): OLE Automation date.
    """
    super(OLEAutomationDate, self).__init__()
    self._precision = definitions.PRECISION_1_MICROSECOND
    self._timestamp = timestamp

  @property
  def timestamp(self):
    """float: OLE Automation date timestamp or None if timestamp is not set."""
    return self._timestamp

  def _GetNormalizedTimestamp(self):
    """Retrieves the normalized timestamp.

    Returns:
      decimal.Decimal: normalized timestamp, which contains the number of
          seconds since January 1, 1970 00:00:00 and a fraction of second used
          for increased precision, or None if the normalized timestamp cannot be
          determined.
    """
    if self._normalized_timestamp is None:
      if self._timestamp is not None:
        self._normalized_timestamp = (
            decimal.Decimal(self._timestamp) -
            self._OLE_AUTOMATION_DATE_TO_POSIX_BASE)
        self._normalized_timestamp *= definitions.SECONDS_PER_DAY

    return self._normalized_timestamp

  def CopyFromDateTimeString(self, time_string):
    """Copies an OLE Automation date from a date and time string.

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

    timestamp = self._GetNumberOfSecondsFromElements(
        year, month, day_of_month, hours, minutes, seconds)

    timestamp = float(timestamp)
    if microseconds is not None:
      timestamp += float(microseconds) / definitions.MICROSECONDS_PER_SECOND

    timestamp /= definitions.SECONDS_PER_DAY
    timestamp += self._OLE_AUTOMATION_DATE_TO_POSIX_BASE

    self._normalized_timestamp = None
    self._timestamp = timestamp
    self.is_local_time = False

  def CopyToDateTimeString(self):
    """Copies the OLE Automation date to a date and time string.

    Returns:
      str: date and time value formatted as: "YYYY-MM-DD hh:mm:ss.######" or
          None if the timestamp is missing.
    """
    if self._timestamp is None:
      return None

    timestamp = self._timestamp * definitions.SECONDS_PER_DAY

    number_of_days, hours, minutes, seconds = self._GetTimeValues(
        int(timestamp))

    year, month, day_of_month = self._GetDateValuesWithEpoch(
        number_of_days, self._EPOCH)

    microseconds = int((timestamp % 1) * definitions.MICROSECONDS_PER_SECOND)

    return '{0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}.{6:06d}'.format(
        year, month, day_of_month, hours, minutes, seconds, microseconds)
