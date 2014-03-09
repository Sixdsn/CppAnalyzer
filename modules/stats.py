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

def display_meths_class(classe, frome=False):
    all_Omeths = classe.Ofuncs + classe.Omeths
    if (frome):
        all_meths = classe.funcs + classe.meths
        print("\t[Methods]: %d"% len(all_meths))
        for classfuncs in all_meths:
            print("\t\t%s: %s"% (classe.name, classfuncs[0]))
        print("\t[Overriding Methods]: %d"% len(all_Omeths))
        for classOfuncs in all_Omeths:
            print("\t\t%s: %s FROM: %s"% (classe.name, classOfuncs[0], classOfuncs[5]))
    else:
        for classOfuncs in all_Omeths:
            print("\t\t%s: %s"% (classe.name, classOfuncs[0]))

def display_class(classe, full, childs):
    print("[Class]: %s"% classe.name)
    print("[In File]: %s"% classe.filename)
    for inherit in classe.inherits:
        print("\tInherits From: " + inherit)
    for herits in childs:
        print("\tClass heriting are: " + herits.name)
    if full:
        display_meths_class(classe, True)
        count = 0
        for herits in childs:
            count += len(herits.Ofuncs + herits.Omeths)
        if (count > 0):
            print("\t[Methods Overrided in child classes]: %d"% count)
            for herits in childs:
                display_meths_class(herits)
    print("")
