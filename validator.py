"""Various validators"""


def validate_integer(
        arg_name, arg_value, min_value=None, max_value=None,
        custom_min_message=None, custom_max_message=None
):
    """Validates that `arg_value` is an integer, and optionally falls within specific
    bounds.
    A custom override error message can also be provided when min/max bounds are exceeded.

    Args:
        arg_name (str): the name of the argument (used for error messages)
        arg_value (obj): the value being validated
        min_value (int): optional,specifies the minimum allowed value
        max_value (int): optional,specifies maximum allowed value
        custom_min_message: optional,custom error message when value is less than min_value
        custom_max_message: optional,custom error message when value is greater than max_value

    Returns:
        None: no exception is raised if validation passes

    Raises:
        TypeError: if `arg_value` is not an integer
        ValueError: if `arg_value` doesn't satisfy bounds
    """
    if not isinstance(arg_value, int):
        raise TypeError(f'{arg_name} is not an integer')

    if min_value is not None and arg_value < min_value:
        if custom_min_message is not None:
            raise ValueError(custom_min_message)
        raise ValueError(f'{arg_name}' f' is less than {min_value}')
    if max_value is not None and arg_value > max_value:
        if custom_max_message is not None:
            raise ValueError(custom_max_message)
        raise ValueError(f'{arg_name}' f' is greater than {max_value}')