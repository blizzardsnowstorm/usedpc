# skeleton
# basic, text, terminal, game
# another test
import pwinput
import sys
import time
import random
import colorama
import os
import json
import shutil

# -------------------------------------------------------------------
# DICTS
# ------------------------------------------------------------------
accounts = {
    "bank": {},
    "email": {}
}
websites = {
    "hackers.org": "hackerssite",
    "bank.com": "banksite",
    "email.com": "emailsite",
    "shop.com": "shopsite",
    "computers.edu": "computersedusite"
}

# -------------------------------------------------------------------
# VIRTUAL FILESYSTEM
# -------------------------------------------------------------------
VIRTUALFS = {
    "home": {
        "type": "dir",
        "owner": "user",
        "contents": {
            "documents": {
                "type": "dir",
                "owner": "user",
                "contents": {
                    "todo.txt": {
                        "type": "file",
                        "owner": "user",
                        "content": (
                            "1. Customize your OS.\n"
                            "2. Explore the filesystem.\n"
                            "3. Connect to a website.\n"
                        )
                    }
                }
            },
            "systemlog.txt": {
                "type": "file",
                "owner": "root",
                "content": "2025-12-02 01:00:00 - Starting Input Listener Service..."
            },
            "README.txt": {
                "type": "file",
                "owner": "root",
                "content": "Welcome to CAMELOT OS. Use 'help' for commands."
            }
        }
    },

    "usr": {
        "type": "dir",
        "owner": "root",
        "contents": {
            "bin": {"type": "dir", "owner": "root", "contents": {}}
        }
    },

    "var": {
        "type": "dir",
        "owner": "root",
        "contents": {
            "log": {
                "type": "dir",
                "owner": "root",
                "contents": {
                    "boot.log": {
                        "type": "file",
                        "owner": "root",
                        "content": "System boot completed successfully."
                    }
                }
            }
        }
    }
}

# -------------------------------------------------------------------
# UTILITY FUNCTIONS
# -------------------------------------------------------------------
def getcurrentdirectorycontents(gamestate):
    """Return the contents of the directory at gamestate['currentPath']."""
    path = gamestate["currentPath"].strip("/")
    parts = path.split("/") if path else []

    node = gamestate["fileSystem"]

    for part in parts:
        if not part:
            continue
        if part in node and node[part]["type"] == "dir":
            node = node[part]["contents"]
        else:
            return None

    return node


def slowprint(text, delay=0.015):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")


def realslowprint(text, delay=0.5):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")


def clearscreen():
    os.system("clear" if os.name != "nt" else "cls")


def enterprompt(prompt="[Press ENTER to continue...]"):
    input(prompt)
    print()


# -----------------------
# WEBSITE HANDLERS
# -----------------------
def handleemail(gamestate):
    slowprint("Connecting to email.com...")
    time.sleep(1)
    slowprint("Welcome to email.com")
    print("1) Login")
    print("2) Create Account")
    choice = input("> ").strip()

    if choice == "2":
        username = input("Choose an email address: ").strip()
        if not username:
            slowprint("Invalid username.")
            return
        if username in accounts["email"]:
            slowprint("Email account already exists.")
            return
        password = pwinput.pwinput("Create a password: ")
        accounts["email"][username] = {
            "password": password,
            "inbox": ["Welcome to email.com!"]
        }
        slowprint("Email account created!")
        return

    elif choice == "1":
        username = input("Email username: ").strip()
        password = pwinput.pwinput("Password: ")

        if username in accounts["email"] and accounts["email"][username]["password"] == password:
            slowprint("Login successful. Inbox:")
            inbox = accounts["email"][username]["inbox"]
            if not inbox:
                print("(empty)")
            else:
                for i, msg in enumerate(inbox, 1):
                    print(f"{i}. {msg}")
        else:
            slowprint("Invalid credentials.")
    else:
        slowprint("Canceled.")


def handlebank(gamestate):
    slowprint("Connecting to bank.com...")
    time.sleep(1)

    slowprint("Welcome to the Bank.")
    print("1) Login")
    print("2) Create Account")
    choice = input("> ").strip()

    if choice == "2":
        username = input("Choose a username: ").strip()
        if not username:
            slowprint("Invalid username.")
            return
        if username in accounts["bank"]:
            slowprint("Account already exists.")
            return

        password = pwinput.pwinput("Choose a password: ")
        accounts["bank"][username] = {
            "password": password,
            "balance": 100  # starting balance
        }
        slowprint("Account created! Starting balance: $100")
        return

    elif choice == "1":
        username = input("Username: ").strip()
        password = pwinput.pwinput("Password: ")

        if username in accounts["bank"] and accounts["bank"][username]["password"] == password:
            slowprint("Login successful.")
            bal = accounts["bank"][username]["balance"]
            slowprint(f"Your current balance is: ${bal}")
            # small bank menu
            while True:
                print("\nBank menu:")
                print("  1) Deposit $10")
                print("  2) Withdraw $10")
                print("  3) Logout")
                sel = input("> ").strip()
                if sel == "1":
                    accounts["bank"][username]["balance"] += 10
                    slowprint(f"Deposited $10. New balance: ${accounts['bank'][username]['balance']}")
                elif sel == "2":
                    if accounts["bank"][username]["balance"] >= 10:
                        accounts["bank"][username]["balance"] -= 10
                        slowprint(f"Withdrew $10. New balance: ${accounts['bank'][username]['balance']}")
                    else:
                        slowprint("Insufficient funds.")
                elif sel == "3":
                    slowprint("Logging out of bank.")
                    break
                else:
                    slowprint("Invalid choice.")
        else:
            slowprint("Invalid credentials.")
            return
    else:
        slowprint("Canceled.")


# -------------------------------------------------------------------
# COMMANDS
# -------------------------------------------------------------------
def exitcommand(gamestate, args):
    slowprint("Logging off...")
    gamestate["running"] = False


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def helpcommand(gamestate, args):
    print("Available commands:")
    print("  help        Show this help list.")
    print("  exit        Log off the system.")
    print("  ls          List files and directories.")
    print("  cd <dir>    Change directory.")
    print("  cat <file>  View a file.")
    print("  wget <host> Connect to a website (e.g. wget bank.com)")


def wgetcommand(gamestate, args):
    if not args:
        slowprint("wget: missing arguments: provide URL")
        slowprint("Try 'wget computers.edu'")
        return
    targeturl = args[0]
    if targeturl in websites:
        sitetype = websites[targeturl]
        slowprint(f"Connecting to {targeturl}...")
        time.sleep(1)
        if sitetype == "banksite":
            handlebank(gamestate)
        elif sitetype == "emailsite":
            handleemail(gamestate)
        else:
            slowprint(f"Connected to {targeturl} — nothing interesting here.")
    else:
        slowprint(f"Error: Could not resolve host {targeturl}. Unknown domain.")


def lscommand(gamestate, args):
    show_all = False
    path_arg = None

    for a in args:
        if a == "-a":
            show_all = True
        elif not a.startswith("-"):
            path_arg = a

    original_path = gamestate["currentPath"]
    if path_arg:
        if path_arg.startswith("/"):
            temp_state = {"fileSystem": gamestate["fileSystem"], "currentPath": path_arg}
            contents = getcurrentdirectorycontents(temp_state)
        else:
            temp_state = {"fileSystem": gamestate["fileSystem"], "currentPath": original_path.rstrip("/") + "/" + path_arg}
            contents = getcurrentdirectorycontents(temp_state)
    else:
        contents = getcurrentdirectorycontents(gamestate)

    if contents is None:
        print(f"ls: cannot access '{path_arg or original_path}': No such directory")
        return

    items = []
    for name, node in contents.items():
        items.append((name, node["type"]))

    if show_all and gamestate["currentPath"] != "/":
        items.insert(0, ("..", "dir"))
        items.insert(0, (".", "dir"))

    for name, typ in items:
        if typ == "dir":
            print(f"{colorama.Fore.BLUE}{name}{colorama.Style.RESET_ALL}/")
        else:
            print(name)


def cdcommand(gamestate, args):
    if not args:
        print("cd: missing operand")
        return

    target = args[0]
    curr = gamestate["currentPath"]

    # cd ..
    if target == "..":
        if curr != "/":
            gamestate["currentPath"] = curr.rsplit("/", 1)[0] or "/"
        return

    # Absolute path
    if target.startswith("/"):
        node = gamestate["fileSystem"]
        parts = target.strip("/").split("/") if target != "/" else []
        newpath = ""
    else:
        node = getcurrentdirectorycontents(gamestate)
        if node is None:
            print(f"cd: internal error: invalid current path '{curr}'")
            return
        parts = [target]
        newpath = curr.rstrip("/")

    # Walk
    for part in parts:
        if not part:
            continue
        if part in node and node[part]["type"] == "dir":
            node = node[part]["contents"]
            newpath += "/" + part
        else:
            print(f"cd: {target}: No such directory")
            return

    gamestate["currentPath"] = newpath or "/"


def catcommand(gamestate, args):
    if not args:
        print("cat: missing operand")
        return

    filename = args[0]
    contents = getcurrentdirectorycontents(gamestate)

    if contents is None:
        print("cat: error: invalid directory")
        return

    if filename not in contents:
        print(f"cat: {filename}: No such file")
        return

    node = contents[filename]
    if node["type"] != "file":
        print(f"cat: {filename}: Is a directory")
        return

    slowprint(node["content"])


# -------------------------------------------------------------------
# GAME STATE
# -------------------------------------------------------------------
def initializegamestate(username, password):
    colorama.init(autoreset=True)
    return {
        "username": username,
        "hostname": "camelot",
        "running": True,
        "currentPath": "/home",
        "fileSystem": VIRTUALFS,
        "commands": {
            "help": helpcommand,
            "exit": exitcommand,
            "ls": lscommand,
            "cd": cdcommand,
            "cat": catcommand,
            "clear": lambda gs, args: clear(),
            "wget": wgetcommand
        }
    }


# -------------------------------------------------------------------
# COMMAND EXECUTION
# -------------------------------------------------------------------
def handlecommand(userinput, gamestate):
    parts = userinput.strip().split()
    if not parts:
        return

    cmd = parts[0]
    args = parts[1:]

    cmds = gamestate["commands"]

    if cmd in cmds:
        cmds[cmd](gamestate, args)
    else:
        print(f"{cmd}: command not found")


# -------------------------------------------------------------------
# MAIN LOOP
# -------------------------------------------------------------------
def gameloop(gamestate):
    while gamestate["running"]:
        prompt = (
            f"{colorama.Fore.GREEN}{gamestate['username']}"
            f"{colorama.Fore.WHITE}@"
            f"{colorama.Fore.CYAN}{gamestate['hostname']}"
            f"{colorama.Fore.WHITE}:{colorama.Fore.YELLOW}"
            f"{gamestate['currentPath']}"
            f"{colorama.Fore.WHITE}$ {colorama.Style.RESET_ALL}"
        )

        try:
            userinput = input(prompt)
        except EOFError:
            print("\nExiting simulation.")
            break

        handlecommand(userinput, gamestate)

    slowprint("System offline.")


# -------------------------------------------------------------------
# BOOT SEQUENCE + LOGIN
# -------------------------------------------------------------------
def main():
    clearscreen()
    slowprint("You found a shitty PC on the side of the road in a nice suburb.")
    slowprint("You plug it into a public outlet at the library.")
    enterprompt()

    clearscreen()
    print("[UEFI] Minimal Firmware Check v1.02")
    time.sleep(0.6)
    print("CPU: Intel Celeron N4000 @ 1.10GHz   [OK]")
    slowprint("RAM: 4GB DDR4 2400MHz               [OK]")
    slowprint("HDD: 256GB SATA SSD                  [OK]")
    slowprint("SystemD Boot Manager — CAMELOT")
    slowprint("Loading Kernel 5.4.0-lowpower...")
    slowprint("Initializing disk cache...           [OK]")
    slowprint("Waking LAN adapter...                [OK]")
    slowprint("Starting Input Listener Service...   [OK]")
    slowprint("Running filesystem integrity check... [OK]")
    time.sleep(1)

    clearscreen()
    username = input("Create a username: ").strip()
    if not username:
        username = "player"

    while True:
        pw1 = pwinput.pwinput("Create a password: ")
        pw2 = pwinput.pwinput("Confirm password: ")
        if pw1 == pw2:
            slowprint("Password confirmed.")
            break
        slowprint("Passwords do not match.\n")

    clearscreen()
    slowprint("Loading OS…")
    realslowprint("[#######]")
    clearscreen()

    state = initializegamestate(username, pw1)
    slowprint(f"Welcome to CAMELOT OS, {username}.")
    gameloop(state)


if __name__ == "__main__":
    main()

