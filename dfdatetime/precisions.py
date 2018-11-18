# -*- coding: utf-8 -*-
"""Date and time precision helpers."""

from __future__ import unicode_literals

import decimal

from dfdatetime import definitions


class DateTimePrecisionHelper(object):
  """Date time precision helper interface.

  This is the super class of different date and time precision helpers.

  Time precision helpers provide functionality for converting date and time
  values between different precisions.
  """

  # pylint: disable=missing-raises-doc,redundant-returns-doc

  @classmethod
  def CopyMicrosecondsToFractionOfSecond(cls, microseconds):
    """Copies the number of microseconds to a fraction of second value.

    Args:
      microseconds (int): number of microseconds.

    Returns:
      decimal.Decimal: fraction of second, which must be a value between 0.0
          and 1.0.
    """
    raise NotImplementedError()

  @classmethod
  def CopyToDateTimeString(cls, time_elements_tuple, fraction_of_second):
    """Copies the time elements and fraction of second to a string.

    Args:
      time_elements_tuple (tuple[int, int, int, int, int, int]):
          time elements, contains year, month, day of month, hours, minutes and
          seconds.
      fraction_of_second (decimal.Decimal): fraction of second, which must be a
          value between 0.0 and 1.0.

    Returns:
      str: date and time value formatted as: YYYY-MM-DD hh:mm:ss with fraction
          of second part that corresponds to the precision.
    """
    raise NotImplementedError()


class SecondsPrecisionHelper(DateTimePrecisionHelper):
  """Seconds precision helper."""

  @classmethod
  def CopyMicrosecondsToFractionOfSecond(cls, microseconds):
    """Copies the number of microseconds to a fraction of second value.

    Args:
      microseconds (int): number of microseconds.

    Returns:
      decimal.Decimal: fraction of second, which must be a value between 0.0 and
          1.0. For the seconds precision helper this will always be 0.0.

    Raises:
      ValueError: if the number of microseconds is out of bounds.
    """
    if microseconds < 0 or microseconds >= definitions.MICROSECONDS_PER_SECOND:
      raise ValueError(
          'Number of microseconds value: {0:d} out of bounds.'.format(
              microseconds))

    return decimal.Decimal(0.0)

  @classmethod
  def CopyToDateTimeString(cls, time_elements_tuple, fraction_of_second):
    """Copies the time elements and fraction of second to a string.

    Args:
      time_elements_tuple (tuple[int, int, int, int, int, int]):
          time elements, contains year, month, day of month, hours, minutes and
          seconds.
      fraction_of_second (decimal.Decimal): fraction of second, which must be a
          value between 0.0 and 1.0.

    Returns:
      str: date and time value formatted as:
          YYYY-MM-DD hh:mm:ss

    Raises:
      ValueError: if the fraction of second is out of bounds.
    """
    if fraction_of_second < 0.0 or fraction_of_second >= 1.0:
      raise ValueError('Fraction of second value: {0:f} out of bounds.'.format(
          fraction_of_second))

    return '{0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}'.format(
        time_elements_tuple[0], time_elements_tuple[1], time_elements_tuple[2],
        time_elements_tuple[3], time_elements_tuple[4], time_elements_tuple[5])


class MillisecondsPrecisionHelper(DateTimePrecisionHelper):
  """Milliseconds precision helper."""

  @classmethod
  def CopyMicrosecondsToFractionOfSecond(cls, microseconds):
    """Copies the number of microseconds to a fraction of second value.

    Args:
      microseconds (int): number of microseconds.

    Returns:
      decimal.Decimal: fraction of second, which must be a value between 0.0 and
          1.0.

    Raises:
      ValueError: if the number of microseconds is out of bounds.
    """
    if microseconds < 0 or microseconds >= definitions.MICROSECONDS_PER_SECOND:
      raise ValueError(
          'Number of microseconds value: {0:d} out of bounds.'.format(
              microseconds))

    milliseconds, _ = divmod(
        microseconds, definitions.MICROSECONDS_PER_MILLISECOND)
    return decimal.Decimal(milliseconds) / definitions.MILLISECONDS_PER_SECOND

  @classmethod
  def CopyToDateTimeString(cls, time_elements_tuple, fraction_of_second):
    """Copies the time elements and fraction of second to a string.

    Args:
      time_elements_tuple (tuple[int, int, int, int, int, int]):
          time elements, contains year, month, day of month, hours, minutes and
          seconds.
      fraction_of_second (decimal.Decimal): fraction of second, which must be a
          value between 0.0 and 1.0.

    Returns:
      str: date and time value formatted as:
          YYYY-MM-DD hh:mm:ss.###

    Raises:
      ValueError: if the fraction of second is out of bounds.
    """
    if fraction_of_second < 0.0 or fraction_of_second >= 1.0:
      raise ValueError('Fraction of second value: {0:f} out of bounds.'.format(
          fraction_of_second))

    milliseconds = int(fraction_of_second * definitions.MILLISECONDS_PER_SECOND)

    return '{0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}.{6:03d}'.format(
        time_elements_tuple[0], time_elements_tuple[1], time_elements_tuple[2],
        time_elements_tuple[3], time_elements_tuple[4], time_elements_tuple[5],
        milliseconds)


class MicrosecondsPrecisionHelper(DateTimePrecisionHelper):
  """Microseconds precision helper."""

  @classmethod
  def CopyMicrosecondsToFractionOfSecond(cls, microseconds):
    """Copies the number of microseconds to a fraction of second value.

    Args:
      microseconds (int): number of microseconds.

    Returns:
      decimal.Decimal: fraction of second, which must be a value between 0.0 and
          1.0.

    Raises:
      ValueError: if the number of microseconds is out of bounds.
    """
    if microseconds < 0 or microseconds >= definitions.MICROSECONDS_PER_SECOND:
      raise ValueError(
          'Number of microseconds value: {0:d} out of bounds.'.format(
              microseconds))

    return decimal.Decimal(microseconds) / definitions.MICROSECONDS_PER_SECOND

  @classmethod
  def CopyToDateTimeString(cls, time_elements_tuple, fraction_of_second):
    """Copies the time elements and fraction of second to a string.

    Args:
      time_elements_tuple (tuple[int, int, int, int, int, int]):
          time elements, contains year, month, day of month, hours, minutes and
          seconds.
      fraction_of_second (decimal.Decimal): fraction of second, which must be a
          value between 0.0 and 1.0.

    Returns:
      str: date and time value formatted as:
          YYYY-MM-DD hh:mm:ss.######

    Raises:
      ValueError: if the fraction of second is out of bounds.
    """
    if fraction_of_second < 0.0 or fraction_of_second >= 1.0:
      raise ValueError('Fraction of second value: {0:f} out of bounds.'.format(
          fraction_of_second))

    microseconds = int(fraction_of_second * definitions.MICROSECONDS_PER_SECOND)

    return '{0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}.{6:06d}'.format(
        time_elements_tuple[0], time_elements_tuple[1], time_elements_tuple[2],
        time_elements_tuple[3], time_elements_tuple[4], time_elements_tuple[5],
        microseconds)


class PrecisionHelperFactory(object):
  """Date time precision helper factory."""

  _PRECISION_CLASSES = {
      definitions.PRECISION_1_MICROSECOND: MicrosecondsPrecisionHelper,
      definitions.PRECISION_1_MILLISECOND: MillisecondsPrecisionHelper,
      definitions.PRECISION_1_SECOND: SecondsPrecisionHelper,
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
