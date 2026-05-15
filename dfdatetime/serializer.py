"""The date and time values serializer."""

from dfdatetime import factory
from dfdatetime import interface


class Serializer:
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
        return date_time_values.CopyToSerializableDict()

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

        Raises:
          KeyError: If date and time values type is not supported by factory.
        """
        class_name = json_dict.get("__class_name__")
        if class_name:
            del json_dict["__class_name__"]

        # Remove the class type from the JSON dict since we cannot pass it.
        del json_dict["__type__"]

        if class_name not in (
            "TimeElements",
            "TimeElementsInMilliseconds",
            "TimeElementsInMicroseconds",
        ):
            is_delta = json_dict.get("is_delta")
            if is_delta is not None:
                del json_dict["is_delta"]

        is_local_time = json_dict.get("is_local_time")
        if is_local_time is not None:
            del json_dict["is_local_time"]

        time_zone_hint = json_dict.get("time_zone_hint")
        if time_zone_hint is not None:
            del json_dict["time_zone_hint"]

        if class_name in ("InvalidTime", "Never", "NotSet"):
            string = json_dict.get("string")
            if string is not None:
                del json_dict["string"]

        if class_name in ("GolangTime", "RFC2579DateTime"):
            time_zone_offset = json_dict.get("time_zone_offset")
            if time_zone_offset is not None:
                del json_dict["time_zone_offset"]

        date_time = factory.Factory.NewDateTimeValues(class_name, **json_dict)
        if is_local_time:
            date_time.is_local_time = is_local_time
        if time_zone_hint:
            date_time.time_zone_hint = time_zone_hint

        return date_time
