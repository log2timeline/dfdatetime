# -*- coding: utf-8 -*-
"""Java java.util.Date timestamp implementation."""

from __future__ import unicode_literals

from dfdatetime import posix_time


class JavaTime(posix_time.PosixTimeInMilliseconds):
  """Java java.util.Date timestamp.

  The Java java.util.Date timestamp is a signed integer that contains the
  number of milliseconds since 1970-01-01 00:00:00 (also known as the POSIX
  epoch). Negative values represent date and times predating the POSIX epoch.

  Also see:
    https://docs.oracle.com/javase/8/docs/api/java/util/Date.html

  Attributes:
    is_local_time (bool): True if the date and time value is in local time.
  """
