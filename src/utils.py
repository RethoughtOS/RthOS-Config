def display_action_message(stdscr, action_message):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    x = w // 2 - len(action_message) // 2
    y = h // 2
    stdscr.addstr(y, x, action_message, curses.color_pair(5))
    stdscr.addstr(y + 2, x, "Press [y] to confirm or any other key to cancel.", curses.color_pair(5))
    stdscr.refresh()

    key = stdscr.getch()
    return key == ord('y')

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
                repair_submenu(stdscr)
            else:
                if display_action_message(stdscr, f"Proceed with {options[current_row]}?"):
                    show_message(stdscr, f"{options[current_row]} in progress...")

def repair_submenu(stdscr):
    repair_options = ["Online Sync", "Reinstall Packages", "Reset Configurations", "Back"]
    current_row = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        draw_border(stdscr)

        stdscr.addstr(1, w // 2 - len("Repair Options") // 2, "Repair Options", curses.color_pair(5))

        for idx, option in enumerate(repair_options):
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
        elif key == curses.KEY_DOWN and current_row < len(repair_options) - 1:
            current_row += 1
        elif key in [curses.KEY_ENTER, 10, 13]:
            if repair_options[current_row] == "Back":
                break
            else:
                if display_action_message(stdscr, f"Proceed with {repair_options[current_row]}?"):
                    show_message(stdscr, f"{repair_options[current_row]} in progress...")