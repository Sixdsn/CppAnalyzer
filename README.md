CppAnalyser
===========

Parse your CPP class definitions and analyse it

This CLI Tool is using the CppHeaderParser Module available here:

https://pypi.python.org/pypi/CppHeaderParser/

This module is developped by senex (Jashua Cloutier) who does a real good job on it :)

You just need to install it
```
$>pip install cppheaderparser
```

Requirements (for graph export):
```
$> apt-get install libgraphviz-dev python-dev graphviz
$> pip install pygraphviz
```

CppAnalyzer is a script based on the [MOZ_OVERRIDE](https://github.com/Sixdsn/MOZ_OVERRIDE) tool
I developped for Mozilla wich recreates the whole heritage tree for all classes in mozilla-central.

It can be used on any folder containing C++ Code.

Usage:

`./main.py Path [-v|-d] [-h|--help] [-J Workers] [-I header_folder]`

> Path		  => Path to the files you want to add MOZ_OVERRIDE

> -v 		  => Verbose Mode

> -d 		  => Debug Mode

> -h		  => Obvious

> -J      => Number of parallel workers used to parse and generate the database (be carreful, it's using processes so memory usage is very important)

> -I header_folder  => Another path to parse header files very usefull if some of your classes in Path included files that aren't in the same folder


CLI Commands:

```
All parameters are interepreted as regex
But use '*' carefully :)

$>cd	 [folder]     =>Change Folder
$>graph	 [filename]   => Generate Classes Graph
$>imp	 [module]     => Import Module
$>pc	 [classname]  => Shows Basic Class Intels
$>pcf	 [classname]  => Shows All Class Intels
$>pf	 [filename]   => Shows Basic Class Intels contained in Filename
$>pff	 [filename]   => Shows All Class Intels contained in Filename
$>reload [module]     => Reimport Module
$>sc	 [classname]  => Search Class
$>sf	 [filename]   => Search Files
$>six	 [Message]    => Print Message
$>sm	 [method]     => Search Methods
```

Modules:

CppAnalyzer will try to load all modules from the services/ folder at startup.

You can add any other personnal module by using the "imp" command and giving it the module path (absolute or relative)

Module MUST have a init() function that return a dict containing the "Command" as key and a list containing the function to call and the message to print within the "help" command.

There is an example in services/six.py


Graph Export:
```
Analyze$> graph /tmp/example
```

Will generate the hierarchy graph for classes inside CWD in /tmp/example.png (/tmp/example.dot for the original dot file)

![Graph Export Example](http://sixdsn.github.io/images/CppAnalyser_Example.png)

Of course feel free to open a issue if you want a new command/feature or if you have a question
