# -*- coding: utf-8 -*-
"""FAT date time implementation."""

from dfdatetime import interface


class FATDateTime(interface.DateTimeValues):
  """Class that implements a FAT date time.

  The FAT date time is mainly used in DOS/Windows file formats and FAT.

  The FAT date and time is a 32-bit value containing two 16-bit values:
    * The date (lower 16-bit).
      * bits 0 - 4:  day of month, where 1 represents the first day
      * bits 5 - 8:  month of year, where 1 represent January
      * bits 9 - 15: year since 1980
    * The time of day (upper 16-bit).
      * bits 0 - 4: seconds (in 2 second intervals)
      * bits 5 - 10: minutes
      * bits 11 - 15: hours

  The FAT date time has no time zone information and is typically stored
  in the local time of the computer.
  """

  # The difference between Jan 1, 1980 and Jan 1, 1970 in seconds.
  _FAT_DATE_TO_POSIX_BASE = 315532800

  def __init__(self, fat_date_time=None):
    """Initializes a FAT date time object.

    Args:
      fat_date_time (Optional[int]): FAT date time.
    """
    super(FATDateTime, self).__init__()
    self._number_of_seconds = self._GetNumberOfSeconds(fat_date_time)

  def _GetNumberOfSeconds(self, fat_date_time):
    """Retrieves the number of seconds from a FAT date time.

    Args:
      fat_date_time (int): FAT date time.

    Returns:
      int: number of seconds since January 1, 1980 00:00:00.

    Raises:
      ValueError: if the month, day of month, hours, minutes or seconds
          value is out of bounds.
    """
    day_of_month = (fat_date_time & 0x1f)
    month = ((fat_date_time >> 5) & 0x0f)
    year = (fat_date_time >> 9) & 0x7f

    days_per_month = self._GetDaysPerMonth(year, month)
    if day_of_month < 1 or day_of_month > days_per_month:
      raise ValueError(u'Day of month value out of bounds.')

    number_of_days = self._GetDayOfYear(1980 + year, month, day_of_month)
    for past_year in range(0, year):
      number_of_days += self._GetNumberOfDaysInYear(past_year)

    fat_date_time >>= 16

    seconds = (fat_date_time & 0x1f) * 2
    minutes = (fat_date_time >> 5) & 0x3f
    hours = (fat_date_time >> 11) & 0x1f

    if hours not in range(0, 24):
      raise ValueError(u'Hours value out of bounds.')

    if minutes not in range(0, 60):
      raise ValueError(u'Minutes value out of bounds.')

    if seconds not in range(0, 60):
      raise ValueError(u'Seconds value out of bounds.')

    number_of_seconds = (((hours * 60) + minutes) * 60) + seconds
    number_of_seconds += number_of_days * self._SECONDS_PER_DAY
    return number_of_seconds

  def CopyFromString(self, time_string):
    """Copies a FAT date time from a string containing a date and time value.

    Args:
      time_string (str): date and time value formatted as:
          YYYY-MM-DD hh:mm:ss.######[+-]##:##

          Where # are numeric digits ranging from 0 to 9 and the seconds
          fraction can be either 3 or 6 digits. The time of day, seconds
          fraction and timezone offset are optional. The default timezone
          is UTC.

    Raises:
      ValueError: if the time string is invalid or not supported.
    """
    if not time_string:
      raise ValueError(u'Invalid time string.')

    # TODO: implement.
    raise NotImplementedError()

  def CopyToStatTimeTuple(self):
    """Copies the FAT date time to a stat timestamp tuple.

    Returns:
      tuple[int, int]: a POSIX timestamp in seconds and the remainder in
          100 nano seconds or (None, None) on error.
    """
    if self._number_of_seconds < 0:
      return None, None

    timestamp = self._number_of_seconds + self._FAT_DATE_TO_POSIX_BASE
    return timestamp, 0

  def GetPlasoTimestamp(self):
    """Retrieves a timestamp that is compatible with plaso.

    Returns:
      int: a POSIX timestamp in microseconds or None on error.
    """
    if self._number_of_seconds < 0:
      return

    return (self._number_of_seconds + self._FAT_DATE_TO_POSIX_BASE) * 1000000
