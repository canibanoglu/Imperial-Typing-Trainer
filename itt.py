import curses
import time
import signal
import subprocess

class ImperialTrainer(object):
    def __init__(self, screen):
        self.screen = screen
        self.y, self.x = self.screen.getmaxyx()
        self.brutal = 0
        self.mostcommon = 0
        try:
            curses.curs_set(0)
        except:
            pass

    def _paint_menu(self):
        lines = ['Welcome to Imperial Typing Trainer',
                    '1. Start a normal game',
                    '2. Start a Force game',
                    '3. Graphs',
                    '4. Add Quotes',
                    '(B)rutal Mode: %s' % ('On ' if self.brutal else 'Off'),
                    '(M)ost Common Words: %s' % ('On ' if self.mostcommon else 'Off')]

        x = (self.x - len(lines[1])) / 2
        self.screen.addstr(self.y / 2 - 3, (self.x - len(lines[0])) / 2, lines[0])
        self.screen.addstr(self.y / 2 - 1, x, lines[1])
        self.screen.addstr(self.y / 2, x, lines[2])
        self.screen.addstr(self.y / 2 + 1, x, lines[3])
        self.screen.addstr(self.y / 2 + 2, x, lines[4])
        self.screen.addstr(self.y - 2,  2, lines[5])
        self.screen.addstr(self.y - 2, self.x - len(lines[6]) - 2, lines[6])

    def main(self):
        self._paint_menu()
        q = 0
        while q != 27:
            if self.x < 10 or self.y < 10:
                return
            elif self.x < 80 or self.y < 24:
                self.screen.clear()
                self.screen.addstr(self.y / 2, (self.x - 7) / 2, 'RESIZE!')
                q = self.screen.getch()
                if q == 27:
                    return
                elif q in [ord(i) for i in ('1', '2', '3', '4', 'b', 'B', 'm', 'M')]:
                    continue
            else:
                q = self.screen.getch()

            if q == curses.KEY_RESIZE:
                self.y, self.x = self.screen.getmaxyx()
                if self.x >= 80 and self.y >= 24:
                    self.screen.clear()
                    self._paint_menu()
            elif q == ord('1'):
                self._normal()
            elif q == ord('b') or q == ord('B'):
                self.brutal = (self.brutal + 1) % 2
                on_off = 'On ' if self.brutal else 'Off'
                msg = '(B)rutal Mode: %s' % on_off
                self.screen.addstr(self.y - 2, 2, msg)
            elif q == ord('m') or q == ord('M'):
                self.mostcommon = (self.mostcommon + 1) % 2
                on_off = 'On ' if self.mostcommon else 'Off'
                msg = '(M)ost Common Words: %s' % on_off
                self.screen.addstr(self.y - 2, self.x - len(msg) - 2, msg)

    def _split_quote(self, quote):
        length = 0
        parts = [[]]
        words = quote.split()
        limit = 80 if self.x > 80 else self.x - 10

        for word in words:
            if length + len(word) > limit:
                parts.append([word])
                length = len(word) + 1
            else:
                parts[-1].append(word)
                length += len(word) + 1

        substrings = [' '.join(part) for part in parts]

        return substrings, limit

    def _normal(self):
        curses.curs_set(1)
        curses.echo()
        self.screen.clear()
        ### Implement random quote from database here
        message = "Many rivers to cross but I can't seem to find my way over. Wandering, I am lost as I travel along the white cliffs of Dover. Many rivers to cross and it's only my will that keeps me alive. I've been licked, washed up for years, and I merely survive because of my pride."

        partsIndex = 0
        currentChar = 0
        started = 0
        mistakes = 0
        lastPart = 0
        escaped = False

        substrings, limit = self._split_quote(message)

        # x holds our current position
        # startX holds the position where we want to return to after a new
        # substring has been printed to the screen.
        startX = 2 if self.x == 80 else (self.x - limit) / 2
        x = 2 if self.x == 80 else (self.x - limit) / 2

        substring = substrings[partsIndex] + ' '
        nextWord = substrings[partsIndex + 1].split(' ', 1)[0]
        self.screen.addstr(self.y / 2, startX, substring + nextWord)
        self.screen.move(self.y / 2 + 1, startX)
        self.screen.refresh()

        q = -1

        while True:
            # If this is the last substring and current character is the last 
            # character of that substring, it means we are done. This is not an
            # ideal solution, because the user will not have the option of
            # correcting the last character.
            if partsIndex + 1 == len(substrings): # This is the last substr
                lastPart = 1
            if lastPart and currentChar == len(substring):
                break
            elif currentChar == len(substring):
                partsIndex += 1
                substring = substrings[partsIndex] + ' '
                if partsIndex + 1 == len(substrings):
                    nextWord = ''
                    substring = substring[:-1]
                else:
                    nextWord = substrings[partsIndex + 1].split(' ', 1)[0]
                self.screen.addstr(self.y / 2, startX, ' ' * (self.x - startX - 1))
                self.screen.addstr(self.y / 2 + 1, startX, ' ' * (self.x - startX - 1))
                self.screen.addstr(self.y / 2, startX, substring + nextWord)
                self.screen.move(self.y / 2 + 1, startX)
                x = startX
                currentChar = 0
            q = self.screen.getch()

            # Start the timer if this is the first keystroke
            if not started:
                started = 1
                now = time.time()

            if q == 27:
                escaped = True
                break
            elif q == 127 or q == 263: # User is trying to delete character
                if x == startX:
                    self.screen.addch(self.y / 2 + 1, x - 1, ord(' '))
                    self.screen.addch(self.y / 2 + 1, x, ord(' '))
                    self.screen.addch(self.y / 2 + 1, x + 1, ord(' '))
                    self.screen.move(self.y / 2 + 1, x)
                    continue
                self.screen.addch(self.y / 2 + 1, x - 1, ord(' '))
                self.screen.addch(self.y / 2 + 1, x, ord(' ' ))
                self.screen.addch(self.y / 2 + 1, x + 1, ord(' '))
                self.screen.addch(self.y / 2, startX + currentChar - 1, 
                        substring[currentChar - 1], curses.color_pair(0))
                self.screen.move(self.y / 2 + 1, x - 1)
                self.screen.refresh()
                currentChar -= 1
                x -= 1
            elif q == curses.KEY_RESIZE:
                ### Do shit here
                # If the size is too small, return to the menu which will show
                # the 'RESIZE!' message
                self.y, self.x = self.screen.getmaxyx()
                return
            else:
                self.screen.addch(self.y / 2, x, q, curses.color_pair(0))
                if q != ord(substring[currentChar]): # Mistake happened
                    color = (substring[currentChar] == ' ' and 3) or 1
                    self.screen.addch(self.y / 2, startX + currentChar,
                            substring[currentChar], curses.color_pair(color))
                    self.screen.move(self.y / 2 + 1, x + 1)
                    mistakes += 1
                else:
                    self.screen.addch(self.y / 2, startX + currentChar,
                            substring[currentChar], curses.color_pair(2))
                    self.screen.move(self.y / 2 + 1, x + 1)
                self.screen.refresh()
                x += 1
                currentChar += 1

        self.screen.clear()
        curses.noecho()
        if not escaped:
            elapsed = time.time() - now
            wpm = len(message) / float(elapsed) * 12
            accuracy = float(mistakes) / len(message) * 100
            a = 'Your WPM is %5.2f' % wpm
            b = 'Your accuracy is %{0:4.2f}'.format(100 - accuracy)
            self.screen.addstr(self.y / 2, (self.x - len(a)) / 2, a)
            self.screen.addstr(self.y / 2 + 1, (self.x - len(b)) / 2, b)
            self.screen.clear()
            curses.curs_set(0)
            self._paint_menu()
        else:
            curses.curs_set(0)
            self._paint_menu()



def entry(screen):
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_RED)
    trainer = ImperialTrainer(screen)
    trainer.main()

curses.wrapper(entry)
