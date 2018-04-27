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

_debug = 1

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
'-isystem',
'/usr/include',
'-isystem',
'/usr/lib/llvm-3.5/lib/clang/3.5/include',
'-isystem',
'/usr/include/x86_64-linux-gnu',
'-isystem',
'/usr/include/x86_64-linux-gnu/c++/4.8',
'-isystem',
'/usr/include/i386-linux-gnu',
'-isystem',
'/usr/include/c++/4.7',
'-isystem',
'/usr/include/c++/4.8',
'-isystem',
'/usr/include/c++/4.9',
'-isystem',
'/usr/include/c++/5.0',
'-isystem',
'/usr/include/c++/5.1',
'-isystem',
'/usr/include/c++/5.2',
'-isystem',
'/usr/include/i386-linux-gnu/c++/4.8',
'-isystem',
'/usr/local/include',
'-isystem',
'/usr/include/linux',
'-isystem',
'/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/../lib/c++/v1',
'-isystem',
'/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/include',
'-include',
'/usr/include/c++/4.7/cstddef',
'-include',
'/usr/include/c++/4.8/cstddef',
'-include',
'/usr/include/c++/4.9/cstddef',
'-include',
'/usr/include/c++/5.0/cstddef',
'-include',
'/usr/include/c++/5.1/cstddef',
'-include',
'/usr/include/c++/5.2/cstddef',
'-include',
'/usr/include/stdint.h',
'-include',
'cstddef',
'-include',
'stdint.h',
]

def Log(msg):
    if not _debug:
        return 

    f = open("/tmp/ycm_conf.log", 'a+')
    f.write(msg + '\n')
    f.close()

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
  return extension in [ '.h', '.hxx', '.hpp', '.hh' ]


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
makefile_list = ['Makefile', 'makefile', '../Makefile', '../makefile', 'build/Makefile', '../build/Makefile', '../../Makefile', '../../makefile']

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
    path = os.path.split(filename)[0]
    for mk in makefile_list:
        abs_mk = os.path.join(path, mk) 
        if not os.path.isfile(abs_mk):
            continue

        include_flags = ExtractIncludesFromMakefile(os.path.split(abs_mk)[0])
        for flag in include_flags:
            mk_flags.append('-I')
            mk_flags.append(flag)

        break

    Log(str(mk_flags))
    return mk_flags

def ExtractIncludesFromCMake(cmk):
    Log('ExtractIncludesFromCMake')
    cmk_dir = os.path.dirname(cmk)
    args_dict = {
            'CMAKE_SOURCE_DIR' : cmk_dir,
            'CMAKE_BINARY_DIR' : cmk_dir,
            'PROJECT_SOURCE_DIR' : cmk_dir,
            'PROJECT_BINARY_DIR' : cmk_dir,
            }
    includes = []
    set_c = 0
    include_c = 0
    with open(cmk, 'r') as f:
        fileinfo = f.read()
        for it in re.finditer(r'\s*set\s*\(([^"]+)\s+(.*)\)\s*', fileinfo, re.IGNORECASE):
            set_c += 1
            args_dict[it.group(1).strip().upper()] = it.group(2).strip().strip('"')

        for it in re.finditer(r'\s*include_directories\s*\((.*)\)\s*', fileinfo, re.IGNORECASE):
            include_c += 1
            d = it.group(1).strip().strip('"')
            while True:
                finded = False
                for it in re.finditer(r'\$\{(.*)\}', d):
                    finded = True
                    k = it.group(1).upper()
                    v = args_dict.get(k)
                    if not v:
                        Log('unkown key: %s, when parse %s' % (k, cmk))
                        finded = False
                        break

                    d = d.replace(it.group(0), v)

                if not finded:
                    break

            if not os.path.isabs(d):
                d = os.path.join(cmk_dir, d)
            includes.append(d)

    Log('set_c=%s, include_c=%s' % (set_c, include_c))
    return includes

def CMakeIncludesFlags(filename):
    Log('CMakeIncludesFlags')
    try:
        flags = []
        cmake_filename = 'CMakeLists.txt'
        for deep in range(3):
            cmk = os.path.dirname(filename)
            for i in range(deep):
                cmk = os.path.dirname(cmk)
            cmk = os.path.join(cmk, cmake_filename)
            isfile = os.path.isfile(cmk)
            Log('test isfile %s: %s' % (cmk, isfile))
            if not isfile:
                continue

            includes = ExtractIncludesFromCMake(cmk)
            for include in includes:
                flags.append('-I')
                flags.append(include)
            break
    except:
        Log(traceback.format_exc())

    Log(str(flags))
    return flags

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
