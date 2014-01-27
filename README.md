## Imperial Typing Trainer

A simple Python program which is intended for those who wish to improve their
typing speed. Think of it as TypeRacer for your terminal.

Currently, only English is supported as the whole thing is written with ``curses``.

### Features

#### Normal and Brutal Modes
You can train in two different modes: normal and brutal. The normal mode is just your
run-of-the-mill typing game. You type the string shown to you and after you're done
you're shown your typing speed and your accuracy. If you wish to continue playing,
you're shown a random string again and the same thing continues to happen as long as
you wish to continue playing.

On the other hand, brutal mode won't let you type another string unless you manage
to type the current string with at least *98%* accuracy. As long as you fail to meet
that level of accuracy, you will be shown the same string as long as you continue playing.

Needless to say, you can of course change the mode in the main menu but if you wish
to improve your typing speed I really urge you to give the brutal mode a try. I found
that accuracy helps you more than anything when you're trying to speed up your typing
speed.

#### Most Common Words
If you wish to practice the most common words in the English language, you can toggle
the ``MCW`` option in the main menu and you will be typing a random selection from the
most common words in the English language.

#### Force Game
In the Force Game, the string that you should be typing will not be waiting for you to
type at your leisure. It will scroll at a speed that you can set before starting the game
and you will have no chance of seeing a word once it disappears from the screen. Great
for pushing yourself. May the Force be with you! (Yeah, I'm a Star Wars geek, and I
take a perverted pleasure from stuff like this.)

#### Graphs!
If you want to see how you have progressed since you have started using Imperial Typing
Tutor, you can choose the graph option from the main menu and you will see your 
WPM and accuracy stats plotted against time. 

I also plan to implement a way of seeing how you have been doing for individual strings
from the database in the future.

Note that graphs require you to have ``matplotlib`` on your computer.

#### Quotes Database
Imperial Typing Tutor comes with a set of quotes so you can start training right away
but if in the future you find that you'd rather add your own quotes, you can do so
in the main menu. Remember: Only English is supported!

### FAQ
#### Why even write such a program?
Well, ever since I saw a gentlemen who could touch type on a computer when I was 9 years
old, I wanted to type without looking at the keyboard. And I wanted to type fast. I don't
know why I care, but I do. Getting to 130 WPM is one of my 2014 resolutions and 
I just wanted to write something that has everything I want.

#### Your code sucks!
Yes, I know. I try to get better though. Would love some help if you have some free time.

#### Why no tests?
Frankly, I don't know how to unit test a curses program. I would appreciate pointers
and add unit tests as I learn how. If this makes you feel better, I did spent
countless hours in front of this program.

#### What's up with the "You need to resize your terminal window!" message?
Well, the program will run without a hich if your current terminal window has a
size of 25x80, which is the standard. Anything smaller is really crampy. I was thinking
of having the program automatically resize the window but that has turned out to be
a nightmarish experience. Kindly resize your terminal window and all will be well.
Truly, this is not the size you're looking for.

#### I have a suggestion! What should I do?
Create an issue, shoot me an email, fork and submit a PR, I don't care how you get in touch
but I would LOVE to hear your suggestions!

#### I have a fix! What should I do?
Please see the above answer.
