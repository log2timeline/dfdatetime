# -*- coding: utf-8 -*-
"""Date and time precision helpers."""

from __future__ import unicode_literals

from dfdatetime import definitions


class DateTimePrecisionHelper(object):
  """Date time precision helper interface.

  This is the super class of different date and time precision helpers.
  """

  @classmethod
  def CopyMicrosecondsToFractionOfSecond(cls, microseconds):
    """Copies the number of microseconds to a fraction of second value.

    Args:
      microseconds (int): number of microseconds.

    Returns:
      float: fraction of second value.
    """
    raise NotImplementedError()

  @classmethod
  def CopyToDateTimeString(cls, time_elements_tuple, fraction_of_second):
    """Copies the date time value to a date and time string.

    Args:
      time_elements_tuple (tuple[int, int, int, int, int, int]):
          time elements, contains year, month, day of month, hours, minutes and
          seconds.
      fraction_of_second (float): fraction of second.

    Returns:
      str: date and time value formatted as:
          YYYY-MM-DD hh:mm:ss.######
    """
    raise NotImplementedError()


class MillisecondsPrecisionHelper(DateTimePrecisionHelper):
  """Milliseconds precision helper."""

  @classmethod
  def CopyMicrosecondsToFractionOfSecond(cls, microseconds):
    """Copies the number of microseconds to a fraction of second value.

    Args:
      microseconds (int): number of microseconds.

    Returns:
      float: fraction of second value.
    """
    milliseconds, _ = divmod(
        microseconds, definitions.MICROSECONDS_PER_MILLISECOND)
    return float(milliseconds) / definitions.MILLISECONDS_PER_SECOND

  @classmethod
  def CopyToDateTimeString(cls, time_elements_tuple, fraction_of_second):
    """Copies the date time value to a date and time string.

    Args:
      time_elements_tuple (tuple[int, int, int, int, int, int]):
          time elements, contains year, month, day of month, hours, minutes and
          seconds.
      fraction_of_second (float): fraction of second.

    Returns:
      str: date and time value formatted as:
          YYYY-MM-DD hh:mm:ss.###
    """
    fraction_of_second = int(
        fraction_of_second * definitions.MILLISECONDS_PER_SECOND)

    return '{0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}.{6:03d}'.format(
        time_elements_tuple[0], time_elements_tuple[1], time_elements_tuple[2],
        time_elements_tuple[3], time_elements_tuple[4], time_elements_tuple[5],
        fraction_of_second)


class MicrosecondsPrecisionHelper(DateTimePrecisionHelper):
  """Microseconds precision helper."""

  @classmethod
  def CopyMicrosecondsToFractionOfSecond(cls, microseconds):
    """Copies the number of microseconds to a fraction of second value.

    Args:
      microseconds (int): number of microseconds.

    Returns:
      float: fraction of second value.
    """
    return float(microseconds) / definitions.MICROSECONDS_PER_SECOND

  @classmethod
  def CopyToDateTimeString(cls, time_elements_tuple, fraction_of_second):
    """Copies the time elements to a date and time string.

    Args:
      time_elements_tuple (tuple[int, int, int, int, int, int]):
          time elements, contains year, month, day of month, hours, minutes and
          seconds.
      fraction_of_second (float): fraction of second.

    Returns:
      str: date and time value formatted as:
          YYYY-MM-DD hh:mm:ss.######
    """
    fraction_of_second = int(
        fraction_of_second * definitions.MICROSECONDS_PER_SECOND)

    return '{0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}.{6:06d}'.format(
        time_elements_tuple[0], time_elements_tuple[1], time_elements_tuple[2],
        time_elements_tuple[3], time_elements_tuple[4], time_elements_tuple[5],
        fraction_of_second)


class PrecisionHelperFactory(object):
  """Date time precision helper factory."""

  _PRECISION_CLASSES = {
      definitions.PRECISION_1_MICROSECOND: MicrosecondsPrecisionHelper,
      definitions.PRECISION_1_MILLISECOND: MillisecondsPrecisionHelper,
  }

  @classmethod
  def CreatePrecisionHelper(cls, precision):
    """Creates a precision helper.

    Args:
      precision (str): precision of the date and time value, which should
          be one of the PRECISION_VALUES in definitions.

    Returns:
      class: date time precision helper class.

    Raises:
      ValueError: if the precision value is unsupported.
    """
    precision_helper_class = cls._PRECISION_CLASSES.get(precision, None)
    if not precision_helper_class:
      raise ValueError('Unsupported precision: {0!s}'.format(precision))

    return precision_helper_class
