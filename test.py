import curses
from curses import wrapper
from curses.textpad import rectangle
from time import sleep


def draw_messages(scr: curses.window, messages: list[str]):
    for i, message in enumerate(messages):
        scr.addstr(i + 1, 1, message)


def main(scr: curses.window):
    text = ""
    messages: list[str] = []
    scr.nodelay(True)
    window_size = (curses.LINES - 1, curses.COLS - 1)

    while True:
        try:
            key = scr.getch()
        except curses.error:
            key = None
        if 31 < key and key < 127:
            text += chr(key)
        if key == 127:
            if len(text) > 0:
                text = text[:-1]
        if key == 27:
            break
        if key == 10:
            messages.append(text)
            text = ""

        scr.clear()
        draw_messages(scr, messages)
        rectangle(scr, 0, 0, window_size[0] - 4, window_size[1])
        rectangle(scr, window_size[0] - 3, 0,
                  window_size[0] - 1, window_size[1])
        scr.addstr(window_size[0] - 2, 2, text)
        scr.refresh()
        sleep(0.02)
    scr.clear()


wrapper(main)
