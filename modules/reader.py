import sys
import readline

def get_line():
    try:
        return (raw_input("Analyze$> "))
    except:
        print("use quit or exit to exit")
        return (None)

def check_line(line):
    if (line == "exit" or line == "quit"):
        sys.exit(0)
    return line
