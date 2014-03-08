#!/usr/bin/python

import sys, concurrent.futures, CppHeaderParser

from multiprocessing import Value

from logger import SIXAnalyzer_logger
from rules import SIXAnalyzer_rules
from options import SIXAnalyzer_options
from files import SIXAnalyzer_files

import stats
import builder_func

def chunks(seq, n):
    return (seq[i:i+n] for i in range(0, len(seq), n))

class_cpt = Value('i', -1)
file_cpt = Value('i', -1)

class SIXAnalyzer_builder():
    def __init__(self, files, idl_files):
        self.classes = {}
        self.good_classes = {}
        self.files = files
        self.idl_files = idl_files
        CppHeaderParser.ignoreSymbols += SIXAnalyzer_rules.to_ignore

    def init(self):
        self.parse_header_files()
        return (self.classes)


    def get_classes(self):
        return self.classes

    def run(self):
        SIXAnalyzer_logger.print_info("Stage */6: Managing Typedef's")
        local_classes = []
        chunk_size = 50
        if (chunk_size > len(self.classes)):
            chunk_size = int(len(self.classes) / SIXAnalyzer_options.workers)
        if (chunk_size == 0):
            chunk_size = 1
        listes = list(chunks(self.classes, int(len(self.classes) / chunk_size)))
        #depends on issue #19 need to reduce memory usage
        workers = SIXAnalyzer_options.workers
        if (workers > 1):
            workers = 2
        with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
            future_task = {executor.submit(manage_typedefs, self.classes, liste): liste for liste in listes}
            for future in concurrent.futures.as_completed(future_task):
                try:
                    local_classes.extend(future.result())
                except Exception as exc:
                    print('Worker generated an exception: %s' % (exc))
                    continue
        self.classes = local_classes
        self.good_classes = [ elem for elem in self.classes if elem.filename in SIXAnalyzer_files.get_files() ]
        print("")
        self.add_full_heritage()
        self.find_override()

    def is_a_class(self, name):
        might_be = None
        for cppclass in self.classes:
            if cppclass.name == name:
                #we give priority to class in files to modify
                if cppclass.filename in SIXAnalyzer_files.get_files():
                    return (cppclass)
                else:
                    #keep the one that isn't in the file to modify
                    #in case we don't find another one
                    might_be = cppclass
        return (might_be)

    ## @brief creates the heritage tree for all methods
    ## @param self.classes dict of all self.classes
    #  classname string
    ## @returns void
    def find_override(self):
        SIXAnalyzer_logger.print_info("Stage 4/6: Finding methods to override")
        for cppclass in self.good_classes:
            for inherit in cppclass.inherits:
                inhname = inherit
                inherit = self.is_a_class(inherit)
                if (inherit):
                    SIXAnalyzer_logger.print_debug(cppclass.name + " inherits " + inherit.name)
                    for inhmeths in inherit.meths:
                        SIXAnalyzer_logger.print_debug("1: " + inherit.name + "::" + inhmeths[0])
                        for classfuncs in cppclass.funcs:
                            SIXAnalyzer_logger.print_debug("2: " + inherit.name + "::" + inhmeths[0] \
                                            + " " + cppclass.name + "::" + classfuncs[0])
                            if inhmeths[0] == classfuncs[0]:
                                cppclass.Ofuncs.append(classfuncs + [ inherit.name ])
                                SIXAnalyzer_logger.print_debug("OVERRIDE2: " + inherit.name + "::" + inhmeths[2] \
                                                + " and " + cppclass.name + "::" + classfuncs[2])
                                break
                        for classmeths in cppclass.meths:
                            SIXAnalyzer_logger.print_debug("3: " + inherit.name + "::" + inhmeths[0] \
                                            + " " + cppclass.name + "::" + classmeths[0])
                            if inhmeths[0] == classmeths[0]:
                                cppclass.Omeths.append(classmeths + [ inherit.name ])
                                SIXAnalyzer_logger.print_debug("OVERRIDE3: " + inherit.name + "::" + inhmeths[2] \
                                                + " line [" + str(inhmeths[3]) + "]" \
                                                + " and " + cppclass.name + "::" + classmeths[2] + " line [" + str(classmeths[3]) + "]")
                                break
                else:
                    SIXAnalyzer_logger.print_debug("Inherit Error: " + inhname + " not found for " + cppclass.name)

    def add_full_heritage(self):
        SIXAnalyzer_logger.print_info("Stage 3/6: Creating Heritage Tree")
        change = 1
        while (change == 1):
            change = 0
            for cppclass in self.good_classes:
                for simple_inherits in cppclass.inherits:
                    test_inh = self.is_a_class(str(cppclass.namespace + simple_inherits))
                    if (test_inh and not self.is_a_class(simple_inherits)):
                        simple_inherits = test_inh
                    else:
                        simple_inherits = self.is_a_class(simple_inherits)
                    if (simple_inherits):
                        for hidden_inherits in simple_inherits.inherits:
                            if (self.is_a_class(hidden_inherits) and hidden_inherits not in cppclass.inherits and hidden_inherits != cppclass.name):
                                SIXAnalyzer_logger.print_debug("Class: " + cppclass.name + " inherits " + hidden_inherits)
                                cppclass.inherits.append(hidden_inherits)
                                change = 1
                            else:
                                SIXAnalyzer_logger.print_debug("OTHER: " + cppclass.name + " inherits " + hidden_inherits)

    def parse_header_files(self):
        SIXAnalyzer_logger.print_info("Stage 2/6: Parsing Header Files")
        nb_files = len(self.files) + len(self.idl_files)
        files = self.files + self.idl_files
        self.classes = []
        saveout = sys.stdout
        chunk_size = 50
        if (chunk_size > len(files)):
            chunk_size = int(len(files) / SIXAnalyzer_options.workers)
        if (chunk_size == 0):
            chunk_size = 1
        listes = list(chunks(files, int(len(files) / chunk_size)))
        with concurrent.futures.ProcessPoolExecutor(max_workers=SIXAnalyzer_options.workers) as executor:
            future_task = {executor.submit(do_parse, liste, len(files)): liste for liste in listes}
            for future in concurrent.futures.as_completed(future_task):
                try:
                    self.classes.extend(future.result())
                except Exception as exc:
                    sys.stdout = saveout
                    print('Worker generated an exception: %s' % (exc))
                    continue
        sys.stdout = saveout

class CppClass():
    def __init__(self, filename):
        self.name = ""
        self.filename = filename
        self.inherits = []
        self.namespace = ""
        self.funcs = []
        self.meths = []
        self.Ofuncs = []
        self.Omeths = []
        self.nested_typedefs = {}
        self.typedefs = {}

    def set_name(self, classe):
        if len(classe["namespace"]):
            self.namespace = classe["namespace"].strip("::") + "::"
        self.name = self.namespace
        self.name += classe["name"]
        SIXAnalyzer_logger.print_debug("Class: " + self.name)

    def set_inherits(self, classe):
        for inherit in classe["inherits"]:
            if (inherit['class'] != self.name):
                self.inherits.append(inherit['class'])
                SIXAnalyzer_logger.print_debug("Inherits: %s"% inherit['class'])

    def append_ometh(self, meth):
        self.Omeths.append(meth)

    def append_meth(self, meth):
        self.meths.append(meth)

    def append_func(self, func):
        self.funcs.append(func)

def manage_typedefs(all_classes, liste):
    global class_cpt

    for cppclass in all_classes:
        for name in cppclass.typedefs:
            for ncppclass in liste:
                for inh in ncppclass.inherits:
                    if inh == name and cppclass.typedefs[name] not in ncppclass.inherits and cppclass.typedefs[name] != cppclass.name:
                        ncppclass.inherits.append(cppclass.typedefs[name])
                        SIXAnalyzer_logger.print_debug(cppclass.name + " typedef inherits: " + cppclass.typedefs[name])
                        break
    class_cpt.value += len(liste)
    SIXAnalyzer_logger.foo_print("[%d%%]"% int(class_cpt.value * 100 / len(all_classes)))
    return (liste)

def build_meth(typeid_func):
    SIXAnalyzer_logger.print_debug("meth name: " + typeid_func["name"])
    SIXAnalyzer_logger.print_debug("meth ret: " + typeid_func["rtnType"] \
                              + " => " + builder_func.check_ret(typeid_func["rtnType"]))
    SIXAnalyzer_logger.print_debug(typeid_func)
    meths = builder_func.check_ret(typeid_func["rtnType"])
    if (len(meths)):
        meths += " "
    meths += typeid_func["name"] + " ("
    params = ""
    for param in range(len(typeid_func["parameters"])):
        SIXAnalyzer_logger.print_debug("meth params: " + typeid_func["parameters"][param]["type"])
        real_param = typeid_func["parameters"][param]["type"].split("::") 
        params += real_param[len(real_param) - 1:][0]
        SIXAnalyzer_logger.print_debug("Param: " + typeid_func["parameters"][param]["type"] \
                                  + " => " + real_param[len(real_param) - 1:][0])
        params += " "
        if (params != "void "):
            meths += params
    meths +=  ")"
    if (typeid_func['const']):
        meths += " const"
    return (meths)

def gen_class(filename, cppHeader, HeaderClass):
    accessType_tab = [ "public", "private", "protected" ]

    headerclass = cppHeader.classes[HeaderClass]
    cppclass = CppClass(filename)
    cppclass.set_name(headerclass)
    cppclass.set_inherits(headerclass)
    for accessType in accessType_tab:
        for typeid_func in headerclass["methods"][accessType]:
            meths = build_meth(typeid_func)
            if (typeid_func.show().find("virtual") != -1) \
               or (typeid_func.show().find("NS_IMETHOD") != -1) \
               or (typeid_func.show().find("NS_IMETHOD_") != -1):
                SIXAnalyzer_logger.print_debug("Meths: " + meths)
                cppclass.append_meth([builder_func.over_meth(meths), \
                                      builder_func.over_meth(typeid_func["debug"]), \
                                      typeid_func["debug"], \
                                      typeid_func["line_number"], \
                                      typeid_func["name"]])
            else:
                SIXAnalyzer_logger.print_debug("Funcs: " + meths)
                cppclass.append_func([builder_func.over_meth(meths), \
                                      builder_func.over_meth(typeid_func["debug"]), \
                                      typeid_func["debug"], \
                                      typeid_func["line_number"], \
                                      typeid_func["name"]])
            SIXAnalyzer_logger.print_debug("%s: Funcs(%d) Meths(%d)"% (cppclass.name, len(cppclass.funcs), len(cppclass.meths)))
    cppclass.nested_typedefs = headerclass._public_typedefs
    cppclass.typedefs = cppHeader.typedefs
    #Only for debug
    #stats.display_class(cppclass)
    return (cppclass)

def do_parse(files, nb_files):
    global file_cpt

    classes = []
    saveout = sys.stdout
    dev_null = open("/dev/null", 'w')
    for filename in files:
        file_cpt.value += 1
        try:
            sys.stdout = dev_null
            cppHeader = CppHeaderParser.CppHeader(filename)
            sys.stdout = saveout
        except CppHeaderParser.CppParseError as e:
            sys.stdout = saveout
            SIXAnalyzer_logger.print_error(str(e), filename)
            continue
        except Exception as e:
            sys.stdout = saveout
            SIXAnalyzer_logger.print_error(str(e), filename)
            continue
        except:
            sys.stdout = saveout
            SIXAnalyzer_logger.print_error("Unknown", filename)
            continue
            SIXAnalyzer_logger.print_debug("NB CLASSES: " + str(len(cppHeader.classes)))
            SIXAnalyzer_logger.print_debug(cppHeader.classes)
        for HeaderClass in cppHeader.classes:
            classes.append(gen_class(filename, cppHeader, HeaderClass))
    SIXAnalyzer_logger.foo_print("[%d%%]"% int(file_cpt.value * 100 / nb_files))
    dev_null.close()
    return (classes)
