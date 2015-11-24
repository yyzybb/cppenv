#!/usr/bin/python

import os
import re

class finder:
    def __init__(self):
        self.cache = {}

    def find_cmake(self, start_path):
        return self.find(start_path, r'CMakeLists\.txt')

    def find_makefile(self, start_path):
        return self.find(start_path, r'[mM]akefile')

    def find(self, start_path, project_file_pattern):
        if self.cache.has_key(start_path):
            c2 = self.cache[start_path]
            if c2.has_key(project_file_pattern):
                return c2[project_file_pattern]

        path = start_path
        while True:
            for p in os.listdir(path):
                abs_p = os.path.join(path, p)
                if not os.path.isfile(abs_p):
                    continue

                r = re.match(project_file_pattern, p, 0)
                if r.group(0) == p:
                    self.cache[start_path][project_file_pattern] = abs_p
                    return abs_p

            parent = os.path.dirname(path)
            if path == parent:
                break

            path = parent
        
        return ''

    def findall(self, start_path):
        cmake_f = self.find_cmake(start_path)
        if cmake_f:
            return cmake_f

        return self.find_makefile(start_path)

project_finder = finder()

