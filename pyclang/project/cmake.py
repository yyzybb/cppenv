#!/usr/bin/python

import os
import sys
import re

class cmake:
    def __init__(self):
        pass

    def get_includes(self, cmakefile):
        ret = []
        with open(cmakefile, 'r') as f:
            info_list = f.readlines()
            for s in info_list:
                if not s.strip().upper().startswith('INCLUDE_DIRECTORIES'):
                    continue

                r = re.match(r'\s*include_directories\("([^"]+)"\)\s*', s, re.IGNORECASE)
                if r.group(0) != s:
                    continue

                ret.append(r.group(1))

        for i in range(len(ret)):
            if not ret[i].startswith('/'):
                ret[i] = os.path.join(os.path.dirname(cmakefile), ret[i])

        return ret

g_cmake_parser = cmake()

