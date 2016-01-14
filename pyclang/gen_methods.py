#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys, traceback, re
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


## 广度优先遍历AST语法树
# @root 根节点
# @pred 条件谓词(返回false时不再继续遍历当前节点的子节点)
def bft_ast_iter(root, pred = None):
    stack = [root]
    while len(stack):
        c = stack[0]
        stack.pop(0)
        yield c
        if pred and not pred(c):
            continue

        for child in c.get_children():
            stack.append(child)

## 找到class定义的节点
def find_class_definition_in_file(root, class_name):
    for cursor in bft_ast_iter(root):
        #print cursor.spelling
        if cursor.is_definition() and cursor.spelling == class_name:
            kind_name = cursor.kind.name
            if kind_name in class_kinds:
                return cursor
    return 

## 生成模板参数
[
  template_enum_decl,
  template_enum_args,
  template_enum_types,
] = range(3)

def gen_template_decl_or_args(template_enum, iterator):
    elems = []
    for elem in iterator:
        value = ''
        tokens = ''.join([ch.spelling for ch in elem.get_tokens()])
        variadic = '...' in tokens and '...' or ''
        if elem.kind.name == 'TEMPLATE_TYPE_PARAMETER':
            if template_enum == template_enum_decl:
                value = 'typename %s %s' % (variadic, elem.spelling)
            elif template_enum == template_enum_args:
                value = '%s%s' % (elem.spelling, variadic)
            else:
                value = 'typename%s' % variadic

        elif elem.kind.name == 'TEMPLATE_NON_TYPE_PARAMETER':
            if template_enum == template_enum_decl:
                value = '%s %s %s' % (elem.type.spelling, variadic, elem.spelling)
            elif template_enum == template_enum_args:
                value = '%s%s' % (elem.spelling, variadic)
            else:
                value = '%s%s' % (elem.type.spelling, variadic)

        if value:
            elems.append(value)

    if not elems:
        return ''

    if template_enum == template_enum_decl:
        return 'template <' + ', '.join(elems) + '>\n'
    else:
        return '<' + ', '.join(elems) + '>'

## 生成一个member function的定义代码
def gen_one_method_definition(f):
    # 类模板参数定义    template <typename T>
    class_template_declarations = ''

    # 类模板参数   <T>
    class_template_args = ''

    # 类定义节点
    class_cursor = f.semantic_parent

    # 类名
    class_name = class_cursor.spelling
    if class_cursor.kind.name in template_class_kinds:
        class_template_declarations = gen_template_decl_or_args(template_enum_decl, class_cursor.get_children())
        class_template_args = gen_template_decl_or_args(template_enum_args, class_cursor.get_children())

    # 函数模板参数定义
    function_template_declarations = gen_template_decl_or_args(template_enum_decl, f.get_children())
    #print 'In gen method:', function_template_declarations

    # 函数参数列表
    args = ', '.join([ \
            elem.type.spelling + ' ' + elem.spelling \
            for elem in f.get_children() \
            if elem.kind.name == 'PARM_DECL' \
            ])

    # 函数修饰符(& && const volatile)
    qualified_str = ''
    qualifieds = re.findall(r'(?<=\))[^\)]*$', f.type.spelling)
    if qualifieds:
        # 修饰符无序 (&& & 要在最后)
        q_list = qualifieds[0].split(' ')
        q_list.sort()
        q_list.reverse()
        qualified_str = ' '.join(q_list)

    # 返回类型
    ori_result_type = f.result_type.spelling
    result_type = ori_result_type.replace('%s::' % class_name, '%s%s::' % (class_name, class_template_args))
    if result_type != ori_result_type:
        # 受限类型前面要加typename
        result_type = 'typename ' + result_type

    return class_template_declarations + function_template_declarations + \
            result_type + ' ' + class_name + class_template_args + "::" + f.spelling + \
            '(' + args + ')' + qualified_str + '\n{\n\n}\n'

## 全名
def complete_spelling(c):
    if not c.semantic_parent or c.semantic_parent.kind.name == 'TRANSLATION_UNIT':
        return c.spelling

    return complete_spelling(c.semantic_parent) + '::' + c.spelling

## 生成function的特征码
# @c function cursor
def create_function_traits(c):
    if c.kind.name not in method_kinds:
        raise ''

    class_name = ''
    complete_class_name = ''
    if c.semantic_parent.kind.name in class_kinds:
        class_name = c.semantic_parent.spelling
        complete_class_name = class_name + gen_template_decl_or_args(template_enum_args, c.semantic_parent.get_children())

    s = complete_spelling(c)# + template_args
    s += '(' + ', '.join([arg.type.spelling.replace(complete_class_name, class_name) for arg in c.get_children() if arg.kind.name == 'PARM_DECL']) + ')'

    # 函数修饰符(& && const volatile)
    qualifieds = re.findall(r'(?<=\))[^\)]*$', c.type.spelling)[0] 

    # 修饰符无序 (&& & 要在最后)
    q_list = qualifieds.split(' ')
    q_list.sort()
    q_list.reverse()
    s += ' '.join(q_list)
    return s

## 获取class定义节点中所有member function的子节点, 并排除已定义的
def get_functions_by_class(class_node, root):
    # 收集已定义的function
    defineds = {}
    for c in bft_ast_iter(root, lambda c: c.kind.name == "NAMESPACE" or c.kind.name == 'TRANSLATION_UNIT'):
        if c.kind.name not in method_kinds:
            continue

        if c.is_definition() and c.semantic_parent and c.semantic_parent.spelling == class_node.spelling:
            defineds[create_function_traits(c)] = c.spelling

    print 'defineds: ', defineds

    out_list = []
    for c in class_node.get_children():
        if c.kind.name not in method_kinds:
            continue

        ## 排除定义体直接写在类中的
        if c.is_definition():
            continue

        ## 排除在外部定义的
        print 'function:', create_function_traits(c)
        if defineds.has_key(create_function_traits(c)):
            continue

        out_list.append(c)
    return out_list

## 调试打印出AST语法树结构
def show_ast(cursor, point_c = None):
    stack = [(cursor, 0)]
    while len(stack):
        c, d = stack[0]
        stack.pop(0)
        if point_c and point_c == c:
            space = '*'
        else:
            space = ' '

        print '%s%s  %s  %s' % (space * 2 * d, c.spelling, c.kind.name, complete_spelling(c))
        children = []
        for child in c.get_children():
            children.append((child, d + 1))
        children.extend(stack)
        stack = children

## returns a tuple as (methods code, error info)
def gen_methods_definition(filename, class_name):
    index = Index.create()
    tu = index.parse(filename)
    root = tu.cursor
    #print dir(root); return '', ''
    #show_ast(root); return '', ''
    class_def_cursor = find_class_definition_in_file(root, class_name)
    if not class_def_cursor:
        return ('', 'not found class definitions in file: %s' % filename)

    #print 'found class_def_cursor'
    code = ''
    funcs = get_functions_by_class(class_def_cursor, root)
    for f in funcs:
        code += gen_one_method_definition(f)
    return (code, '')
    
if __name__ == '__main__':
    code, err = gen_methods_definition("./test.cpp", 'A')
    print 'code:'
    print code
    print 'err:', err

