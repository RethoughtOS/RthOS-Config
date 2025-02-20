import curses
from utils import show_message, draw_border
from menus.install import install_menu
from menus.repair import repair_menu
from menus.update import update_menu
from menus.diagnostics import diagnostics_menu
from menus.custom_profiles import custom_profiles_menu
from menus.framework import framework_menu

def rthos_setup_menu(stdscr):
    options = [
        "Install", "Repair", "Update", "Diagnose & Kompatibilitätsprüfung",
        "Benutzerdefinierte RthOS-Profile laden", "RthOS Framework installieren/aktualisieren", "Back"
    ]
    current_row = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        draw_border(stdscr)

        stdscr.addstr(1, w // 2 - len("RthOS Setup") // 2, "RthOS Setup", curses.color_pair(5))

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
            elif options[current_row] == "Install":
                install_menu(stdscr)
            elif options[current_row] == "Repair":
                repair_menu(stdscr)
            elif options[current_row] == "Update":
                update_menu(stdscr)
            elif options[current_row] == "Diagnose & Kompatibilitätsprüfung":
                diagnostics_menu(stdscr)
            elif options[current_row] == "Benutzerdefinierte RthOS-Profile laden":
                custom_profiles_menu(stdscr)
            elif options[current_row] == "RthOS Framework installieren/aktualisieren":
                framework_menu(stdscr)
            else:
                show_message(stdscr, f"{options[current_row]} coming soon!")

        stdscr.refresh()