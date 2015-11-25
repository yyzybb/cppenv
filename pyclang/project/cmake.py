#!/usr/bin/python

import os
import sys
import re

class cmake:
    def __init__(self):
        pass

    def recursive_replace(self, s, args_dct):
        arg_list = re.findall(r'\$\{(.+?)\}', s, re.IGNORECASE)
        if not arg_list:
            return s

        is_replaced = False
        for arg in arg_list:
            if args_dct.has_key(arg):
                is_replaced = True
                s = s.replace('${%s}' % arg, args_dct.get(arg))

        if not is_replaced:
            return s

        return self.recursive_replace(s, args_dct)

    def get_includes(self, cmakefile):
        ret = []
        with open(cmakefile, 'r') as f:
            info_list = f.readlines()
            arguments = {
                    'PROJECT_SOURCE_DIR' : os.path.split(cmakefile)[0]
                    }

            for s in info_list:
                if s.strip().upper().startswith('SET'):
                    r = re.match(r'\s*set\(([^"]+)\s+(.*)\)\s*', s, re.IGNORECASE)
                    if not r or r.group(0) != s:
                        continue

                    arguments[r.group(1)] = r.group(2).strip().strip('"')
                    
            for s in info_list:
                if s.strip().upper().startswith('INCLUDE_DIRECTORIES'):
                    r = re.match(r'\s*include_directories\("([^"]+)"\)\s*', s, re.IGNORECASE)
                    if not r or r.group(0) != s:
                        continue

                    ret.append(self.recursive_replace(r.group(1), arguments))

        for i in range(len(ret)):
            if not ret[i].startswith('/'):
                ret[i] = os.path.join(os.path.dirname(cmakefile), ret[i])

        return ret

g_cmake_parser = cmake()

if __name__ == '__main__':
    print g_cmake_parser.get_includes('/home/yyz/cloud/sip/kiev/src/CMakeLists.txt')
