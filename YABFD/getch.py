# From http://code.activestate.com/recipes/134892/
# "getch()-like unbuffered character reading from stdin
#  on both Windows and Unix (Python recipe)"
# modified to be a single class

import os

if os.name == "nt":
    import msvcrt
else:
    import sys, tty, termios


class _Getch:
    """Gets a single character from standard input.  Does not echo to the
    screen."""

    win: bool = False

    def __init__(self):
        if os.name == "nt":
            self.win = True
        else:
            self.win = False

    def __call__(self):
        if self.win:
            return msvcrt.getch()
        else:
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch


getch = _Getch()
