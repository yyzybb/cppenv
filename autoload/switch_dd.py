import vim, os

current_file = vim.eval("s:abs_filename")
path = vim.eval("s:directory")
is_vsplit = int(vim.eval("a:vsplit"))
up_deep = int(vim.eval("a:up_deep"))
down_deep = int(vim.eval("a:down_deep"))
down_deep += up_deep
for i in range(up_deep):
    path = os.path.dirname(path)

extension_list = vim.eval("s:extension_list")

#print "extension_list:%s" % extension_list
#print "current_file:%s" % current_file
#print "path:%s" % path
#print 'is_vsplit:%s' % is_vsplit
#print 'up_deep:%s' % up_deep
#print 'down_deep:%s' % down_deep

# show
def show(filelist):
    if len(filelist) == 1:
        dst_file = filelist[0]
        bufindex = int(vim.eval('bufnr("%s")' % dst_file))
        #print "bufindex ", bufindex
        if bufindex == -1:
            if is_vsplit:
                cmd = 'vnew'
            else:
                cmd = 'e'
        else:
            if is_vsplit:
                cmd = 'sbuf'
            else:
                cmd = 'buf'
        cmd = ":" + cmd + " " + dst_file
        #print 'cmd ', cmd
        vim.command(cmd)
        return

    vim.command(':cexpr ""')
    for f in filelist:
        cmd = ':caddexpr "%s:1:-"' % f
        if f == current_file:
            cmd = cmd[:-2] + ' <<<<"'
        vim.command(cmd)
    vim.command(':cw')

# Search in directory recursive.
result = []
def search_r(path, recursive_deep):
    if recursive_deep > down_deep:
        return 

    for p in os.listdir(path):
        f = os.path.join(path, p)
        #print f
        if os.path.isdir(f):
            search_r(f, recursive_deep + 1)

        if os.path.isfile(f):
            pure_name, ext = os.path.splitext(f)
            if ext[1:] in extension_list and \
                    os.path.basename(pure_name) == os.path.basename(os.path.splitext(current_file)[0]):
                result.append(f)

search_r(path, 0)
#print 'result:', result

if len(result) <= 1:
    print 'Not find switch files.'
elif len(result) == 2:
    result.remove(current_file)
    show(result)
else:
    show(result)

