import sys
import readline

def print_help():
    print("$>p [classname] => Shows class intels")

def get_line():
    try:
        return (raw_input("Analyze$> "))
    except:
        print("use quit or exit to exit")
        return (None)

def check_line(line):
    if (line == "help"):
        print_help()
        return ""
    elif (line == "exit" or line == "quit"):
        sys.exit(0)
    return line
