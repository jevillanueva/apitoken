import time


def current() -> int:
    """Return the current time in milliseconds since the epoch.

    Returns:
        int: Current time in milliseconds
    """
    return int(round(time.time() * 1000))
