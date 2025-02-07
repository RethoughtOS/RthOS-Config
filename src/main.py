import curses
import platform
import subprocess
import re

# Systeminformationen abrufen
def get_system_info():
    kernel_version = platform.release()
    python_version = platform.python_version()
    rthos_framework_version = "Not found! :/"  # Beispielversion

    def extract_version(output):
        match = re.search(r'\d+(\.\d+)+', output)
        return match.group(0) if match else "Unknown"

    def check_arch_based():
        try:
            with open("/etc/os-release") as f:
                content = f.read().lower()
                if "arch" in content or "rthos" in content:
                    return True
        except FileNotFoundError:
            pass

        try:
            with open("/etc/arch-release") as f:
                return True
        except FileNotFoundError:
            pass

        try:
            subprocess.check_output(["pacman", "-V"])
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            pass

        return False

    arch_based = check_arch_based()

    try:
        gcc_output = subprocess.check_output(["gcc", "--version"]).decode().split('\n')[0]
        gcc_version = f"GCC {extract_version(gcc_output)}"
    except FileNotFoundError:
        gcc_version = "GCC not installed"

    try:
        gpp_output = subprocess.check_output(["g++", "--version"]).decode().split('\n')[0]
        gpp_version = f"G++ {extract_version(gpp_output)}"
    except FileNotFoundError:
        gpp_version = "G++ not installed"

    compatibility = "Compatible" if arch_based else "Incompatible System"

    return {
        "Kernel": kernel_version,
        "Python": python_version,
        "GCC": gcc_version,
        "G++": gpp_version,
        "RthOS Framework": rthos_framework_version,
        "Compatibility": compatibility
    }

# Nachricht anzeigen
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

# Rahmen zeichnen
def draw_border(stdscr):
    stdscr.attron(curses.color_pair(3))
    stdscr.border(0)
    stdscr.attroff(curses.color_pair(3))

# Untermenüs anzeigen
def system_configuration_menu(stdscr):
    options = ["Wi-Fi Options", "Bluetooth Options", "Display Settings", "Back"]
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

# RthOS Setup Menü anzeigen
def rthos_setup_menu(stdscr):
    options = ["Install", "Repair", "Update", "Back"]
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

        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(options) - 1:
            current_row += 1
        elif key in [curses.KEY_ENTER, 10, 13]:
            if options[current_row] == "Back":
                break
            elif options[current_row] == "Repair":
                repair_menu(stdscr)
            else:
                show_confirmation(stdscr, f"{options[current_row]} process will start. Proceed?")

        stdscr.refresh()

# Reparaturmenü anzeigen
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

        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(options) - 1:
            current_row += 1
        elif key in [curses.KEY_ENTER, 10, 13]:
            if options[current_row] == "Back":
                break
            else:
                show_confirmation(stdscr, f"{options[current_row]} process will start. Proceed?")

        stdscr.refresh()

# Bestätigungsnachricht anzeigen
def show_confirmation(stdscr, message):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    x = w // 2 - len(message) // 2
    y = h // 2
    draw_border(stdscr)
    stdscr.addstr(y, x, message, curses.color_pair(5))
    stdscr.addstr(y + 2, x, "Press [y] to confirm or any other key to cancel", curses.color_pair(5))
    stdscr.refresh()

    key = stdscr.getch()
    if key == ord('y'):
        show_message(stdscr, "Action confirmed!")
    else:
        show_message(stdscr, "Action canceled!")

# Hauptmenü anzeigen
def main_menu(stdscr):
    curses.curs_set(0)  # Cursor ausblenden
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_MAGENTA)    # Schwarzer Text auf Lila für Auswahl
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)    # Lila für Titel und Hints
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)    # Lila Rahmen
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLACK)      # Dunkelgrauer Hintergrund
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)      # Weißer Text für Menüpunkte

    current_row = 0
    menu = ["System Configuration", "Package Management", "RthOS Setup", "Exit"]
    system_info = get_system_info()

    min_height, min_width = 20, 80  # Erhöhte Mindestgröße für bessere Darstellung

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        # Hintergrundfarbe
        stdscr.bkgd(' ', curses.color_pair(4))

        # Überprüfen, ob das Terminal groß genug ist
        if h < min_height or w < min_width:
            error_msg = "Terminal window too small. Resize to at least 80x20."
            stdscr.addstr(h // 2, (w - len(error_msg)) // 2, error_msg, curses.A_BOLD)
            stdscr.refresh()
            stdscr.getch()
            continue

        # Rahmen zeichnen
        draw_border(stdscr)

        # Titel
        title = "RethoughtOS (RthOS) Configuration Tool"
        stdscr.attron(curses.color_pair(2))
        stdscr.addstr(1, w // 2 - len(title) // 2, title)
        stdscr.attroff(curses.color_pair(2))

        # Menü anzeigen
        for idx, row in enumerate(menu):
            menu_item = f"{idx + 1}. {row}"
            x = 4
            y = 4 + idx

            if idx == current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, menu_item, curses.color_pair(1))
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, menu_item, curses.color_pair(5))

        # Systeminformationen anzeigen
        sys_info_y = 4
        sys_info_x = w - 40
        stdscr.attron(curses.color_pair(2))
        stdscr.addstr(sys_info_y - 1, sys_info_x, "System Information")
        stdscr.attroff(curses.color_pair(2))

        for i, (key, value) in enumerate(system_info.items()):
            stdscr.addstr(sys_info_y + i, sys_info_x, f"{key}: {value}", curses.color_pair(5))

        # Hints unten
        hints = "[↑/↓] Navigate   [Enter] Select   [q] Quit"
        stdscr.attron(curses.color_pair(2))
        stdscr.addstr(h - 2, w // 2 - len(hints) // 2, hints)
        stdscr.attroff(curses.color_pair(2))

        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key in [curses.KEY_ENTER, 10, 13]:
            if current_row == 0:
                system_configuration_menu(stdscr)
            elif current_row == 1:
                show_message(stdscr, "Package Management coming soon!")
            elif current_row == 2:
                rthos_setup_menu(stdscr)
            elif current_row == 3:
                break  # Exit
        elif key == ord('q'):
            break  # Quit mit 'q'

        stdscr.refresh()

if __name__ == "__main__":
    curses.wrapper(main_menu)