#!/usr/bin/python

import os, sys, subprocess, logging

from options import SIXAnalyzer_options
from rules import SIXAnalyzer_rules

class SIXAnalyzer_files():
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
            logging.info("Getting Files from header_folder: " + SIXAnalyzer_options.header_folder)
            header_files = subprocess.check_output("find " + SIXAnalyzer_options.header_folder + 
                                                " -type f -readable \( " +
                                                SIXAnalyzer_rules.get_conf('header_extensions') +
                                                " \) -and -not -path \"" +
                                                SIXAnalyzer_options.path + "*\" | sort", shell=True).decode().split("\n")
        return (header_files)

    def __find_files():
        logging.info("Stage 1/6: Getting files to parse: %s"% SIXAnalyzer_options.path)
        files = subprocess.check_output("find " + SIXAnalyzer_options.path + " -type f -readable " +
                                        SIXAnalyzer_rules.get_conf('path_extensions') +
                                        " | sort", shell=True).decode().split("\n")
        return (files)

    files = __find_files()
    header_files = __find_header_files()

#Only used by override module with multithreading
def get_files():
    return SIXAnalyzer_files.get_files()

def get_header_files():
    return SIXAnalyzer_files.get_header_files()
