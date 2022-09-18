# -*- coding: utf-8 -*-
"""The date and time values factory."""


class Factory(object):
  """Date and time values factory."""

  _date_time_values_types = {}

  @classmethod
  def DeregisterDateTimeValues(cls, date_time_values_type):
    """Deregisters a date and time values type.

    Args:
      date_time_values_type (type): date and time values type.

    Raises:
      KeyError: if date and time values type is not registered.
    """
    class_name = date_time_values_type.__name__
    if class_name not in cls._date_time_values_types:
      raise KeyError(f'Date and time values type: {class_name:s} not set.')

    del cls._date_time_values_types[class_name]

  @classmethod
  def NewDateTimeValues(cls, class_name, **kwargs):
    """Creates a new date and time values for the specific type indicator.

    Args:
      class_name (str): type indicator.
      kwargs (dict): keyword arguments depending on the date and time values.

    Returns:
      DateTimeValues: date and time values.

    Raises:
      KeyError: if date and time values is not registered.
    """
    if class_name not in cls._date_time_values_types:
      raise KeyError(f'Date and time values type: {class_name:s} not set.')

    date_time_values_type = cls._date_time_values_types[class_name]
    return date_time_values_type(**kwargs)

  @classmethod
  def RegisterDateTimeValues(cls, date_time_values_type):
    """Registers a date and time values type.

    Args:
      date_time_values_type (type): date and time values type.

    Raises:
      KeyError: if date and time values is already registered.
    """
    class_name = date_time_values_type.__name__
    if class_name in cls._date_time_values_types:
      raise KeyError(f'Date and time values type: {class_name:s} already set.')

    cls._date_time_values_types[class_name] = date_time_values_type
