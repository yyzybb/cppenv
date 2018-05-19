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

_debug = 1

def Log(msg):
    if not _debug:
        return 

    f = open("/tmp/ycm_conf.log", 'a+')
    f.write(msg + '\n')
    f.close()

# These are the compilation flags that will be used in case there's no
# compilation database set (by default, one is not set).
# CHANGE THIS LIST OF FLAGS. YES, THIS IS THE DROID YOU HAVE BEEN LOOKING FOR.
flags = [
'-Wall',
'-Wextra',
'-Werror',
#'-Wc++98-compat',
'-Wno-long-long',
'-Wno-variadic-macros',
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
#'-isystem',
#'/usr/include/c++/v1',
#'-isystem',
#'/usr/include',
#'-isystem',
#'/usr/local/include',
]

gcc_search_dirs = ''
if os.path.isfile('/tmp/gcc_search_dirs'):
    f = open('/tmp/gcc_search_dirs', 'r')
    gcc_search_dirs = f.read().strip()
    f.close()

if gcc_search_dirs == '':
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
    f = open('/tmp/gcc_search_dirs', 'w')
    f.write(gcc_search_dirs)
    f.close()

Log('gcc_search_dirs:' + gcc_search_dirs)
dirs = gcc_search_dirs.split('\n')
for d in dirs:
    d = d.strip()
    if d == '':
        continue
    flags.append('-isystem')
    flags.append(d)

gcc_version = os.popen('gcc --version | head -1 | cut -d\) -f2 | awk \'{print $1}\'').read().strip()
Log('gcc_version:' + gcc_version)

env_cpath = os.environ.get("CPATH")
if env_cpath:
    cpaths = env_cpath.split(':')
    for cpath in cpaths:
        if cpath == '':
            continue

        flags.append("-I")
        flags.append(cpath)

flags.extend([
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

# Set this to the absolute path to the folder (NOT the file!) containing the
# compile_commands.json file to use that instead of 'flags'. See here for
# more details: http://clang.llvm.org/docs/JSONCompilationDatabase.html
#
# You can get CMake to generate this file for you by adding:
#   set( CMAKE_EXPORT_COMPILE_COMMANDS 1 )
# to your CMakeLists.txt file.
#
# Most projects will NOT need to set this to anything; you can just change the
# 'flags' list of compilation flags. Notice that YCM itself uses that approach.
compilation_database_folder = ''

if os.path.exists( compilation_database_folder ):
  database = ycm_core.CompilationDatabase( compilation_database_folder )
else:
  database = None

SOURCE_EXTENSIONS = [ '.cpp', '.cxx', '.cc', '.c', '.m', '.mm' ]

def DirectoryOfThisScript():
  Log("__file__ is %s" % __file__)
  Log("__file__ abspath is %s" % os.path.abspath( __file__ ))
  return os.path.dirname( os.path.abspath( __file__ ) )


def MakeRelativePathsInFlagsAbsolute( flags, working_directory ):
  Log(working_directory)

  if not working_directory:
    return list( flags )
  new_flags = []
  make_next_absolute = False
  path_flags = [ '-isystem', '-I', '-iquote', '--sysroot=' ]
  for flag in flags:
    new_flag = flag

    if make_next_absolute:
      make_next_absolute = False
      if not flag.startswith( '/' ):
        new_flag = os.path.join( working_directory, flag )

    for path_flag in path_flags:
      if flag == path_flag:
        make_next_absolute = True
        break

      if flag.startswith( path_flag ):
        path = flag[ len( path_flag ): ]
        new_flag = path_flag + os.path.join( working_directory, path )
        break

    if new_flag:
      new_flags.append( new_flag )
  
  return new_flags


def IsHeaderFile( filename ):
  extension = os.path.splitext( filename )[ 1 ]
  return extension in [ '.h', '.hxx', '.hpp', '.hh' ] #or extension.startswith('/usr/include')


def GetCompilationInfoForFile( filename ):
  # The compilation_commands.json file generated by CMake does not have entries
  # for header files. So we do our best by asking the db for flags for a
  # corresponding source file, if any. If one exists, the flags for that file
  # should be good enough.
  if IsHeaderFile( filename ):
    basename = os.path.splitext( filename )[ 0 ]
    for extension in SOURCE_EXTENSIONS:
      replacement_file = basename + extension
      if os.path.exists( replacement_file ):
        compilation_info = database.GetCompilationInfoForFile(
          replacement_file )
        if compilation_info.compiler_flags_:
          return compilation_info
    return None
  return database.GetCompilationInfoForFile( filename )


## Add includes flags from the Makefile.
#

def ExtractIncludesFromMakefile(path):
    Log('ExtractIncludesFromMakefile')
    include_flags = set()
    make_commands = os.popen('cd %s && make -Bn 2>/dev/null' % path, 'r').read()
    #Log('Make commands:\n%s' % make_commands);
    matchs = re.findall(r'-I\s*[^\s$]+', make_commands)
    for m in matchs:
        include_path = m[2:].strip()
        if not os.path.isabs(include_path):
            include_path = os.path.join(path, include_path)
        include_flags.add(include_path)

    return include_flags

def MakefileIncludesFlags(filename):
    Log('MakefileIncludesFlags')
    mk_flags = []
    makefile_list = ['Makefile', 'makefile', 'build/Makefile', 'build/makefile']
    mk = findProjectFile(filename, makefile_list)
    if not mk:
        return mk_flags

    include_flags = ExtractIncludesFromMakefile(os.path.dirname(mk))
    for flag in include_flags:
        mk_flags.append('-I')
        mk_flags.append(flag)

    Log(str(mk_flags))
    return mk_flags

# TODO: use cmake command: -DCMAKE_EXPORT_COMPILE_COMMANDS=ON to make json file.
def ExtractIncludesFromCMake(cmk, filename):
    Log('ExtractIncludesFromCMake')
    cmk_dir = os.path.dirname(cmk)
    tmp_dir = '/tmp' + cmk_dir
    Log("cmake_dir:%s, tmp_dir:%s, filename:%s" % (cmk_dir, tmp_dir, filename))
    ign = os.popen("mkdir -p %s && cd %s && cmake %s -DCMAKE_EXPORT_COMPILE_COMMANDS=ON" % (tmp_dir, tmp_dir, cmk_dir)).read()
    json_file = os.path.join(tmp_dir, "compile_commands.json")
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
    for unit in js:
        if not matcher(unit):
            continue

        command = unit.get("command")
        cmd_elems = command.split(" ")
        for elem in cmd_elems:
            if len(elem) > 2 and elem[:2] == '-I':
                #Log("Add elem:{%s}" % elem)
                includes.append(elem[2:])

    return list(set(includes))

def CMakeIncludesFlags(filename):
    Log('CMakeIncludesFlags')
    try:
        flags = []
        cmk = findProjectFile(filename, ['CMakeLists.txt'])
        if not cmk:
            Log("Not find CMakeLists.txt")
            return flags

        includes = ExtractIncludesFromCMake(cmk, filename)
        for include in includes:
            flags.append('-I')
            flags.append(include)
    except:
        Log(traceback.format_exc())

    Log(str(flags))
    return flags

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
                Log("check:" + pf)
                if os.path.isfile(pf):
                    return pf
    except:
        Log(traceback.format_exc())
    return

def FlagsForFile( filename, **kwargs ):
  Log("Process file: %s" % filename)
  Log("WorkDirectory is: %s" % os.getcwd())
  if database:
    Log('database case:')
    # Bear in mind that compilation_info.compiler_flags_ does NOT return a
    # python list, but a "list-like" StringVec object
    compilation_info = GetCompilationInfoForFile( filename )
    if not compilation_info:
      return None

    final_flags = MakeRelativePathsInFlagsAbsolute(
      compilation_info.compiler_flags_,
      compilation_info.compiler_working_dir_ )

    # NOTE: This is just for YouCompleteMe; it's highly likely that your project
    # does NOT need to remove the stdlib flag. DO NOT USE THIS IN YOUR
    # ycm_extra_conf IF YOU'RE NOT 100% SURE YOU NEED IT.
    try:
      final_flags.remove( '-stdlib=libc++' )
    except ValueError:
      pass
  else:
    Log('no database case:')
    #relative_to = DirectoryOfThisScript()
    relative_to = '/etc/vim/bundle/YouCompleteMe/third_party/ycmd/cpp/ycm'
    final_flags = MakeRelativePathsInFlagsAbsolute( flags, relative_to )

  final_flags.extend(['-I', os.path.dirname(filename)])
  final_flags.extend(MakefileIncludesFlags(filename))
  final_flags.extend(CMakeIncludesFlags(filename))

  Log(str(final_flags))

  return {
    'flags': final_flags,
    'do_cache': True
  }


if __name__ == '__main__':
    # test mk_flags
    print MakefileIncludesFlags('/home/yyz/cloud/sip/mpush/main.cpp')
