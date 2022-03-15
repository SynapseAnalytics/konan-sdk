from enum import Enum
from typing import Type


def string_to_konan_enum(
    enum_string: str,
    enum_class: Type,
) -> Enum:
    """Create an enum object from enum_string.
    If the enum_class does NOT have a corresponding enum_string, then return enum_class.Other
    enum_class must include the Other type

    :param enum_string: string of the num type
    :type enum_string: str
    :param enum_class: enum class type
    :type enum_class: Type
    :return: corresponding enum_class object, or enum_class.Other
    :rtype: Enum
    """
    if enum_string in [e.value for e in enum_class]:
        return enum_class(enum_string)
    else:
        return enum_class.Other
