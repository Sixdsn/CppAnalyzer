#!/usr/bin/python

import os, sys, getopt

from logger import SIXAnalyzer_logger

## @brief print usage
def usage():
    print("Usage: ./this_script Path [-v|-d] [-h|--help] [-I header_from_header_folder] [-J Number of parallel parsers]")

## @brief print help
def _help():
    print("Usage: ./this_script Path [-v|-d] [--dryrun] [-h|--help] [-W]")
    print("-v:\t\tVerbose")
    print("-d:\t\tDebug (Include Verbose)")
    print("-I folder:\tFolder you want to get headers generated from header_files")
    print("-J workers:\tNumber of parallel process to parse the files")
    print("-h --help:\tPrint this Menu")

class SIXAnalyzer_options():
    @staticmethod
    def __init__():
        pass

    def check_options():
        if (len(sys.argv) < 2 or len(sys.argv[1]) <= 0 or not os.path.exists(sys.argv[1])):
            usage()
            sys.exit(1)
        header_folder = ""
        workers = 1
        try:
            opts, args = getopt.getopt(sys.argv[2:], "hdvJ:I:", [ "help" ])
        except getopt.GetoptError as err:
            print("GetOpt Error: %s"% str(err))
            usage()
            sys.exit(2)
        except:
            print("Unknown opt Error")
            sys.exit(2)

        if (len(args)):
            print("Unhandled Option")
            sys.exit(1)
        for o, a in opts:
            if o == "-v":
                print("[Running Verbose Mode]")
                SIXAnalyzer_logger.set_verbose()
            elif o in ("-d"):
                print("[Running Debug Mode]")
                SIXAnalyzer_logger.set_debug()
            elif o in ("-I"):
                print("[Using Header Folder] %s"% a)
                header_folder = a
            elif o in ("-J"):
                if (int(a) <= 0):
                    usage()
                    sys.exit(1)
                print("[Using %d Workers]"% int(a))
                workers = int(a)
            elif o in ("-h", "--help"):
                _help()
                sys.exit(0)
            else:
                print("Unhandled Option")
                sys.exit(1)
        return (sys.argv[1], header_folder, workers)

    path, header_folder, workers = check_options()
