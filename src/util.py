"""Utilities"""


class Singleton(type):
    """Singleton metaclass.

    Stores instances on the class attribute. Instantiations using two
    different arguments will result in storing a different object. This
    allows us, for example, to use a singleton for a Redis client that
    will return the correct client for particular connection data.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Check if the instance has been created with arguments.

        This is useful if we need to instantiate different redis clients.
        """
        key = (args, tuple(sorted(kwargs.items())))
        if cls not in cls._instances:
            cls._instances[cls] = {}
        if key not in cls._instances[cls]:
            cls._instances[cls][key] = super(Singleton, cls).__call__(
                *args, **kwargs
            )
        return cls._instances[cls][key]
