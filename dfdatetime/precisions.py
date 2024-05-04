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
  def CopyNanosecondsToFractionOfSecond(cls, nanoseconds):
    """Copies the number of nanoseconds to a fraction of second value.

    Args:
      nanoseconds (int): number of nanoseconds.

    Returns:
      decimal.Decimal: fraction of second, which must be a value between 0.0 and
          1.0.
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
  def CopyNanosecondsToFractionOfSecond(cls, nanoseconds):
    """Copies the number of nanoseconds to a fraction of second value.

    Args:
      nanoseconds (int): number of nanoseconds.

    Returns:
      decimal.Decimal: fraction of second, which must be a value between 0.0 and
          1.0. For the seconds precision helper this will always be 0.0.

    Raises:
      ValueError: if the number of nanoseconds is out of bounds.
    """
    if nanoseconds < 0 or nanoseconds >= definitions.NANOSECONDS_PER_SECOND:
      raise ValueError(
          f'Number of nanoseconds value: {nanoseconds:d} out of bounds.')

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


class CentisecondsPrecisionHelper(DateTimePrecisionHelper):
  """Centiseconds (10 ms) precision helper."""

  @classmethod
  def CopyNanosecondsToFractionOfSecond(cls, nanoseconds):
    """Copies the number of nanoseconds to a fraction of second value.

    Args:
      nanoseconds (int): number of nanoseconds.

    Returns:
      decimal.Decimal: fraction of second, which must be a value between 0.0 and
          1.0.

    Raises:
      ValueError: if the number of nanoseconds is out of bounds.
    """
    if nanoseconds < 0 or nanoseconds >= definitions.NANOSECONDS_PER_SECOND:
      raise ValueError(
          f'Number of nanoseconds value: {nanoseconds:d} out of bounds.')

    centiseconds, _ = divmod(
        nanoseconds, definitions.NANOSECONDS_PER_CENTISECOND)
    return decimal.Decimal(centiseconds) / definitions.CENTISECONDS_PER_SECOND

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
          YYYY-MM-DD hh:mm:ss.##

    Raises:
      ValueError: if the fraction of second is out of bounds.
    """
    if fraction_of_second < 0.0 or fraction_of_second >= 1.0:
      raise ValueError(
          f'Fraction of second value: {fraction_of_second:f} out of bounds.')

    year, month, day_of_month, hours, minutes, seconds = time_elements_tuple
    centiseconds = int(fraction_of_second * definitions.CENTISECONDS_PER_SECOND)

    return (f'{year:04d}-{month:02d}-{day_of_month:02d} '
            f'{hours:02d}:{minutes:02d}:{seconds:02d}.{centiseconds:02d}')


class MillisecondsPrecisionHelper(DateTimePrecisionHelper):
  """Milliseconds precision helper."""

  @classmethod
  def CopyNanosecondsToFractionOfSecond(cls, nanoseconds):
    """Copies the number of nanoseconds to a fraction of second value.

    Args:
      nanoseconds (int): number of nanoseconds.

    Returns:
      decimal.Decimal: fraction of second, which must be a value between 0.0 and
          1.0.

    Raises:
      ValueError: if the number of nanoseconds is out of bounds.
    """
    if nanoseconds < 0 or nanoseconds >= definitions.NANOSECONDS_PER_SECOND:
      raise ValueError(
          f'Number of nanoseconds value: {nanoseconds:d} out of bounds.')

    milliseconds, _ = divmod(
        nanoseconds, definitions.NANOSECONDS_PER_MILLISECOND)
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


class DecimillisecondsPrecisionHelper(DateTimePrecisionHelper):
  """Decimilliseconds (100 microseconds) precision helper."""

  @classmethod
  def CopyNanosecondsToFractionOfSecond(cls, nanoseconds):
    """Copies the number of nanoseconds to a fraction of second value.

    Args:
      nanoseconds (int): number of nanoseconds.

    Returns:
      decimal.Decimal: fraction of second, which must be a value between 0.0
          and 1.0.

    Raises:
      ValueError: if the number of nanoseconds is out of bounds.
    """
    if nanoseconds < 0 or nanoseconds >= definitions.NANOSECONDS_PER_SECOND:
      raise ValueError(
          f'Number of nanoseconds value: {nanoseconds:d} out of bounds.')

    decimiliseconds, _ = divmod(
        nanoseconds, definitions.NANOSECONDS_PER_DECIMILISECOND)
    return (
        decimal.Decimal(decimiliseconds) /
        definitions.DECIMICROSECONDS_PER_SECOND)

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
          YYYY-MM-DD hh:mm:ss.####

    Raises:
      ValueError: if the fraction of second is out of bounds.
    """
    if fraction_of_second < 0.0 or fraction_of_second >= 1.0:
      raise ValueError(
          f'Fraction of second value: {fraction_of_second:f} out of bounds.')

    year, month, day_of_month, hours, minutes, seconds = time_elements_tuple
    decimicroseconds = int(
        fraction_of_second * definitions.DECIMICROSECONDS_PER_SECOND)

    return (f'{year:04d}-{month:02d}-{day_of_month:02d} '
            f'{hours:02d}:{minutes:02d}:{seconds:02d}.{decimicroseconds:04d}')


class MicrosecondsPrecisionHelper(DateTimePrecisionHelper):
  """Microseconds precision helper."""

  @classmethod
  def CopyNanosecondsToFractionOfSecond(cls, nanoseconds):
    """Copies the number of nanoseconds to a fraction of second value.

    Args:
      nanoseconds (int): number of nanoseconds.

    Returns:
      decimal.Decimal: fraction of second, which must be a value between 0.0 and
          1.0.

    Raises:
      ValueError: if the number of nanoseconds is out of bounds.
    """
    if nanoseconds < 0 or nanoseconds >= definitions.NANOSECONDS_PER_SECOND:
      raise ValueError(
          f'Number of nanoseconds value: {nanoseconds:d} out of bounds.')

    microseconds, _ = divmod(
        nanoseconds, definitions.NANOSECONDS_PER_MICROSECOND)
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


class NanosecondsPrecisionHelper(DateTimePrecisionHelper):
  """Nanoseconds precision helper."""

  @classmethod
  def CopyNanosecondsToFractionOfSecond(cls, nanoseconds):
    """Copies the number of nanoseconds to a fraction of second value.

    Args:
      nanoseconds (int): number of nanoseconds.

    Returns:
      decimal.Decimal: fraction of second, which must be a value between 0.0 and
          1.0.

    Raises:
      ValueError: if the number of nanoseconds is out of bounds.
    """
    if nanoseconds < 0 or nanoseconds >= definitions.NANOSECONDS_PER_SECOND:
      raise ValueError(
          f'Number of nanoseconds value: {nanoseconds:d} out of bounds.')

    return decimal.Decimal(nanoseconds) / definitions.NANOSECONDS_PER_SECOND

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
    nanoseconds = int(fraction_of_second * definitions.NANOSECONDS_PER_SECOND)

    return (f'{year:04d}-{month:02d}-{day_of_month:02d} '
            f'{hours:02d}:{minutes:02d}:{seconds:02d}.{nanoseconds:09d}')


class PrecisionHelperFactory(object):
  """Date time precision helper factory."""

  _PRECISION_CLASSES = {
      definitions.PRECISION_10_MILLISECONDS: CentisecondsPrecisionHelper,
      definitions.PRECISION_100_MICROSECONDS: DecimillisecondsPrecisionHelper,
      definitions.PRECISION_1_MICROSECOND: MicrosecondsPrecisionHelper,
      definitions.PRECISION_1_MILLISECOND: MillisecondsPrecisionHelper,
      definitions.PRECISION_1_NANOSECOND: NanosecondsPrecisionHelper,
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
