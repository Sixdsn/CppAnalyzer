#!/usr/bin/python

from logger import SIXAnalyzer_logger

def display(classes, files, header_files):
    tot_meths = 0
    tot_mems = 0

    for cppclass in classes:
        tot_meths += len(cppclass.funcs)
        tot_mems += len(cppclass.meths)
    print("")
    SIXAnalyzer_logger.print_verbose("Got %d File Issues" % len(SIXAnalyzer_logger.file_issue))
    for f in SIXAnalyzer_logger.file_issue:
        SIXAnalyzer_logger.print_debug(" -> %s"% f)
    SIXAnalyzer_logger.print_verbose("Found %d files to check" % len(files))
    SIXAnalyzer_logger.print_verbose("Found %d header files" % len(header_files))
    SIXAnalyzer_logger.print_verbose("Found %d classes" % len(classes))
    SIXAnalyzer_logger.print_verbose("Found %d member functions" % tot_mems)
    SIXAnalyzer_logger.print_verbose("Found %d methods" % tot_meths)

def display_class(classe, full):
    print("File: " + classe.filename)
    print("Class: " + classe.name)
    for inherit in classe.inherits:
        print("\t Inherits From: " + inherit)
    if full:
        all_meths = classe.funcs + classe.meths
        print("Methods: %d"% len(all_meths))
        for classfuncs in all_meths:
            print(classe.name + ": " + classfuncs[0] + " | " + classfuncs[2])
        all_Omeths = classe.Ofuncs + classe.Omeths
        print("Overriding Methods: %d"% len(all_Omeths))
        for classOfuncs in all_Omeths:
            print(classe.name + ": " + classOfuncs[0])
    print("")
