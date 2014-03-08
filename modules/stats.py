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

def display_class(classe):
    print("File: " + classe.filename)
    print("Class: " + classe.name)
    for inherit in classe.inherits:
        print("From: " + inherit)
    print("Func: %d"% len(classe.funcs))
    for classfuncs in classe.funcs:
        print(classe.name + ": " + classfuncs[0] + " | " + classfuncs[2])
    print("Meths: %d"% len(classe.meths))
    for classmeths in classe.meths:
        print(classe.name + ": " + classmeths[0] + " | " + classmeths[2])
    print("Overriding Func: %d"% len(classe.Ofuncs))
    for classOfuncs in classe.Ofuncs:
        print(classe.name + ": " + classOfuncs[0])
    print("Overriding Meths: %d"% len(classe.Omeths))
    for classOmeths in classe.Omeths:
        print(classe.name + ": " + classOmeths[0])
    print("")
