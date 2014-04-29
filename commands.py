# coding=UTF-8
import curses
import locale
import sys
import time
locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

if sys.version_info.major < 3:
    PY2 = True
else:
    PY2 = False

class AddCharCommand(object):
    def __init__(self, window, line_start, y, x, character):
        """
        Command class for adding the specified character, to the specified
        window, at the specified coordinates.
        """
        self.window = window
        self.line_start = line_start
        self.y = int(y)
        self.x = int(x)
        self.character = character

    def write(self):
        self.window.addch(self.y, self.x, self.character)

    def delete(self):
        """
        Erase characters usually print two characters to the curses window.
        As such both the character at these coordinates and the one next to it
        (that is the one self.x + 1) must be replaced with the a blank space.
        Move to cursor the original coordinates when done.
        """
        for i in range(2):
            self.window.addch(self.y, self.x + i, ord(' '))
        self.window.move(self.y, self.x)

def main(screen):
    maxy, maxx = screen.getmaxyx()
    q = 0
    commands = list()
    x = 0
    erasecode = ord(curses.erasechar())
    getch = screen.getch if PY2 else screen.get_wch
    while q != 27:
        q = getch()
        if not PY2:
            keycode = ord(q)
        else:
            keycode = q
        if keycode == erasecode:
            command = commands.pop(-1).delete()
            x -= 1
            continue
        command = AddCharCommand(screen, 0, maxy/2, x, q)
        commands.append(command)
        command.write()
        x += 1

curses.wrapper(main)
