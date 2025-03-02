import curses
import subprocess
from utils import show_message, draw_border

def get_battery_info():
    try:
        battery_devices = subprocess.check_output(["upower", "-e"]).decode().split("\n")
        battery_path = next((dev for dev in battery_devices if "battery" in dev), None)

        if not battery_path:
            return ["Keine Batterie gefunden."]

        battery_info = subprocess.check_output(["upower", "-i", battery_path]).decode()
        info_dict = {
            "Ladezyklen": "charge-cycles",
            "Max. Kapazität": "energy-full-design",
            "Derzeitige Kapazität": "energy-full",
            "Kapazität (%)": "capacity"
        }

        output = []
        for key, keyword in info_dict.items():
            value = None
            for line in battery_info.split("\n"):
                if keyword in line.lower():
                    value = line.split(":")[-1].strip()
                    break
            output.append(f"{key}: {value if value else 'Nicht verfügbar'}")

        return output

    except subprocess.CalledProcessError as e:
        return [f"Fehler beim Abrufen der Batterieinformationen:\n{e}"]

def battery_menu(stdscr):
    stdscr.clear()
    draw_border(stdscr)

    # Titel oben anzeigen (zentriert)
    title = " Batterie-Informationen "
    h, w = stdscr.getmaxyx()
    stdscr.attron(curses.color_pair(2))
    stdscr.addstr(0, (w - len(title)) // 2, title)
    stdscr.attroff(curses.color_pair(2))

    # Batterieinformationen anzeigen
    battery_info = get_battery_info()
    y, x = 2, 2  
    for line in battery_info:
        stdscr.addstr(y, x, line, curses.color_pair(5))
        y += 1  

    stdscr.refresh()
    stdscr.getch()
