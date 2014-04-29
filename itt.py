import curses
import time
import json
import random
import threading
from unidecode import unidecode

class ImperialTrainer(object):
    def __init__(self, screen):
        self.screen = screen
        self.y, self.x = self.screen.getmaxyx()
        self.brutal = 0
        self.mostcommon = 0
        self.force_game_end = None
        try:
            curses.curs_set(0)
        except:
            pass
        try:
            with open('data.json') as f:
                self.quotes = json.load(f)
        except IOError:
            curses.endwin()
            print 'No data file found, please recheck that you have .data.json\
                    in the folder.'
            exit()

    def _paint_menu(self):
        lines = ['Welcome to Imperial Typing Trainer',
                    '1. Start a normal game',
                    '2. Start a Force game',
                    '3. Graphs',
                    '4. Add Quotes',]

        x = (self.x - len(lines[1])) / 2
        self.screen.addstr(self.y / 2 - 3, (self.x - len(lines[0])) / 2, lines[0])
        self.screen.addstr(self.y / 2 - 1, x, lines[1])
        self.screen.addstr(self.y / 2, x, lines[2])
        self.screen.addstr(self.y / 2 + 1, x, lines[3])
        self.screen.addstr(self.y / 2 + 2, x, lines[4])
        self._paint_modes()

    def _toggle_mode(self, mode):
        """
        Toggles the instance variables self.brutal and self.mostcommon
        If the mode argument is 0, it means we want to toggle self.brutal
        If the mode argument is 1, it means we want to toggle self.mostcommon
        Any other values will result in the function returning without doing
        anything.
        """

        if mode == 0:
            self.brutal = (self.brutal + 1) % 2
        elif mode == 1:
            self.mostcommon = (self.mostcommon + 1) % 2
        else:
            return

        self._paint_modes()

    def _paint_modes(self):
        brutal = '(B)rutal Mode: %s' % ('On ' if self.brutal else 'Off')
        mcw = '(M)ost Common Words: %s' % ('On ' if self.mostcommon else 'Off')
        self.screen.addstr(self.y - 2, 2, brutal)
        self.screen.addstr(self.y - 2, self.x - len(mcw) - 2, mcw)

    def main(self):
        self._paint_menu()
        q = 0
        while True:
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
                self.normal()
            elif q == ord('2'):
                self.force()
            elif q == ord('b') or q == ord('B'):
                self._toggle_mode(0)
            elif q == ord('m') or q == ord('M'):
                self._toggle_mode(1)
            elif q == 27:
                with open('data.json', 'w') as f:
                    json.dump(self.quotes, f, indent=4)
                exit()

    def _split_quote(self, quote):
        length = 0
        parts = [[]]
        words = quote.split()
        limit = 80 if self.x > 100 else self.x - 15

        for word in words:
            if length + len(word) > limit:
                parts.append([word])
                length = len(word) + 1
            else:
                parts[-1].append(word)
                length += len(word) + 1

        substrings = [' '.join(part) for part in parts]

        return substrings, limit

    def normal(self):
        q = 0
        while True:
            if q == -1:
                return
            elif q == 0:
                r = random.randint(0, len(self.quotes) - 1)
                quote = unidecode(self.quotes[r][0])
                q = self._normal_logic(quote, r)
            elif q == 1:
                q = self._normal_logic(quote, r)

    def _normal_logic(self, quote, quote_id):
        curses.curs_set(1)
        curses.echo()
        self.screen.clear()

        partsIndex = 0
        currentChar = 0
        started = 0
        mistakes = 0
        lastPart = 0
        escaped = False

        substrings, limit = self._split_quote(quote)

        # x holds our current position
        # startX holds the position where we want to return to after a new
        # substring has been printed to the screen.
        startX = 2 if self.x == 80 else (self.x - limit) / 2
        x = 2 if self.x == 80 else (self.x - limit) / 2

        substring = substrings[partsIndex] + ' '
        if len(substrings) > 1:
            nextWord = substrings[partsIndex + 1].split(' ', 1)[0]
        else:
            nextWord = ''
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
                currentChar, x = self._delete(x, startX, substring, currentChar)
                
            elif q == curses.KEY_RESIZE:
                return _resize_handler()
            else:
                self.screen.addch(self.y / 2, x, q, curses.color_pair(0))
                if q != ord(substring[currentChar]): # Mistake happened
                    curses.beep()
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

        if not escaped:
            accuracy = self._show_result_screen(quote, now, mistakes, quote_id)
            while True:
                a = self.screen.getch()
                if a == 27 or a == ord('x') or a == ord('X'):
                    return self._exit_game()
                elif a == ord('n') or a == ord('N'):
                    if self.brutal and accuracy > 2:
                        return 1
                    else:
                        return 0
                elif a == ord('s') or a == ord('S'):
                    if self.brutal and accuracy > 2:
                        continue
                    else:
                        return 1
                elif a == curses.KEY_RESIZE:
                    self.y, self.x = self.screen.getmaxyx()
                    return self._exit_game()

        else:
            return self._exit_game()

    def force(self):
        q = 0
        while True:
            if q == -1:
                return
            elif q == 0:
                r = random.randint(0, len(self.quotes) - 1)
                quote = unidecode(self.quotes[r][0])
                q = self._force_logic(quote, r)
            elif q == 1:
                q = self._force_logic(quote, r)

    def _force_logic(self, quote, quote_id, wpm=60):
        curses.curs_set(0)
        curses.noecho()
        self.screen.nodelay(1)
        self.screen.clear()
        self.force_game_end = False

        partsIndex = 0
        currentChar = 0
        userCurrentChar = 0
        userX = 0
        started = 0
        mistakes = 0
        lastPart = 0

        quote_thread = threading.Thread(target=self._force_thread, args=(quote,))
        quote_thread.daemon = True

        substrings, limit = self._split_quote(quote)

        startX = 2 if self.x == 80 else (self.x - limit) / 2
        x = 2 if self.x == 80 else (self.x - limit) / 2
        userX = startX

        substring = substrings[partsIndex] + ' '
        if len(substrings) > 1:
            nextWord = substrings[partsIndex + 1].split(' ', 1)[0]
        else:
            nextWord = ''
        self.screen.addstr(self.y / 2, startX, substring + nextWord)
        self.screen.move(self.y / 2 + 1, startX)

        q = -1
        typedChars = 0

        while True:
            if self.force_game_end or typedChars == len(quote):
                break
            q = self.screen.getch()

            if q != -1 and not started:
                started = 1
                end = quote_thread.start()
                now = time.time()

            if q == 27:
                self.force_game_end = True
                break
            elif q == 127 or q == 263:
                if x == startX:
                    self.screen.addch(self.y / 2 + 1, x - 1, ord(' '))
                    self.screen.addch(self.y / 2 + 1, x, ord(' '))
                    self.screen.addch(self.y / 2 + 1, x + 1, ord(' '))
                    self.screen.move(self.y / 2 + 1, x)
                    continue
                self.screen.addch(self.y / 2 + 1, x - 1, ord(' '))
                self.screen.addch(self.y / 2 + 1, x, ord(' ' ))
                self.screen.addch(self.y / 2 + 1, x + 1, ord(' '))
                self.screen.move(self.y / 2 + 1, x - 1)
                self.screen.refresh()
                typedChars -= 1
                userCurrentChar -= 1
                userX -= 1
            elif q == curses.KEY_RESIZE:
                self.y, self.x = self.screen.getmaxyx()
                return self._exit_game()
            elif q != -1:
                self.screen.move(self.y / 2 + 1, userX)
                self.screen.addch(self.y / 2 + 1, userX, q)
                typedChars += 1
                userX += 1
                userCurrentChar += 1

        accuracy = self._show_result_screen(quote, now, 0, quote_id)
        while True:
            a = self.screen.getch()
            if a == 27 or a == ord('x') or a == ord('X'):
                return self._exit_game()
            elif a == ord('n') or a == ord('N'):
                return 0
            elif a == ord('s') or a == ord('S'):
                return 1
            elif a == curses.KEY_RESIZE:
                self.y, self.x = self.screen.getmaxyx()
                return self._exit_game()

    def _force_thread(self, quote):
        partsIndex = 0
        currentChar = 0
        lastPart = 0

        substrings, limit = self._split_quote(quote)

        startX = 2 if self.x == 80 else (self.x - limit) / 2
        x = startX

        substring = substrings[partsIndex] + ' '

        if len(substrings) > 1:
            nextWord = substrings[partsIndex + 1].split(' ', 1)[0]
        else:
            nextWord = ''

        #self.screen.addstr(self.y / 2, startX, substring + nextWord)
        #self.screen.move(self.y / 2 + 1, startX)

        while not self.force_game_end:
            if partsIndex + 1 == len(substrings):
                lastPart = 1
            if lastPart and currentChar == len(substring):
                self.force_game_end = True
                return
            elif currentChar == len(substring):
                partsIndex += 1
                substring = substrings[partsIndex] + ' '
                if partsIndex + 1 == len(substrings):
                    nextWord = ''
                    substring = substring[:-1]
                else:
                    nextWord = substrings[partsIndex + 1].split(' ', 1)[0]
                self.screen.addstr(self.y / 2, startX, ' ' * (self.x - startX - 1))
                self.screen.addstr(self.y / 2 + 1, startX, ' ' * (self.x - startX -1))
                self.screen.addstr(self.y / 2, startX, substring + nextWord)
                x = startX
                currentChar = 0

            time.sleep(12.0 / 100)
            self.screen.addch(self.y / 2, startX + currentChar, ' ')
            self.screen.refresh()
            currentChar += 1

    def _exit_game(self):
        curses.curs_set(0)
        curses.noecho()
        self.screen.clear()
        self._paint_menu()
        return -1

    def _show_result_screen(self, quote, start_time, mistakes, quote_id):
        """
        Display the results of the current game
        """

        self.screen.clear()
        curses.curs_set(0)
        curses.noecho()

        elapsed = time.time() - start_time
        wpm = len(quote) / float(elapsed) * 12
        accuracy = float(mistakes) / len(quote) * 100
        if not (accuracy > 40):
            self._save_current_game_results(quote_id, wpm, accuracy)
        a = 'Your WPM  is %5.2f' % wpm
        b = 'Your accuracy is %{0:4.2f}'.format(100 - accuracy)
        if self.brutal and accuracy > 2:
            c = '(N)ew Game        E(x)it to Menu'
        else:
            c = '(N)ew Game        (S)ame Quote       E(x)it to Menu'
        self.screen.addstr(self.y / 2, (self.x - len(a)) / 2, a)
        self.screen.addstr(self.y / 2 + 1, (self.x - len(b)) / 2, b)
        self.screen.addstr(self.y / 2 + 4, (self.x - len(c)) / 2, c)
        self._paint_modes()

        return accuracy

    def _save_current_game_results(self, quote_id, wpm, accuracy):
        self.quotes[quote_id][1]['past_acc'].append(accuracy)
        self.quotes[quote_id][1]['past_wpm'].append(wpm)

    def _resize_handler(self):
        """Updates the screen size instance variables and exits the current
        game and returns to the main menu."""
        self.y, self.x = self.screen.getmaxyx()
        return self._exit_game()

    def _delete(self, currentX, startPosition, substring, currentChar):
        """Handles the deleting of characters when the user deletes a character
        with the backspace key"""

        if currentX == startPosition:
            self._delete_characters(currentX)
            self.screen.move(self.y / 2 + 1, currentX)
            return
        self._delete_characters(currentX)
        self.screen.addch(self.y / 2, startPosition + currentChar - 1,
                substring[currentChar - 1], curses.color_pair(0))
        self.screen.move(self.y / 2 + 1, currentX - 1)
        self.screen.refresh()
        return currentChar - 1, currentX - 1

    def _delete_characters(self, currentX):
        self.screen.addch(self.y / 2 + 1, currentX - 1, ord(' '))
        self.screen.addch(self.y / 2 + 1, currentX, ord(' '))
        self.screen.addch(self.y / 2 + 1, currentX + 1, ord(' '))


def entry(screen):
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_RED)
    trainer = ImperialTrainer(screen)
    trainer.main()

curses.wrapper(entry)
