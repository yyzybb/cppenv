#!/usr/bin/python

import sys
from clang.cindex import *

class_kinds = [
    'CLASS_DECL',
    'STRUCT_DECL',
    'UNION_DECL',
    'CLASS_TEMPLATE',
    'CLASS_TEMPLATE_PARTIAL_SPECIALIZATION',
    ]

template_class_kinds = [
    'CLASS_TEMPLATE',
    'CLASS_TEMPLATE_PARTIAL_SPECIALIZATION',
    ]

method_kinds = [
    'CXX_METHOD',
    'FUNCTION_TEMPLATE',
    ]

template_arg_kinds = [
    'TEMPLATE_TYPE_PARAMETER',
    'TEMPLATE_NON_TYPE_PARAMETER',
    ]

def find_class_definition_in_file(file_cursor, class_name):
    stack = [file_cursor]
    defs = []
    while len(stack):
        cursor = stack[0]
        stack.pop(0)
        #print cursor.spelling, cursor.kind.name#, cursor.kind.is_reference(), cursor.kind.is_declaration(), cursor.kind.is_invalid(), cursor.is_definition()
        #print dir(cursor)
        #break

        if cursor.is_definition() and cursor.spelling == class_name:
            kind_name = cursor.kind.name
            if kind_name in class_kinds:
                defs.append(cursor)
                continue

        for c in cursor.get_children():
            stack.append(c)

    return defs

def __gen_template_args_prefix(iterator, is_prefix = True):
    result = ''
    for elem in iterator:
        value = ''
        if elem.kind.name == 'TEMPLATE_TYPE_PARAMETER':
            if is_prefix:
                value += 'typename '
            value += elem.spelling

        elif elem.kind.name == 'TEMPLATE_NON_TYPE_PARAMETER':
            if is_prefix:
                value += elem.type.spelling + ' '
            value += elem.spelling

        if value:
            if result:
                result += ', '
            if not result:
                if is_prefix:
                    result += 'template '
                result += '<'
            result += value

    if result:
        result += ">"
        if is_prefix:
            result += '\n'
    return result

def gen_one_method_definition(f):
    class_prefix = ''
    class_name_postfix = ''
    prefix = ''
    args = ''

    parent = f.semantic_parent
    class_name = parent.spelling
    if parent.kind.name in template_class_kinds:
        class_prefix = __gen_template_args_prefix(parent.get_children())
        class_name_postfix = __gen_template_args_prefix(parent.get_children(), False)
        #print class_name_postfix

    #print f.spelling, f.result_type.spelling #, help(f)
    #print f.type.spelling
    #print help(f)

    prefix = __gen_template_args_prefix(f.get_children())

    for elem in f.get_children():
        if elem.kind.name != 'PARM_DECL':
            continue

        if args:
            args += ', '
        args += elem.type.spelling + ' ' + elem.spelling

    func = f.result_type.spelling + ' ' + class_name + "::" + f.spelling + '('
    result = class_prefix + prefix + func + args + ')\n{\n\n}\n'
    result = result.replace(class_name, class_name + class_name_postfix)
    return result

def get_functions_by_class(class_node):
    out_list = []
    for c in class_node.get_children():
        if c.kind.name not in method_kinds:
            continue

        if c.is_definition():
            continue

        out_list.append(c)
    return out_list

def show_ast(cursor, point_c = None):
    stack = [(cursor, 0)]
    while len(stack):
        c, d = stack[0]
        stack.pop(0)
        if point_c and point_c == c:
            space = '*'
        else:
            space = ' '

        print '%s%s %s' % (space * 2 * d, c.spelling, c.kind.name)
        children = []
        for child in c.get_children():
            children.append((child, d + 1))
        children.extend(stack)
        stack = children

## returns a tuple as (methods code, error info)
#
def gen_methods_definition(filename, class_name):
    index = Index.create()
    tu = index.parse(filename)
    class_defs = find_class_definition_in_file(tu.cursor, class_name)
    if not len(class_defs):
        return ('', 'not found class definitions in file: %s' % filename)


    code = ''
    for class_def_cursor in class_defs:
        funcs = get_functions_by_class(class_def_cursor)
        for f in funcs:
            code += gen_one_method_definition(f)
    return (code, '')
    
if __name__ == '__main__':
    code, err = gen_methods_definition("/home/yyz/test/pyclang/test.cpp", 'A')
    print code
    print 'err:', err

