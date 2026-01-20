import curses, sys, os

def save_file(filename, lines):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def editor(stdscr, filename):
    curses.curs_set(1)
    stdscr.keypad(True)
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = [ln.rstrip("\n") for ln in f.readlines()]
    except FileNotFoundError:
        lines = [""]
    if not lines:
        lines = [""]

    cy = 0
    cx = 0
    top = 0
    status = "Ctrl-S: save  Esc: quit"

    while True:
        h, w = stdscr.getmaxyx()
        stdscr.erase()
        # draw text area
        for i in range(h - 1):
            idx = top + i
            if idx < len(lines):
                stdscr.addstr(i, 0, lines[idx][:w-1])
        # status line
        stdscr.addstr(h - 1, 0, status[:w-1], curses.A_REVERSE)
        # keep cursor inside view
        if cy < top:
            top = cy
        elif cy >= top + (h - 1):
            top = cy - (h - 2)
        scr_y = cy - top
        stdscr.move(scr_y, min(cx, w - 1))
        stdscr.refresh()

        key = stdscr.get_wch()

        # control keys (strings for printable/control, ints for special keys)
        if isinstance(key, str):
            if key == "\x1b":  # Esc
                return
            if key == "\x13":  # Ctrl-S
                save_file(filename, lines)
                status = f"Saved: {os.path.basename(filename)}"
                continue
            if key == "\n":
                cur = lines[cy]
                lines[cy] = cur[:cx]
                lines.insert(cy + 1, cur[cx:])
                cy += 1
                cx = 0
                continue
            if key in ("\x7f", "\b"):  # backspace
                if cx > 0:
                    lines[cy] = lines[cy][:cx - 1] + lines[cy][cx:]
                    cx -= 1
                elif cy > 0:
                    prev_len = len(lines[cy - 1])
                    lines[cy - 1] += lines[cy]
                    lines.pop(cy)
                    cy -= 1
                    cx = prev_len
                continue
            # printable
            if ord(key) >= 32:
                lines[cy] = lines[cy][:cx] + key + lines[cy][cx:]
                cx += 1
                continue
        else:
            # special keys (integers)
            if key == curses.KEY_UP:
                if cy > 0:
                    cy -= 1
                cx = min(cx, len(lines[cy]))
            elif key == curses.KEY_DOWN:
                if cy < len(lines) - 1:
                    cy += 1
                cx = min(cx, len(lines[cy]))
            elif key == curses.KEY_LEFT:
                if cx > 0:
                    cx -= 1
                elif cy > 0:
                    cy -= 1
                    cx = len(lines[cy])
            elif key == curses.KEY_RIGHT:
                if cx < len(lines[cy]):
                    cx += 1
                elif cy < len(lines) - 1:
                    cy += 1
                    cx = 0
            elif key == curses.KEY_DC:  # delete
                if cx < len(lines[cy]):
                    lines[cy] = lines[cy][:cx] + lines[cy][cx + 1:]
                elif cy < len(lines) - 1:
                    lines[cy] += lines.pop(cy + 1)
            elif key == curses.KEY_HOME:
                cx = 0
            elif key == curses.KEY_END:
                cx = len(lines[cy])

        status = "Ctrl-S: save  Esc: quit"

def mini(filename):
    try:
        curses.wrapper(editor, filename)

    finally:
        curses.endwin()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python mini.py <file>")
    else:
        mini(sys.argv[1])
# ...existing code...
intro = True

while intro == True:
    try:
        print("MINI - not knockoff nano. Only for handling .txt files")
        ask2 = input("Do you want to OPEN a file, CREATE a file, RENAME a file, or DELETE a file?")
        ask2 = ask2.lower()

        if ask2 == "open":
            try:
                fileName = input("What is the name of the file you wish to open?")
                fileName = str(fileName+".txt")
                mini(fileName)
                    
            except:
                print("Error opening file and file editor!")
                    
            finally:
                fileName.close()
        elif ask2 == "create":
            try:
                fileName = input("What do you want to call your new file?")
                fileName = str(fileName+".txt")
                file = open(fileName, "w")
                mini(fileName)
                    
            except:
                print("Error creating file and opening file editor!")
                    
            finally:
                file.close()
                
        elif ask2 == "rename":
            try:
                fileName = input("What is the current name of the file you wish to rename?")
                fileName = str(fileName+".txt")
                fileNewName = input("What is the name you wish to rename the file to?")
                fileName = str(fileNewName+".txt")

                file = open(fileName, "r")
                newFile = open(fileNewName, "w")
                read = "nil"

                while read != "END":
                    read = file.readline()
                    newFile.write(read="\n")
                    
            except:
                print("File renaming error!")
                    
            finally:
                file.close()
                newFile.close()
    
        elif ask2 == "delete":
            try:
                fileName = input("What is the name of the file you wish to delete?")
                fileName = str(fileName+".txt")
                os.remove(fileName)
                print("File deleted successfully.")
                    
            except:
                print("File deletion error!")

        else:
            print("Invalid option selected.")  
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
                            