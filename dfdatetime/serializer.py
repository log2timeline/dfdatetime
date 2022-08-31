# -*- coding: utf-8 -*-
"""The date and time values serializer."""

from dfdatetime import factory
from dfdatetime import interface


class Serializer(object):
  """Date and time values serializer."""

  @classmethod
  def ConvertDictToDateTimeValues(cls, json_dict):
    """Converts a JSON dict into a date time values object.

    This method is deprecated use ConvertJSONToDateTimeValues instead.

    The dictionary of the JSON serialized objects consists of:
    {
        '__type__': 'DateTimeValues'
        '__class_name__': 'RFC2579DateTime'
        ...
    }

    Here '__type__' indicates the object base type. In this case this should
    be 'DateTimeValues'. The rest of the elements of the dictionary make up the
    date time values object properties.

    Args:
      json_dict (dict[str, object]): JSON serialized objects.

    Returns:
      dfdatetime.DateTimeValues: date and time values.
    """
    return cls.ConvertJSONToDateTimeValues(json_dict)

  @classmethod
  def ConvertDateTimeValuesToDict(cls, date_time_values):
    """Converts a date and time values object into a JSON dictionary.

    This method is deprecated use ConvertDateTimeValuesToJSON instead.

    The resulting dictionary of the JSON serialized objects consists of:
    {
        '__type__': 'DateTimeValues'
        '__class_name__': 'RFC2579DateTime'
        ...
    }

    Here '__type__' indicates the object base type. In this case
    'DateTimeValues'. The rest of the elements of the dictionary make up the
    date and time value object properties.

    Args:
      date_time_values (dfdatetime.DateTimeValues): date and time values.

    Returns:
      dict[str, object]: JSON serialized objects.

    Raises:
      TypeError: if object is not an instance of DateTimeValues.
    """
    if not isinstance(date_time_values, interface.DateTimeValues):
      raise TypeError

    return cls.ConvertDateTimeValuesToJSON(date_time_values)

  @classmethod
  def ConvertDateTimeValuesToJSON(cls, date_time_values):
    """Converts a date and time values object into a JSON dictionary.

    The resulting dictionary of the JSON serialized objects consists of:
    {
        '__type__': 'DateTimeValues'
        '__class_name__': 'RFC2579DateTime'
        ...
    }

    Here '__type__' indicates the object base type. In this case
    'DateTimeValues'. The rest of the elements of the dictionary make up the
    date and time value object properties.

    Args:
      date_time_values (dfdatetime.DateTimeValues): date and time values.

    Returns:
      dict[str, object]: JSON serialized objects.
    """
    class_name = type(date_time_values).__name__

    json_dict = {
        '__class_name__': class_name,
        '__type__': 'DateTimeValues'}

    if hasattr(date_time_values, 'timestamp'):
      json_dict['timestamp'] = date_time_values.timestamp

    elif hasattr(date_time_values, 'string'):
      json_dict['string'] = date_time_values.string

    elif class_name == 'FATDateTime':
      json_dict['fat_date_time'] = date_time_values.fat_date_time

    elif class_name == 'GolangTime':
      json_dict['golang_timestamp'] = date_time_values.golang_timestamp

    elif class_name == 'RFC2579DateTime':
      time_zone_hours, time_zone_minutes = divmod(
          date_time_values.time_zone_offset, 60)

      if date_time_values.time_zone_offset < 0:
        time_zone_sign = '-'
        time_zone_hours *= -1
      else:
        time_zone_sign = '+'

      json_dict['rfc2579_date_time_tuple'] = (
          date_time_values.year, date_time_values.month,
          date_time_values.day_of_month, date_time_values.hours,
          date_time_values.minutes, date_time_values.seconds,
          date_time_values.deciseconds, time_zone_sign, time_zone_hours,
          time_zone_minutes)

    elif class_name == 'TimeElements':
      json_dict['time_elements_tuple'] = (
          date_time_values.year, date_time_values.month,
          date_time_values.day_of_month, date_time_values.hours,
          date_time_values.minutes, date_time_values.seconds)

    elif class_name == 'TimeElementsInMilliseconds':
      json_dict['time_elements_tuple'] = (
          date_time_values.year, date_time_values.month,
          date_time_values.day_of_month, date_time_values.hours,
          date_time_values.minutes, date_time_values.seconds,
          date_time_values.milliseconds)

    elif class_name == 'TimeElementsInMicroseconds':
      json_dict['time_elements_tuple'] = (
          date_time_values.year, date_time_values.month,
          date_time_values.day_of_month, date_time_values.hours,
          date_time_values.minutes, date_time_values.seconds,
          date_time_values.microseconds)

    if date_time_values.time_zone_offset is not None and class_name not in (
        'GolangTime', 'RFC2579DateTime'):
      json_dict['time_zone_offset'] = date_time_values.time_zone_offset

    if date_time_values.is_local_time:
      json_dict['is_local_time'] = True

    return json_dict

  @classmethod
  def ConvertJSONToDateTimeValues(cls, json_dict):
    """Converts a JSON dict into a date time values object.

    The dictionary of the JSON serialized objects consists of:
    {
        '__type__': 'DateTimeValues'
        '__class_name__': 'RFC2579DateTime'
        ...
    }

    Here '__type__' indicates the object base type. In this case this should
    be 'DateTimeValues'. The rest of the elements of the dictionary make up the
    date time values object properties.

    Args:
      json_dict (dict[str, object]): JSON serialized objects.

    Returns:
      dfdatetime.DateTimeValues: date and time values.
    """
    class_name = json_dict.get('__class_name__', None)
    if class_name:
      del json_dict['__class_name__']

    # Remove the class type from the JSON dict since we cannot pass it.
    del json_dict['__type__']

    is_local_time = json_dict.get('is_local_time', None)
    if is_local_time is not None:
      del json_dict['is_local_time']

    if class_name in ('InvalidTime', 'Never', 'NotSet'):
      string = json_dict.get('string', None)
      if string is not None:
        del json_dict['string']

    if class_name in ('GolangTime', 'RFC2579DateTime'):
      time_zone_offset = json_dict.get('time_zone_offset', None)
      if time_zone_offset is not None:
        del json_dict['time_zone_offset']

    date_time = factory.Factory.NewDateTimeValues(class_name, **json_dict)
    if is_local_time:
      date_time.is_local_time = is_local_time

    return date_time
