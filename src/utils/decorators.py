"""
decorators.py

Contains the decorators used in the application.
"""

#-------------------------------------------------------------------#

import functools
import sys

#-------------------------------------------------------------------#


def setup_service(func):
    """
    Setups to the service when its setup method is done.
    This way, the application will try to connect to the service safely.
    """
    max_attempts = 5
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        class_name = args[0].__class__.__name__ # Get the name of the service
        loggers = args[0].loggers
        attempt = 1
        while attempt <= max_attempts:
            loggers.log.debug(f"Setup {class_name} (attempt {attempt})")
            if result := func(*args, **kwargs):
                return result
            attempt += 1
        loggers.log.debug(f"Unable to setup {class_name}.")
        sys.exit(1)
    return wrapper

def close_service(func):
    """
    Close the connection of the service when its closing method is done.
    """
    max_attempts = 5
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        class_name = args[0].__class__.__name__
        loggers = args[0].loggers
        attempt = 1
        while attempt <= max_attempts:
            loggers.log.debug(f"Closing connection of {class_name} (attempt {attempt})...")
            if result := func(*args, **kwargs):
                return result
            attempt += 1
        loggers.log.debug("Failed to close connection")
        return None
    return wrapper
