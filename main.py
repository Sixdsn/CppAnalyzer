#!/usr/bin/python

import sys

sys.path[0] += "/modules"

from rules import SIXAnalyzer_rules

SIXAnalyzer_rules.init()

from runner import SIXAnalyzer_runner

Six = SIXAnalyzer_runner()
Six.run()
