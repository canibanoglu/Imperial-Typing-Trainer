import curses
screen = curses.initscr()
screen.addstr(2, 2, str(curses.erasechar()))
screen.getch()
curses.endwin()
