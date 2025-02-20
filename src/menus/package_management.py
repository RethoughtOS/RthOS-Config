import curses
from utils import show_message, draw_border
from menus.system_updates import system_updates_menu
from menus.package_sources import package_sources_menu
from menus.additional_package_managers import additional_package_managers_menu
from menus.default_software import default_software_menu
from menus.dependencies_build_tools import dependencies_build_tools_menu
from menus.package_cache import package_cache_menu

def package_management_menu(stdscr):
    options = [
        "Systemupdates installieren", "Paketquellen verwalten (Mirrors, Repos)",
        "Zusätzliche Paketmanager verwalten (Flatpak, Snap, AppImage)",
        "Standardsoftware auswählen (Editor, Terminal, Browser)",
        "Abhängigkeiten & Build-Tools installieren", "Paketcache bereinigen", "Back"
    ]
    current_row = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        draw_border(stdscr)

        stdscr.addstr(1, w // 2 - len("Package Management") // 2, "Package Management", curses.color_pair(5))

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
            elif options[current_row] == "Systemupdates installieren":
                system_updates_menu(stdscr)
            elif options[current_row] == "Paketquellen verwalten (Mirrors, Repos)":
                package_sources_menu(stdscr)
            elif options[current_row] == "Zusätzliche Paketmanager verwalten (Flatpak, Snap, AppImage)":
                additional_package_managers_menu(stdscr)
            elif options[current_row] == "Standardsoftware auswählen (Editor, Terminal, Browser)":
                default_software_menu(stdscr)
            elif options[current_row] == "Abhängigkeiten & Build-Tools installieren":
                dependencies_build_tools_menu(stdscr)
            elif options[current_row] == "Paketcache bereinigen":
                package_cache_menu(stdscr)
            else:
                show_message(stdscr, f"{options[current_row]} coming soon!")

        stdscr.refresh()