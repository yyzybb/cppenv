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
import ycm_core
import re
import traceback
import json
import dbm
import time

_debug = 1

def Log(msg):
    if not _debug:
        return 

    f = open("/tmp/ycm_conf.log", 'a+')
    f.write(msg + '\n')
    f.close()

g_home = os.environ.get("HOME")
g_tmp_dir = os.path.join(g_home, '.vim.git')
g_time_format = '%Y-%m-%dT%H:%M:%S'
db = dbm.open(os.path.join(g_tmp_dir, 'ycm.db'), "c")
Log("db keys:%s" % str(db.keys()))

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

gcc_search_dirs = db.get('gcc_search_dirs')

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
    db['gcc_search_dirs'] = gcc_search_dirs

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

SOURCE_EXTENSIONS = [ '.cpp', '.cxx', '.cc', '.c', '.m', '.mm' ]

## Add includes flags from the Makefile.
#
def ExtractIncludesFromMakefile(path):
    Log('ExtractIncludesFromMakefile(path="%s")' % path)

    cache_name = 'Makefile-%s' % path
    cache_dct = GetCacheDict(cache_name)
    if cache_dct:
        Log(" -> Makefile use cache!")
        make_commands =  cache_dct.get('commands')
    else:
        make_commands = os.popen('cd %s && make -Bn 2>/dev/null' % path, 'r').read()
        SetCacheDict(cache_name, {'commands':make_commands}, [path])

    #Log('Make commands:\n%s' % make_commands);
    matchs = re.findall(r'-I\s*[^\s$]+', make_commands)
    include_flags = set()
    for m in matchs:
        include_path = m[2:].strip()
        if not os.path.isabs(include_path):
            include_path = os.path.join(path, include_path)
        include_flags.add(include_path)

    return include_flags

def MakefileIncludesFlags(filename):
    Log('MakefileIncludesFlags(filename="%s")' % filename)

    makefile_list = ['Makefile', 'makefile', 'build/Makefile', 'build/makefile']
    mk = findProjectFile(filename, makefile_list)
    if not mk:
        return [], ''

    include_flags = ExtractIncludesFromMakefile(os.path.dirname(mk))
    mk_flags = []
    for flag in include_flags:
        mk_flags.append('-I')
        mk_flags.append(flag)

    return mk_flags, mk

def ExtractIncludesFromCMake(cmk, filename):
    Log('ExtractIncludesFromCMake')
    cmk_dir = os.path.dirname(cmk)
    tmp_dir = '/tmp' + cmk_dir
    Log("cmake_dir:%s, tmp_dir:%s, filename:%s" % (cmk_dir, tmp_dir, filename))
    ign = os.popen("mkdir -p %s && cd %s && cmake %s -DCMAKE_EXPORT_COMPILE_COMMANDS=ON" % (tmp_dir, tmp_dir, cmk_dir)).read()
    json_file = os.path.join(tmp_dir, "compile_commands.json")
    if not os.path.isfile(json_file):
        return []

    f = open(json_file, 'r')
    strjs = f.read()
    f.close()

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
            return [], ''

        includes = ExtractIncludesFromCMake(cmk, filename)
        return includes, cmk
    except:
        Log(traceback.format_exc())

    return [], ''

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

def GetCacheDict(cache_name):
    cache_str = db.get(cache_name)
    if cache_str:
        # dict: {xxxx:xxxx, 'depends':{'filename':'mtime'}}
        cache_dct = eval(cache_str)
        dep_dct = cache_dct.get('depends')
        valid_cache = True
        if dep_dct:
            for f in dep_dct.keys():
                mtime = dep_dct.get(f)
                if not CheckDependFileMTime(f, mtime):
                    valid_cache = False
                    break

        if valid_cache:
            return cache_dct
    return None

def SetCacheDict(cache_name, dct, depfiles):
    if len(depfiles) > 0:
        if not dct.has_key('depends'):
            dct['depends'] = {}
        for f in depfiles:
            dct['depends'][f] = GetFileMTime(f)

    db[cache_name] = str(dct)

def GetIncludesDirectories(filename, func, cache_name_leader):
    dirs = []
    cache_name = cache_name_leader + '-' + filename
    cache_dct = GetCacheDict(cache_name)
    if cache_dct:
        Log(" -> file:%s Project:%s use cache!" % (filename, cache_name_leader))
        return cache_dct.get('I')

    dirs, mk = func(filename)
    if len(dirs) == 0:
        return dirs

    SetCacheDict(cache_name, {'I': dirs}, [mk])
    return dirs

def FlagsForFile( filename, **kwargs ):
    Log("-------------- %s --------------" % filename)
    Log("WorkDirectory is: %s" % os.getcwd())
    final_flags = flags
    final_flags.extend(['-I', os.path.dirname(filename)])
  
    # parse makefile
    makefile_include_dirs = GetIncludesDirectories(filename, MakefileIncludesFlags, 'cpp-Makefile')
    Log("Makfile include direcotires: %s" % makefile_include_dirs)
    for d in makefile_include_dirs:
        final_flags.append('-I')
        final_flags.append(d)

    # parse cmake
    cmake_include_dirs = GetIncludesDirectories(filename, CMakeIncludesFlags, 'cpp-CMake')
    Log("CMake include direcotires: %s" % cmake_include_dirs)
    for d in cmake_include_dirs:
        final_flags.append('-I')
        final_flags.append(d)
  
    final_flags.extend(sysflags)
  
    Log("final_flags:")
    Log(str(final_flags))
    Log("build command:")
  
    cmd = 'g++ -std=c++0x -c %s ' % filename
    cmd += ' '.join(final_flags)
    Log(cmd)
    Log("-------------- Done [%s] --------------" % filename)
  
    return {
      'flags': final_flags,
      'do_cache': True
    }

if __name__ == '__main__':
    # test mk_flags
    print FlagsForFile(os.path.join(g_home, 'test/a.cpp'))
