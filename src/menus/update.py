import curses
import os
import subprocess
from utils import show_message, draw_border

def ensure_sudo():
    if os.geteuid() != 0:
        try:
            subprocess.run(["clear"], check=True)  # Terminal clearen
            subprocess.run(["sudo", "-k", "echo", "Sudo access granted"], check=True)
            return True
        except subprocess.CalledProcessError:
            return False
    return True

def perform_update():
    try:
        subprocess.run(["clear"], check=True)  # Terminal clearen
        subprocess.run(["sudo", "pacman", "-Syu"], check=True)
        return "Update erfolgreich abgeschlossen!"
    except subprocess.CalledProcessError as e:
        return f"Update fehlgeschlagen:\n{e.stderr}"

def update_menu(stdscr):
    if ensure_sudo():
        curses.endwin()  # TUI beenden
        subprocess.run(["clear"], check=True)  # Terminal clearen
        message = perform_update()
        subprocess.run(["clear"], check=True)  # Terminal clearen
        curses.initscr()  # TUI neu starten
        show_message(stdscr, message)  # Nachricht anzeigen
    else:
        show_message(stdscr, "Sudo-Zugriff verweigert oder abgebrochen.")