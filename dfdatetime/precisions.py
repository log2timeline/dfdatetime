# -*- coding: utf-8 -*-
"""Date and time precision helpers."""

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
          f'Number of microseconds value: {microseconds:d} out of bounds.')

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
      raise ValueError(
          f'Fraction of second value: {fraction_of_second:f} out of bounds.')

    year, month, day_of_month, hours, minutes, seconds = time_elements_tuple

    return (f'{year:04d}-{month:02d}-{day_of_month:02d} '
            f'{hours:02d}:{minutes:02d}:{seconds:02d}')


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
          f'Number of microseconds value: {microseconds:d} out of bounds.')

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
      raise ValueError(
          f'Fraction of second value: {fraction_of_second:f} out of bounds.')

    year, month, day_of_month, hours, minutes, seconds = time_elements_tuple
    milliseconds = int(fraction_of_second * definitions.MILLISECONDS_PER_SECOND)

    return (f'{year:04d}-{month:02d}-{day_of_month:02d} '
            f'{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}')


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
          f'Number of microseconds value: {microseconds:d} out of bounds.')

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
      raise ValueError(
          f'Fraction of second value: {fraction_of_second:f} out of bounds.')

    year, month, day_of_month, hours, minutes, seconds = time_elements_tuple
    microseconds = int(fraction_of_second * definitions.MICROSECONDS_PER_SECOND)

    return (f'{year:04d}-{month:02d}-{day_of_month:02d} '
            f'{hours:02d}:{minutes:02d}:{seconds:02d}.{microseconds:06d}')


class PrecisionHelperFactory(object):
  """Date time precision helper factory."""

  _PRECISION_CLASSES = {
      definitions.PRECISION_1_MICROSECOND: MicrosecondsPrecisionHelper,
      definitions.PRECISION_1_MILLISECOND: MillisecondsPrecisionHelper,
      definitions.PRECISION_1_SECOND: SecondsPrecisionHelper}

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
      raise ValueError(f'Unsupported precision: {precision!s}')

    return precision_helper_class
