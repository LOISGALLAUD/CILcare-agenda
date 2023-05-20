"""
decorators.py

Contains the decorators used in the application.
"""

#-------------------------------------------------------------------#

import functools
import sys

#-------------------------------------------------------------------#

def setup_service(max_attempts:int=5):
    """
    Setups to the service when its setup method is done.
    This way, the application will try to connect to the service safely.
    """
    def decorator_func(func:callable) -> callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> None:
            class_name = args[0].__class__.__name__ # Get the name of the service
            loggers = args[0].loggers
            attempt = 1
            while attempt <= max_attempts:
                loggers.log.debug(f"Setup {class_name} (attempt {attempt})")
                try:
                    func(*args, **kwargs)
                except Exception as setup_error:
                    loggers.log.debug(f"Unable to setup {class_name}: {type(setup_error).__name__}")
                attempt += 1
            loggers.log.fatal(f"Can't setup {class_name}. Exiting the application.")
            print("CILcare agenda stopped.")
            sys.exit(1)
        return wrapper
    return decorator_func

def close_service(max_attempts:int=5):
    """
    Close the connection of the service when its closing method is done.
    This way, the application will try to close the connection to the service safely.
    """
    def decorator_func(func:callable) -> callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> None:
            class_name = args[0].__class__.__name__
            loggers = args[0].loggers
            attempt = 1
            while attempt <= max_attempts:
                loggers.log.debug(f"Closing {class_name} (attempt {attempt})...")
                if result := func(*args, **kwargs):
                    return result
                attempt += 1
            loggers.log.debug("Failed to close service")
            return None
        return wrapper
    return decorator_func
