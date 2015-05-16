import fnmatch, sys, os, glob, imp

import pygraphviz as pgv

from collections import OrderedDict
from options import SIXAnalyzer_options
from reader import Reader

import stats

CMDS = [ "pc", "pcf", "pf", "pff", "sc", "sf", "sm", "imp", "reload", "cd", "graph" ]

PATH = SIXAnalyzer_options.path

def get_module_path(uri):
    if (uri[0] != '/'):
        uri = os.path.dirname(os.path.realpath(__file__ + "/..")) + "/" + uri
    path, fname = os.path.split(uri)
    mname, ext = os.path.splitext(fname)
    no_ext = os.path.join(path, mname)
    return (mname, no_ext)

class SIXAnalyzer_finder():
    def __init__(self, classes):
        global CMDS

        self.modules_loaded = []
        self.classes = sorted(classes, key=lambda classe: classe.name.lower())
        self.cmd =  {
            "pc": [ self.run_pc, " [classname]\t=> Shows Basic Class Intels", True ], \
            "pcf": [ self.run_pcf, " [classname]\t=> Shows All Class Intels", True ], \
            "pf": [ self.run_pf, " [filename]\t=> Shows Basic Class Intels contained in Filename", True ], \
            "pff": [ self.run_pff, " [filename]\t=> Shows All Class Intels contained in Filename", True ], \
            "sc": [ self.run_sc, " [classname]\t=> Search Class", True ], \
            "sf": [ self.run_sf, " [filename]\t=> Search Files", True ], \
            "sm": [ self.run_sm, " [method]\t\t=> Search Methods", True ], \
            "imp": [ self.run_imp, " [module]\t\t=> Import Module", True ], \
            "reload": [ self.run_reload, " [module]\t=> Reimport Module", True ], \
            "cd": [ self.run_cd, " [folder]\t\t=>Change Folder", False ], \
            "graph": [ self.run_graph, " [filename]\t=> Generate Classes Graph", True ]
        }
        if (len(self.cmd) != len(CMDS)):
            raise "SIXAnalyzer_finder.cmd != global CMDS"
        self.autoload_modules()
        self.cmd = OrderedDict(sorted(self.cmd.items(), key=lambda kv: kv[0].lower()))

    def import_module(self, uri):
        mname, no_ext = get_module_path(uri)
        if uri not in self.modules_loaded:
            if os.path.exists(no_ext + '.py'):
                try:
                    mod = imp.load_source(mname, no_ext + '.py').init()
                    self.modules_loaded.append(uri)
                    return mod
                except:
                    pass
            elif os.path.exists(no_ext + '.pyc'):
                try:
                    mod = imp.load_compiled(mname, no_ext + '.pyc').init()
                    self.modules_loaded.append(uri)
                    return mod
                except:
                    pass
        else:
            print("Modules '%s' Already Loaded"% mname)

    def run_reload(self, modname):
        mname, no_ext = get_module_path(modname)
        self.modules_loaded.remove(modname)
        mod = self.import_module(modname)
        if (not mod):
            return
        for cmd, elems in mod.iteritems():
            if (cmd in self.cmd):
                self.cmd.pop(cmd)
                CMDS.remove(cmd)
        print("Module ReLoaded: %s"% modname)
        for cmd, elems in mod.iteritems():
            print("\t$>%s %s"% (cmd, elems[1]))
            CMDS.append(cmd)
        self.cmd.update(mod)

    def autoload_modules(self):
        for fname in glob.glob("services/*.py"):
            self.run_imp(fname)
        for fname in glob.glob("services/*.pyc"):
            if fname[:-1] not in self.modules_loaded:
                self.run_imp(fname)

    def get_class_by_name(self, classname):
        res = [ elem for elem in self.classes if fnmatch.fnmatch(elem.name.lower(), classname.lower()) ]
        if (len(res) == 0):
            return (None)
        return (sorted(res, key=lambda classe: classe.name.lower()))

    def get_class_by_filename(self, filename):
        res = [ elem for elem in self.classes if fnmatch.fnmatch(elem.filename.lower(), filename.lower()) ]
        if (len(res) == 0):
            return (None)
        return (sorted(res, key=lambda classe: (classe.filename.lower(), classe.name.lower())))

    def get_child_class(self, classes):
        res = []
        for classe in classes:
            for cl in self.classes:
                if classe.name in cl.inherits:
                    res.extend(self.get_class_by_name(cl.name))
        return (sorted(res, key=lambda classe: classe.name.lower()))

    def run_help(self):
        print("All parameters are interepreted as regex")
        print("But use '*' carefully :)")
        print("")
        for cmd, elems in self.cmd.iteritems():
            print("\t$>%s %s"% (cmd, elems[1]))

    def run_imp(self, module):
        mod = self.import_module(module)
        if (not mod):
            print("Failed to import Module: %s"% module)
            return
        for cmd, elems in mod.iteritems():
            if (cmd in self.cmd):
                print("Command: '%s' is already defined"% cmd)
                return
        print("Module Loaded: %s"% module)
        for cmd, elems in mod.iteritems():
            print("\t$>%s %s"% (cmd, elems[1]))
            CMDS.append(cmd)
        self.cmd.update(mod)

    def run_pff(self, fname):
        self.run_pf(fname, full=True)

    def run_pf(self, fname, full=False):
        if (fname[0] != '/'):
            fname = PATH + fname
        classes = self.get_class_by_filename(fname)
        if not classes:
            print("No results for File: '%s'"% fname)
            return
        for classe in classes:
            child_classes = self.get_child_class([ classe ])
            stats.display_class(classe, full, child_classes)

    def run_pcf(self, classe):
        self.run_pc(classe, full=True)

    def run_pc(self, classe, full=False):
        classes = self.get_class_by_name(classe)
        if not classes:
            print("No results for Class: '%s'"% classe)
            return
        for classe in classes:
            child_classes = self.get_child_class([ classe ])
            stats.display_class(classe, full, child_classes)

    def run_sc(self, classe):
        classes = self.get_class_by_name(classe)
        if not classes:
            print("No results for Class: '%s'"% classe)
            return
        for classe in classes:
            print(classe.name)

    def run_sf(self, fname):
        res = []
        if (fname[0] != '/'):
            fname = PATH + fname
        classes = self.get_class_by_filename(fname)
        if not classes:
            print("No results for File: '%s'"% fname)
            return
        for classe in classes:
            if classe.filename not in res:
                res.append(classe.filename)
                print(classe.filename)

    def run_sm(self, meths):
        for classe in self.classes:
            all_meths = classe.funcs + classe.meths
            for meth in all_meths:
                if fnmatch.fnmatch(meth[4].lower(), meths.lower()):
                    print("\t%s: %s"% (classe.name, meth[0]))
            all_Omeths = classe.Ofuncs + classe.Omeths
            for Ometh in all_Omeths:
                if fnmatch.fnmatch(Ometh[4].lower(), meths.lower()):
                    print("\t%s: %s FROM: %s"% (classe.name, Ometh[0],  Ometh[5]))

    def run_cd(self, directory=None):
        global PATH

        if not directory:
            tmp = SIXAnalyzer_options.path
        elif directory == "..":
            if PATH[len(PATH) - 1] == '/':
                i = -2
            else:
                i = -1
            tmp = "/".join(PATH.split("/")[:i]) + '/'
        else:
            if (directory[0] != '/'):
                tmp = os.path.join(PATH, directory)
            else:
                tmp = directory
        if tmp.startswith(SIXAnalyzer_options.path):
            PATH = tmp

    def run_graph(self, fname):
        try:
            A = pgv.AGraph(directed=True, strict=True, rankdir='LR', ranksep='0.1', concentrate=True)
            A.node_attr['style'] ='filled'
            A.node_attr['color'] = 'green'
            A.node_attr['fontcolor']='black'
            A.edge_attr.update(len='0.2',color='blue')
            for classe in self.classes:
                if classe.filename.startswith(PATH):
                    for inh in classe.orig_inherits:
                        if (inh != classe.name):
                            A.add_edge(inh, classe.name)
            A.write(fname + '.dot')
            B = pgv.AGraph(fname + '.dot')
            B.layout(prog='dot')
            B.draw(fname + '.png')
        except:
            print("Unable to generate %s graph"% fname)

    def run(self):
        reader = Reader(self)
        while (True):
            try:
                line = reader.get_line()
                if not line:
                    continue
                if (line == "help"):
                    self.run_help()
                    continue
                line = reader.check_line(line)
                tokens = line.split()
                cmd = tokens[0]
                line = ' '.join(tokens[1:])
                if cmd in self.cmd:
                    if (len(line) <= 0 and self.cmd[cmd][2]):
                        print("Command '%s' needs a parameter"% cmd)
                        continue
                    self.cmd[cmd][0](line)
                else:
                    print("Unknow Command")
                    continue
            except SystemExit as e:
                sys.exit(e)
            #removed for debug
            # except:
            #     continue
