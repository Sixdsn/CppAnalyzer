#!/usr/bin/python

import concurrent.futures

from builder import SIXAnalyzer_builder
import files
import stats

class SIXAnalyzer_runner():
    def __init__(self):
        self.classes = []
        with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
            future_files = executor.submit(files.get_files)
            future_header_files = executor.submit(files.get_header_files)
            self.files = future_files.result()
            self.header_files = future_header_files.result()
        self.builder = SIXAnalyzer_builder(self.files, self.header_files)

    def run(self):
        self.classes = self.builder.init()
        stats.display(self.classes, self.files, self.header_files)
        self.builder.run()
        stats.display(self.classes, self.files, self.header_files)
