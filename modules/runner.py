#!/usr/bin/python

import concurrent.futures

from builder import SIXAnalyzer_builder
from finder import SIXAnalyzer_finder
import files
import stats

class SIXAnalyzer_runner():
    def __init__(self):
        with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
            future_files = executor.submit(files.get_files)
            future_header_files = executor.submit(files.get_header_files)
            self.files = future_files.result()
            self.header_files = future_header_files.result()
        self.builder = SIXAnalyzer_builder(self.files, self.header_files)

    def run(self):
        self.builder.init()
        stats.display(self.builder.get_classes(), self.files, self.header_files)
        self.builder.run()
        stats.display(self.builder.get_classes(), self.files, self.header_files)
        self.finder = SIXAnalyzer_finder(self.builder.get_classes())
        self.finder.run()
