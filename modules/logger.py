#!/usr/bin/python

import sys
from multiprocessing import Manager

class SIXAnalyzer_logger():

    rlock = Manager().RLock()

    @staticmethod
    def __my_print(bar):
        with SIXAnalyzer_logger.rlock:
            print(bar)
            
    ## @brief does nothing, called of no "-d" nor "-v"
    ## @param param string
    ## @returns void
    @staticmethod
    def __void_print(param):
        pass

    ## @brief print debug if "-d"
    ## @param param string
    ## @returns void
    @staticmethod
    def __debug(param):
        SIXAnalyzer_logger.__my_print("[DEBUG] %s"% str(param))

    ## @brief print verbose if "-v" or "-d"
    ## @param param string
    ## @returns void
    @staticmethod
    def verbose(param):
        SIXAnalyzer_logger.__my_print("[VERBOSE] %s"% str(param))

    @staticmethod
    def foo_print(bar):
        sys.stdout.write("\r\x1b[K"+bar.__str__())
        sys.stdout.flush()

    @staticmethod
    def __init__():
        pass

    @staticmethod
    def set_verbose():
        SIXAnalyzer_logger.print_verbose = staticmethod(SIXAnalyzer_logger.verbose)

    @staticmethod
    def set_debug():
        SIXAnalyzer_logger.set_verbose()
        SIXAnalyzer_logger.print_debug = staticmethod(SIXAnalyzer_logger.__debug)

    ## @brief print info
    ## @param param string
    ## @returns void
    @staticmethod
    def print_info(param):
        SIXAnalyzer_logger.__my_print("[INFO] %s"% str(param))

    @staticmethod
    def print_error(msg, filename):
        SIXAnalyzer_logger.print_debug("")
        SIXAnalyzer_logger.print_debug("[EXCEPTION] " + msg + " " + filename)
        SIXAnalyzer_logger.file_issue.append(filename)

    file_issue = []
    print_verbose = __void_print
    print_debug = __void_print
