import os
import sys
import traceback

from .utils import printlog


def try_catch_log(show_traceback):
    """! Decorator to run a function within a try-catch block and
    print the result in case of an error. By default it will also
    print the full traceback. Usage: @try_catch_log on any function
    or method.

    If you don't want to show the traceback use it with:
    @try_catch_log(show_traceback=False)

    @param show_traceback (bool) Whether to show the full traceback
        if it crashes

    @return function Function to run
    """
    # if it is callable, means we are using @try_catch_log without argument,
    # meaning the argument show_traceback is already the function to decorate
    if callable(show_traceback):

        def wrapper_fun(*args, **kwargs):
            function = show_traceback
            try:
                function(*args, **kwargs)
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                # Get next traceback because this one belongs to this wrapper
                exc_tb = exc_tb.tb_next

                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                file = os.path.splitext(fname)[0].upper()

                printlog(
                    msg=f"Exception error: {e}, {exc_type}, {fname}, {exc_tb.tb_lineno}",
                    msg_type="ERROR",
                    caller=function.__name__.upper(),
                    file=file,
                )
                traceback.print_exc()

        return wrapper_fun
    # Else, show_traceback is the argument, @try_catch_log(True) for example
    else:

        def decorator(function):
            def wrapper_fun(*args, **kwargs):
                try:
                    function(*args, **kwargs)
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    # Get next traceback because this one belongs to this wrapper
                    exc_tb = exc_tb.tb_next

                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    file = os.path.splitext(fname)[0].upper()

                    printlog(
                        msg=f"Exception error: {e}, {exc_type}, {fname}, {exc_tb.tb_lineno}",
                        msg_type="ERROR",
                        caller=function.__name__.upper(),
                        file=file,
                    )
                    if show_traceback:
                        traceback.print_exc()

            return wrapper_fun

        return decorator
