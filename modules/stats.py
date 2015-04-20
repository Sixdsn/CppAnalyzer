#!/usr/bin/python

import logging

file_issues = []

def add_file_issues(fname):
    global file_issues

    file_issues.append(fname)

def display(classes, files, header_files):
    global file_issues
    tot_meths = 0
    tot_mems = 0

    for cppclass in classes:
        tot_meths += len(cppclass.funcs)
        tot_mems += len(cppclass.meths)
    print("")
    logging.info("Got %d File Issues" % len(file_issues))
    for f in file_issues:
        logging.debug(" -> %s"% f)
    logging.info("Found %d files to check" % len(files))
    logging.info("Found %d header files" % len(header_files))
    logging.info("Found %d classes" % len(classes))
    logging.info("Found %d member functions" % tot_mems)
    logging.info("Found %d methods" % tot_meths)

def display_meths_class(classe, frome=False):
    all_meths = classe.funcs + classe.meths
    all_Omeths = classe.Ofuncs + classe.Omeths
    print("\t[Methods]: %d"% len(all_meths))
    for classfuncs in all_meths:
        print("\t\t%s: %s"% (classe.name, classfuncs[0]))
    if (frome):
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
    display_meths_class(classe, full)
    if full:
        count = 0
        for herits in childs:
            count += len(herits.Ofuncs + herits.Omeths)
        if (count > 0):
            print("\t[Methods Overrided in child classes]: %d"% count)
            for herits in childs:
                display_meths_class(herits)
    print("")
