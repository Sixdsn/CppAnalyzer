#!/usr/bin/python

import os, sys, subprocess

from options import SIXAnalyzer_options
from logger import SIXAnalyzer_logger
from rules import SIXAnalyzer_rules

class SIXAnalyzer_files():
    def __init__(self):
        #besoin d'ajouter check si files est vide ou ['']
        pass

    @staticmethod
    def get_files():
        return (SIXAnalyzer_files.files)

    @staticmethod
    def get_header_files():
        return (SIXAnalyzer_files.header_files)

    def __find_header_files():
        header_files = []
        if (SIXAnalyzer_options.header_folder != ""):
            if (not os.path.exists(SIXAnalyzer_options.header_folder)):
                print("Options -I %s doesn't not exist"% SIXAnalyzer_options.header_folder)
                sys.exit(1)
            SIXAnalyzer_logger.print_info("Getting Files from header_folder: " + SIXAnalyzer_options.header_folder)
            header_files = subprocess.check_output("find " + SIXAnalyzer_options.header_folder + 
                                                " -type f -readable \( " +
                                                SIXAnalyzer_rules.get_conf('extensions') +
                                                " \) -and -not -path \"" +
                                                SIXAnalyzer_options.path + "*\" | sort", shell=True).decode().split("\n")
        return (header_files)

    def __find_files():
        SIXAnalyzer_logger.print_info("Stage 1/6: Getting files to parse: %s"% SIXAnalyzer_options.path)
        files = subprocess.check_output("find " + SIXAnalyzer_options.path + " -type f -readable " +
                                        SIXAnalyzer_rules.get_conf('extensions') +
                                        " -or -name \"*.cpp\" | sort", shell=True).decode().split("\n")
        return (files)

    files = __find_files()
    header_files = __find_header_files()

#Only used by override module with multithreading
def get_files():
    return SIXAnalyzer_files.get_files()

def get_header_files():
    return SIXAnalyzer_files.get_header_files()
