import reader, fnmatch, sys

import stats

class SIXAnalyzer_finder():
    def __init__(self, classes):
        self.classes = classes
        self.cmd = { "pc": self.run_pc, "pf": self.run_pf, "sc": self.run_sc, "sf": self.run_sf }

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

    def run_pf(self, fname):
        classes = self.get_class_by_filename(fname)
        if not classes:
            print("No results for File: '%s'"% fname)
            return
        for classe in classes:
            stats.display_class(classe)

    def run_pc(self, classe):
        classes = self.get_class_by_name(classe)
        if not classes:
            print("No results for Class: '%s'"% classe)
            return
        for classe in classes:
            stats.display_class(classe)

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
                line = reader.check_line(line)
                cmd = line[:2]
                if (cmd not in self.cmd):
                    print("Unknow Command")
                    continue
                line = line[3:]
                if (len(line) <= 0):
                    print("Command '%s' needs a parameter"% cmd)
                    continue
                self.cmd[cmd](line)
            except SystemExit as e:
                sys.exit(e)
            except:
                continue
