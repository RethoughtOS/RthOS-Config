import curses

def show_message(stdscr, message):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    x = w // 2 - len(message) // 2
    y = h // 2
    draw_border(stdscr)
    stdscr.addstr(y, x, message, curses.color_pair(5))
    stdscr.addstr(y + 2, x, "Press any key to return", curses.color_pair(5))
    stdscr.refresh()
    stdscr.getch()

def draw_border(stdscr):
    stdscr.attron(curses.color_pair(3))
    stdscr.border(0)
    stdscr.attroff(curses.color_pair(3))