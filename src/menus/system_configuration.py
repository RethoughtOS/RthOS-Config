import curses
from utils import show_message, draw_border
from menus.hostname import hostname_menu
from menus.timezone import timezone_menu
from menus.language_keyboard import language_keyboard_menu
from menus.user_management import user_management_menu
from menus.network_configuration import network_configuration_menu
from menus.system_services import system_services_menu
from menus.secure_boot import secure_boot_menu
from menus.rthos_pulse import rthos_pulse_menu
from menus.factory_reset import factory_reset_menu

def system_configuration_menu(stdscr):
    options = [
        "Hostname ändern", "Zeitzone setzen", "Sprache & Tastatur",
        "Benutzer verwalten", "Netzwerk-Konfiguration (LAN/WLAN)",
        "Systemdienste verwalten (Starten/Stoppen)", "Secure Boot verwalten (Falls unterstützt)",
        "RthOS-Pulse aktivieren/deaktivieren", "Werkseinstellungen zurücksetzen", "Back"
    ]
    current_row = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        draw_border(stdscr)

        stdscr.addstr(1, w // 2 - len("System Configuration") // 2, "System Configuration", curses.color_pair(5))

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
            elif options[current_row] == "Hostname ändern":
                hostname_menu(stdscr)
            elif options[current_row] == "Zeitzone setzen":
                timezone_menu(stdscr)
            elif options[current_row] == "Sprache & Tastatur":
                language_keyboard_menu(stdscr)
            elif options[current_row] == "Benutzer verwalten":
                user_management_menu(stdscr)
            elif options[current_row] == "Netzwerk-Konfiguration (LAN/WLAN)":
                network_configuration_menu(stdscr)
            elif options[current_row] == "Systemdienste verwalten (Starten/Stoppen)":
                system_services_menu(stdscr)
            elif options[current_row] == "Secure Boot verwalten (Falls unterstützt)":
                secure_boot_menu(stdscr)
            elif options[current_row] == "RthOS-Pulse aktivieren/deaktivieren":
                rthos_pulse_menu(stdscr)
            elif options[current_row] == "Werkseinstellungen zurücksetzen":
                factory_reset_menu(stdscr)
            else:
                show_message(stdscr, f"{options[current_row]} coming soon!")

        stdscr.refresh()