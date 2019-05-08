#!/usr/bin/python
# -*- coding:utf8 -*-
# This file is NOT licensed under the GPLv3, which is the license for the rest
# of YouCompleteMe.
#
# Here's the license text for this file:
#
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http://unlicense.org/>

import os
import sys
import re
import traceback
import json
import time

# 打印日志
g_debug = 1

# 处理Makefile时是否执行(rm .*.d -f)
g_rm_dot_d_files = 1

# 缓存有效期
g_cmake_cache_valid_seconds = 10
g_makefile_cache_valid_seconds = 10

def Log(msg):
    if not g_debug:
        return 

    f = open("/tmp/ycm_conf.log", 'a+')
    f.write(msg + '\n')
    f.close()

g_home = os.environ.get("HOME")
g_tmp_dir = os.path.join(g_home, '.vim.git/ycm_tmp')
g_time_format = '%Y-%m-%dT%H:%M:%S'

if __name__ == '__main__':
    # clear all cache
    os.popen('rm %s -rf' % g_tmp_dir).read()
    os.makedirs(g_tmp_dir)
    sys.exit(0)

import ycm_core

# These are the compilation flags that will be used in case there's no
# compilation database set (by default, one is not set).
# CHANGE THIS LIST OF FLAGS. YES, THIS IS THE DROID YOU HAVE BEEN LOOKING FOR.
flags = [
#'-Wall',
#'-Wextra',
#'-Werror',
#'-Wc++98-compat',
#'-Wno-long-long',
#'-Wno-variadic-macros',
'-fexceptions',
'-DNDEBUG',
# You 100% do NOT need -DUSE_CLANG_COMPLETER in your flags; only the YCM
# source code needs it.
'-DUSE_CLANG_COMPLETER',
# THIS IS IMPORTANT! Without a "-std=<something>" flag, clang won't know which
# language to use when compiling headers. So it will guess. Badly. So C++
# headers will be compiled as C headers. You don't want that so ALWAYS specify
# a "-std=<something>".
# For a C project, you would set this to something like 'c99' instead of
# 'c++11'.
'-std=c++11',
# ...and the same thing goes for the magic -x option which specifies the
# language that the files to be compiled are written in. This is mostly
# relevant for c++ headers.
# For a C project, you would set this to 'c' instead of 'c++'.
'-x',
'c++',
'-isystem',
'../BoostParts',
'-isystem',
# This path will only work on OS X, but extra paths that don't exist are not
# harmful
'/System/Library/Frameworks/Python.framework/Headers',
'-isystem',
'../llvm/include',
'-isystem',
'../llvm/tools/clang/include',
'-I',
'.',
'-I',
'./ClangCompleter',
'-isystem',
'./tests/gmock/gtest',
'-isystem',
'./tests/gmock/gtest/include',
'-isystem',
'./tests/gmock',
'-isystem',
'./tests/gmock/include',
]

sysflags = []

def readFile(filename):
    if not os.path.isfile(filename):
        return ""

    f = open(filename, 'r')
    s = f.read()
    f.close()
    return s

def readFileLines(filename):
    if not os.path.isfile(filename):
        return []

    f = open(filename, 'r')
    lines = f.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].strip()
    f.close()
    return lines

def writeFile(filename, s):
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    f = open(filename, 'w')
    f.write(s)
    f.close()

def writeFileLines(filename, lines):
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    f = open(filename, 'w')
    for line in lines:
        f.write(line + '\n')
    f.close()

# 计算最后修改时间
def isFileTimeout(temp_file, seconds):
    if not os.path.isfile(temp_file):
        return True

    mt = os.path.getmtime(temp_file)
    now = time.mktime(time.localtime())
    return abs(now - mt) > 5;

# 初始化system flags
def initSysFlags():
    global sysflags

    gcc_search_dirs = ''

    gcc_search = os.path.join(g_tmp_dir, 'gcc_search')
    if os.path.isfile(gcc_search):
        gcc_search_dirs = readFile(gcc_search)

    if not gcc_search_dirs:
        f = open('/tmp/ycm_tmp.cpp', 'w')
        f.write('#include <iostream>\n')
        f.write('main() {}')
        f.close()
        r, w, e = os.popen3('g++ -std=c++11 -v -H /tmp/ycm_tmp.cpp -o /dev/null')
        gcc_search_dirs = e.read()
        start = '#include <...> search starts here:'
        end = 'End of search list.'
        gcc_search_dirs = gcc_search_dirs[gcc_search_dirs.index(start) + len(start):gcc_search_dirs.index(end)]
        gcc_search_dirs = gcc_search_dirs.strip()
        writeFile(gcc_search, gcc_search_dirs)

    Log('gcc_search_dirs:' + gcc_search_dirs)
    dirs = gcc_search_dirs.split('\n')
    for d in dirs:
        d = d.strip()
        if d == '':
            continue
        sysflags.append('-isystem')
        sysflags.append(d)

    gcc_version = os.popen('gcc --version | head -1 | cut -d\) -f2 | awk \'{print $1}\'').read().strip()
    Log('gcc_version:' + gcc_version)

    # use CPATH
    env_cpath = os.environ.get("CPATH")
    if env_cpath:
        cpaths = env_cpath.split(':')
        for cpath in cpaths:
            if cpath == '':
                continue

            sysflags.append("-I")
            sysflags.append(cpath)

    # in Mac and Linux
    sysflags.extend([
        '-isystem',
        '/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/../lib/c++/v1',
        '-isystem',
        '/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/include',
        '-isystem',
        '/usr/include/linux',
        '-isystem',
        '/usr/include/x86_64-linux-gnu',
        '-isystem',
        '/usr/include/i386-linux-gnu',
        ])

initSysFlags()

SOURCE_EXTENSIONS = [ '.cpp', '.cxx', '.cc', '.c', '.m', '.mm' ]

## Add includes flags from the Makefile.
#
def ExtractIncludesFromMakefile(mk, filename):
    Log('ExtractIncludesFromMakefile(mk="%s")' % mk)

    file_dir = os.path.dirname(filename)
    mk_dir = os.path.dirname(mk)
    tmp_dir = g_tmp_dir + mk_dir
    Log("make_dir:%s, tmp_dir:%s, filename:%s" % (mk_dir, tmp_dir, filename))
    temp_file = os.path.join(tmp_dir, 'makefile.commands')

    include_flags = []
    if not isFileTimeout(temp_file, g_makefile_cache_valid_seconds):
        Log("===> match cache file: %s" % temp_file)
        include_flags = readFileLines(temp_file)

    if not include_flags:
        if g_rm_dot_d_files:
            ign = os.popen("rm %s/.*.d -f" % file_dir).read()
        make_commands = os.popen('cd %s && make -Bn 2>/dev/null' % mk_dir, 'r').read()

        #Log('Make commands:\n%s' % make_commands);
        matchs = re.findall(r'-I\s*[^\s$]+', make_commands)
        include_flags = set()
        for m in matchs:
            include_path = m[2:].strip()
            if not os.path.isabs(include_path):
                include_path = os.path.join(mk_dir, include_path)
            include_flags.add(include_path)

        writeFileLines(temp_file, include_flags)

    return include_flags

def MakefileIncludesFlags(filename):
    Log('MakefileIncludesFlags(filename="%s")' % filename)

    makefile_list = ['Makefile', 'makefile', 'build/Makefile', 'build/makefile']
    mk = findProjectFile(filename, makefile_list)
    if not mk:
        return []

    include_flags = ExtractIncludesFromMakefile(mk, filename)
    return include_flags

def ExtractIncludesFromCMake(cmk, filename):
    Log('ExtractIncludesFromCMake')
    cmk_dir = os.path.dirname(cmk)
    tmp_dir = g_tmp_dir + cmk_dir
    Log("cmake_dir:%s, tmp_dir:%s, filename:%s" % (cmk_dir, tmp_dir, filename))
    json_file = os.path.join(tmp_dir, "compile_commands.json")
    if isFileTimeout(json_file, g_cmake_cache_valid_seconds):
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)
        ign = os.popen("cd %s && cmake . %s -DCMAKE_EXPORT_COMPILE_COMMANDS=ON" % (tmp_dir, cmk_dir)).read()
    else:
        Log("===> match cache file: %s" % json_file)
    return ExtractIncludesFromJson(json_file, filename)

def ExtractIncludesFromJson(json_file, filename):
    if not os.path.isfile(json_file):
        Log("Create compile_commands.json failed.")
        return []

    strjs = readFile(json_file)

    #Log("strjs:" + strjs)
    js = json.loads(strjs)
    #Log("object json:" + str(js))

    # 完全匹配
    includes = CMakeJsonMatch(js, lambda unit: unit.get("file") == filename)
    Log("Best Match returns:%s" % len(includes))

    # 尝试匹配对应的.cpp
    cppfile = os.path.splitext(filename)[0] + ".cpp"
    if len(includes) == 0:
        includes = CMakeJsonMatch(js, lambda unit: unit.get("file") == cppfile)
        Log("Match .cpp returns:%s" % len(includes))

    # 匹配同目录下的所有cpp
    d = os.path.dirname(filename)
    if len(includes) == 0:
        includes = CMakeJsonMatch(js, lambda unit: os.path.dirname(unit.get("file")) == d)
        Log("Match directory returns:%s" % len(includes))

    # 整合所有cpp
    if len(includes) == 0:
        includes = CMakeJsonMatch(js, lambda unit: True)
        Log("Match All returns:%s" % len(includes))

    return includes

def CMakeJsonMatch(js, matcher):
    includes = []
    h = {}
    for unit in js:
        if not matcher(unit):
            continue

        command = unit.get("command")
        cmd_elems = command.split(" ")
        for elem in cmd_elems:
            if len(elem) > 2 and elem[:2] == '-I':
                #Log("Add elem:{%s}" % elem)
                d = elem[2:]
                if h.get(d) != None:
                    continue
                h[d] = 1
                includes.append(elem[2:])

    return includes

def CMakeIncludesFlags(filename):
    Log('CMakeIncludesFlags')
    try:
        cmk = findProjectFile(filename, ['CMakeLists.txt'])
        if not cmk:
            Log("Not find CMakeLists.txt")
            return []

        includes = ExtractIncludesFromCMake(cmk, filename)
        return includes
    except:
        Log(traceback.format_exc())

    return []

def findProjectFile(cppfile, pfnames):
    Log('findProjectFile cppfile=%s, project_file_names=%s' % (cppfile, pfnames))
    try:
        d = cppfile
        while True:
            di = os.path.dirname(d)
            if di == d:
                return 

            d = di
            for projectfile in pfnames:
                pf = os.path.join(d, projectfile)
                #Log("check:" + pf)
                if os.path.isfile(pf):
                    return pf
    except:
        Log(traceback.format_exc())
    return

def GetFileMTime(f):
    if os.path.exists(f):
        stat = os.stat(f)
        if stat:
            v = time.localtime(stat.st_mtime)
            time_str = time.strftime(g_time_format, v)
            return time_str
    return ''

def CheckDependFileMTime(f, mtime):
    time_str = GetFileMTime(f)
    return time_str == mtime

def GetIncludesDirectories(filename, func, cache_name_leader):
    dirs, mk = func(filename)
    if len(dirs) == 0:
        return dirs

    return dirs

def FlagsForFile( filename, **kwargs ):
    Log("-------------- %s --------------" % filename)
    Log("WorkDirectory is: %s" % os.getcwd())
    final_flags = flags
    final_flags.extend(['-I', os.path.dirname(filename)])

    # parse cmake
    try:
        cmake_include_dirs = CMakeIncludesFlags(filename)
        Log("CMake include direcotires: %s" % str(cmake_include_dirs))
        for d in cmake_include_dirs:
            final_flags.append('-I')
            final_flags.append(d)
    except:
        Log("parse cmake failed:%s" % traceback.format_exc())
  
    # parse makefile
    try:
        makefile_include_dirs = MakefileIncludesFlags(filename)
        Log("Makfile include direcotires: %s" % str(makefile_include_dirs))
        for d in makefile_include_dirs:
            final_flags.append('-I')
            final_flags.append(d)
    except:
        Log("parse makefile failed:%s" % traceback.format_exc())

    final_flags.extend(sysflags)
  
    Log("file:")
    Log("  %s" % filename)
    Log("final_flags:")
    for i in range(len(final_flags)/2):
        Log("  %s  %s" % (final_flags[i*2], final_flags[i*2 + 1]))
    #Log("build command:")
    #cmd = 'g++ -std=c++0x -c %s ' % filename
    #cmd += ' '.join(final_flags)
    #Log(cmd)
    Log("-------------- Done [%s] --------------" % filename)
  
    return {
      'flags': final_flags,
      'do_cache': True
    }
