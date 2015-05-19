import sys, os, re, readline, fnmatch, glob

import finder

RE_SPACE = re.compile('.*\s+$', re.M)

class Completer(object):
    def __init__(self, finder):
        self.classes = finder.classes
        self.modules_loaded = finder.modules_loaded

    def get_files(self):
        res = []
        for elem in self.classes:
            if elem.filename not in res and elem.filename.startswith(finder.PATH):
                res.append(elem.filename)
        return res

    def get_classes(self):
        res = []
        for elem in self.classes:
            if elem.name not in res and elem.filename.startswith(finder.PATH):
                res.append(elem.name)
        return res

    def _listdir(self, root):
        res = []
        for name in os.listdir(root):
            path = os.path.join(root, name)
            if os.path.isdir(path):
                name += os.sep
                res.append(name)
        return res

    def _complete_cd(self, path=None):
        if not path:
            return self._listdir(finder.PATH)
        dirname, rest = os.path.split(path)
        tmp = dirname if dirname else finder.PATH
        res = [os.path.join(dirname, p)
               for p in self._listdir(tmp) if p.startswith(rest)]
        if len(res) > 1 or not os.path.exists(path):
            return res
        if os.path.isdir(path):
            return [os.path.join(path, p) for p in self._listdir(path)]
        return [path + ' ']

    def _complete_files(self, args):
        return [ f.split(finder.PATH)[1] for f in self.get_files() if f.startswith(finder.PATH + args[-1]) ]

    def _complete_classes(self, args):
        return [ f for f in self.get_classes() if f.startswith(args[-1]) ]

    def _complete_sm(self, meths):
        res = []
        meth_arg = meths[-1]
        for classe in self.classes:
            all_meths = classe.funcs + classe.meths
            for meth in all_meths:
                if meth[4].lower().startswith(meth_arg.lower()):
                    res.append(meth[4])
            all_Omeths = classe.Ofuncs + classe.Omeths
            for Ometh in all_Omeths:
                if Ometh[4].lower().startswith(meth_arg.lower()):
                    res.append(Ometh[4])
        return res

    def complete_graph(self, args):
        if not args or args[0] == '':
            return self._complete_cd(finder.PATH)
        if len(args) == 1:
            return self._complete_cd(args[0])
        return self._complete_classes(args[1:])

    def complete_cd(self, args):
        if not args or args[0] == '':
            return self._complete_cd(finder.PATH)
        return self._complete_cd(args[-1])

    #class
    def complete_pc(self, args):
        return self._complete_classes(args)
    def complete_pcf(self, args):
        return self._complete_classes(args)
    def complete_sc(self, args):
        return self._complete_classes(args)

    #file
    def complete_pf(self, args):
        return self._complete_files(args)
    def complete_pff(self, args):
        return self._complete_files(args)
    def complete_sf(self, args):
        return self._complete_files(args)

    #meths
    def complete_sm(self, args):
        return self._complete_sm(args)

    #module
    def complete_imp(self, args):
        arg = args[-1]
        path = './'
        if arg:
            if os.path.isdir(arg):
                path = arg
            else:
                path = os.path.dirname(arg)
        if not len(path) or path == '.':
            path = "./"
        if path[-1] != '/':
            path += '/'
        files = [ path + f for f in os.listdir(path) ]
        filenames = fnmatch.filter(files, '*.py')
        filenames += fnmatch.filter(files, '*.pyc')
        res = [ f + '/' for f in files if os.path.isdir(f) and (f.startswith(arg) or f.startswith('./' + arg))]
        for filename in filenames:
            if arg:
                fname = filename
                if fname.startswith(arg) or fname.startswith('./' + arg):
                    res.append(fname)
            else:
                res.append(filename)
        return res

    def complete_reload(self, args):
        return [ f for f in self.modules_loaded if f.startswith(args[-1]) ]

    def complete(self, text, state):
        buffer = readline.get_line_buffer()
        line = readline.get_line_buffer().split()
        if not line:
            return [c + ' ' for c in finder.CMDS][state]
        if RE_SPACE.match(buffer):
            line.append('')
        cmd = line[0].strip()
        if cmd in finder.CMDS:
            impl = getattr(self, 'complete_%s' % cmd)
            args = line[1:]
            if args:
                return (impl(args) + [None])[state]
            return [cmd + ' '][state]
        results = [c + ' ' for c in finder.CMDS if c.startswith(cmd)] + [None]
        return results[state]

class Reader():

    def __init__(self, classes):
        self.comp = Completer(classes)

    def get_line(self):
        try:
            readline.set_completer_delims(' \t\n;')
            readline.parse_and_bind("tab: complete")
            readline.set_completer(self.comp.complete)
            return (raw_input("Analyze$> "))
        except:
            print("use quit or exit to exit")
            return (None)

    def check_line(self, line):
        if (line == "exit" or line == "quit"):
            sys.exit(0)
        return line
