from functools import wraps


def argument_is_one_of(*allowed_values):
    def property_type_decorator(func):
        @wraps(func)
        def wrapper(self, value):
            if value not in allowed_values:
                error = "Invalid argument: {0}. {1} must be one of {2}."
                msg = error.format(value, func.__name__, allowed_values)
                raise ValueError(error)
            return func(self, value)

        return wrapper

    return property_type_decorator
