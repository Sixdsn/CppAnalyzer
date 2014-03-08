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
    SIXAnalyzer_logger.print_debug("File: " + classe.filename)
    SIXAnalyzer_logger.print_debug("Class: " + classe.name)
    for inherit in classe.inherits:
        SIXAnalyzer_logger.print_debug("From: " + inherit)
    SIXAnalyzer_logger.print_debug("Func: %d"% len(classe.funcs))
    for classfuncs in classe.funcs:
        SIXAnalyzer_logger.print_debug(classe.name + ": " + classfuncs[0] + " | " + classfuncs[2])
    SIXAnalyzer_logger.print_debug("Meths: %d"% len(classe.meths))
    for classmeths in classe.meths:
        SIXAnalyzer_logger.print_debug(classe.name + ": " + classmeths[0] + " | " + classmeths[2])
    SIXAnalyzer_logger.print_debug("Overriding Func: %d"% len(classe.Ofuncs))
    for classOfuncs in classe.Ofuncs:
        SIXAnalyzer_logger.print_debug(classe.name + ": " + classOfuncs[0])
    SIXAnalyzer_logger.print_debug("Overriding Meths: %d"% len(classe.Omeths))
    for classOmeths in classe.Omeths:
        SIXAnalyzer_logger.print_debug(classe.name + ": " + classOmeths[0])
    SIXAnalyzer_logger.print_debug("")
