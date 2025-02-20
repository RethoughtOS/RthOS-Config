import curses
from utils import show_message, draw_border

def repair_menu(stdscr):
    options = ["Online Sync", "Reinstall Packages", "Reset Configurations", "Back"]
    current_row = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        draw_border(stdscr)

        stdscr.addstr(1, w // 2 - len("Repair Options") // 2, "Repair Options", curses.color_pair(5))

        for idx, option in enumerate(options):
            x = 4
            y = 4 + idx

            if idx == current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, option, curses.color_pair(1))
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, option, curses.color_pair(5))

        hints = "[↑/↓] Navigate   [Enter] Select   [q] Quit"
        stdscr.attron(curses.color_pair(2))
        stdscr.addstr(h - 2, w // 2 - len(hints) // 2, hints)
        stdscr.attroff(curses.color_pair(2))

        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(options) - 1:
            current_row += 1
        elif key in [curses.KEY_ENTER, 10, 13]:
            if options[current_row] == "Back":
                break
            else:
                show_message(stdscr, f"{options[current_row]} coming soon!")

        stdscr.refresh()