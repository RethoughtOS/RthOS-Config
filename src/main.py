import curses
import platform
import subprocess
import re
import requests  
from menus.system_configuration import system_configuration_menu
from menus.package_management import package_management_menu
from menus.rthos_setup import rthos_setup_menu
from menus.system_info import system_info_menu

# Funktion für den Menü-Titel
def draw_menu_title(stdscr, title):
    h, w = stdscr.getmaxyx()
    stdscr.attron(curses.color_pair(2))
    stdscr.addstr(0, (w - len(title)) // 2, f" {title} ")
    stdscr.attroff(curses.color_pair(2))

# Rahmen zeichnen
def draw_border(stdscr):
    stdscr.attron(curses.color_pair(3))
    stdscr.border(0)
    stdscr.attroff(curses.color_pair(3))

# Systeminformationen abrufen
def get_system_info():
    kernel_version = platform.release()
    python_version = platform.python_version()
    rthos_framework_version = "Not found! :/"  

    def get_rthos_pulse_version():
        try:
            response = requests.get("http://127.0.0.1:8000/system/version")
            if response.status_code == 200:
                version_info = response.json()
                return version_info.get("rthos_pulse_version", "Unknown")
            else:
                return "Error"
        except requests.ConnectionError:
            return "Not running"

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
        gcc_version = extract_version(gcc_output)
    except FileNotFoundError:
        gcc_version = "not installed"

    try:
        gpp_output = subprocess.check_output(["g++", "--version"]).decode().split('\n')[0]
        gpp_version = extract_version(gpp_output)
    except FileNotFoundError:
        gpp_version = "not installed"

    compatibility = "Compatible" if arch_based else "Incompatible System"

    return {
        "Kernel": kernel_version,
        "Python": python_version,
        "GCC": f"GCC {gcc_version}",
        "G++": f"G++ {gpp_version}",
        "RthOS Framework": rthos_framework_version,
        "RthOS-Pulse Version": get_rthos_pulse_version(),
        "Compatibility": compatibility
    }

# Nachricht anzeigen mit Titel
def show_message(stdscr, title, message):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    lines = []
    for line in message.split("\n"):
        while len(line) > w - 4:
            lines.append(line[:w-4])
            line = line[w-4:]
        lines.append(line)

    max_lines = min(h - 4, len(lines))
    start_y = (h - max_lines) // 2  

    draw_border(stdscr)
    draw_menu_title(stdscr, title)  # Menü-Titel anzeigen

    for i in range(max_lines):
        stdscr.addstr(start_y + i, 2, lines[i])

    stdscr.addstr(h - 2, w // 2 - 10, "Press any key to return", curses.color_pair(5))

    stdscr.refresh()
    stdscr.getch()

# Hauptmenü anzeigen
def main_menu(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)

    current_row = 0
    menu = [
        ("System Configuration", system_configuration_menu),
        ("Package Management", package_management_menu),
        ("RthOS Setup", rthos_setup_menu),
        ("System Info", system_info_menu),
        ("Exit", None)
    ]
    system_info = get_system_info()

    min_height, min_width = 20, 80

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        stdscr.bkgd(' ', curses.color_pair(4))

        if h < min_height or w < min_width:
            error_msg = "Terminal window too small. Resize to at least 80x20."
            stdscr.addstr(h // 2, (w - len(error_msg)) // 2, error_msg, curses.A_BOLD)
            stdscr.refresh()
            stdscr.getch()
            continue

        draw_border(stdscr)
        draw_menu_title(stdscr, " RethoughtOS Configuration Tool ")

        for idx, (row, _) in enumerate(menu):
            menu_item = f"{idx + 1}. {row}"
            x = 4
            y = 4 + idx

            if idx == current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, menu_item, curses.color_pair(1))
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, menu_item, curses.color_pair(5))

        sys_info_y = 4
        sys_info_x = w - 40
        stdscr.attron(curses.color_pair(2))
        stdscr.addstr(sys_info_y - 1, sys_info_x, "System Information")
        stdscr.attroff(curses.color_pair(2))

        max_info_lines = min(h - sys_info_y - 2, len(system_info))
        for i, (key, value) in enumerate(list(system_info.items())[:max_info_lines]):
            stdscr.addstr(sys_info_y + i, sys_info_x, f"{key}: {value[:w-4]}", curses.color_pair(5))

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
            if menu[current_row][1]:
                menu[current_row][1](stdscr)  # Starte das ausgewählte Menü
            else:
                break
        elif key == ord('q'):
            break

        stdscr.refresh()

if __name__ == "__main__":
    curses.wrapper(main_menu)
