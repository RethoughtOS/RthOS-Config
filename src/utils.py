import curses

def show_message(stdscr, title, message):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    # Zeichne den Rahmen
    draw_border(stdscr)

    # Menü-Titel oben zentriert anzeigen
    stdscr.attron(curses.color_pair(2))
    stdscr.addstr(0, (w - len(title)) // 2, f" {title} ")
    stdscr.attroff(curses.color_pair(2))

    # Nachricht mittig platzieren
    x = max(2, (w // 2) - (len(message) // 2))
    y = h // 2

    stdscr.addstr(y, x, message, curses.color_pair(5))
    stdscr.addstr(y + 2, x, "Press any key to return", curses.color_pair(5))

    stdscr.refresh()
    stdscr.getch()

def draw_border(stdscr):
    stdscr.attron(curses.color_pair(3))
    stdscr.border(0)
    stdscr.attroff(curses.color_pair(3))
