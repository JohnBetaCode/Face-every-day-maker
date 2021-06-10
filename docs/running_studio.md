    (every_day_studio_FACE_CORRECTION:1899): Gdk-ERROR **: 13:12:10.769: The program 'every_day_studio_FACE_CORRECTION' received an X Window System error.
    This probably reflects a bug in the program.
    The error was 'BadAccess (attempt to access private resource denied)'.
    (Details: serial 370 error_code 10 request_code 130 (MIT-SHM) minor_code 1)
    (Note to programmers: normally, X errors are reported asynchronously;
    that is, you will receive the error a while after causing it.
    To debug your program, run it with the GDK_SYNCHRONIZE environment
    variable to change this behavior. You can then get a meaningful
    backtrace from your debugger if you break on the gdk_x_error() function.)
    make_video.sh: line 22:  1899 Trace/breakpoint trap   (core dumped) python3 "${PWD%}/dev_ws/src/everyday_studio/every_day_maker.py"