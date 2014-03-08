import reader, fnmatch, sys

import stats

class SIXAnalyzer_finder():
    def __init__(self, classes):
        self.classes = classes
        self.cmd = { "pc": [ self.run_pc, "[classname] => Shows Basic Class Intels" ], \
                     "pcf": [ self.run_pcf, "[classname] => Shows All Class Intels" ], \
                     "pf": [ self.run_pf, "[filename] => Shows Basic Class Intels contained in Filename"], \
                     "pff": [ self.run_pff, "[filename] => Shows All Class Intels contained in Filename"], \
                     "sc": [ self.run_sc, "[classname] => Search Class" ], \
                     "sf": [ self.run_sf, "[filename] => Shows Files" ] }

    def get_class_by_name(self, classname):
        res = [ elem for elem in self.classes if fnmatch.fnmatch(elem.name, classname) ]
        if (len(res) == 0):
            return (None)
        return (sorted(res, key=lambda classe: classe.name.lower()))

    def get_class_by_filename(self, filename):
        res = [ elem for elem in self.classes if fnmatch.fnmatch(elem.filename, filename) ]
        if (len(res) == 0):
            return (None)
        return (sorted(res, key=lambda classe: (classe.filename.lower(), classe.name.lower())))

    def get_child_class(self, classes):
        res = []
        for classe in classes:
            for cl in self.classes:
                if classe.name in cl.inherits:
                    res.extend(self.get_class_by_name(cl.name))
        return (res)

    def run_help(self):
        print("All parameters are interepreted as regex")
        print("But use '*' carefully :)")
        print("")
        for cmd, elems in self.cmd.iteritems():
            print("\t$>%s %s"% (cmd, elems[1]))

    def run_pff(self, fname):
        self.run_pf(fname, full=True)

    def run_pf(self, fname, full=False):
        classes = self.get_class_by_filename(fname)
        if not classes:
            print("No results for File: '%s'"% fname)
            return
        child_classes = self.get_child_class(classes)
        for classe in classes:
            stats.display_class(classe, full, child_classes)

    def run_pcf(self, classe):
        self.run_pc(classe, full=True)

    def run_pc(self, classe, full=False):
        classes = self.get_class_by_name(classe)
        if not classes:
            print("No results for Class: '%s'"% classe)
            return
        child_classes = self.get_child_class(classes)
        for classe in classes:
            stats.display_class(classe, full, child_classes)

    def run_sc(self, classe):
        classes = self.get_class_by_name(classe)
        if not classes:
            print("No results for Class: '%s'"% classe)
            return
        for classe in classes:
            print(classe.name)

    def run_sf(self, fname):
        classes = self.get_class_by_filename(fname)
        if not classes:
            print("No results for File: '%s'"% fname)
            return
        for classe in sorted(set(classes)):
            print(classe.filename)

    def run(self):
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
                if (cmd not in self.cmd):
                    print("Unknow Command")
                    continue
                line = ' '.join(tokens[1:])
                if (len(line) <= 0):
                    print("Command '%s' needs a parameter"% cmd)
                    continue
                self.cmd[cmd][0](line)
            except SystemExit as e:
                sys.exit(e)
            #removed for debug
            # except:
            #     continue
