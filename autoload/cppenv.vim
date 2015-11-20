"if exists("g:loaded_cppenv")
"    finish
"endif
"let g:loaded_cppenv = 1

let s:indent_space = repeat(' ', 4)

func! cppenv#dummy()
endfunc

func! cppenv#warn(msg)
    echohl WarningMsg
    echomsg a:msg
    echohl NONE
endfunc

" auto indent
func! cppenv#indent(lnum)
    let indent_n = cindent(a:lnum)
    let line_info = getline(a:lnum)
    if line_info =~ '^\s\{' . indent_n . '\}[^\s]*$'
        return ''
    endif

    let info = substitute(line_info, '^\s*', "", "")
    "echo info
    call setline(a:lnum, repeat(' ', indent_n) . info)
endfunc

" comment one line code
func! cppenv#comment()
    call setline('.', '//' . getline('.'))
endfunc

" uncomment one line code
func! cppenv#uncomment()
    let line_info = getline('.')
    "echo line_info
    if line_info =~ '^\s*//'
        let result = substitute(line_info, "///*", "", "")
        call setline('.', result)
    endif
endfunc

" auto () [] {}
func! cppenv#auto_brackets(bracket)
    let line_info = getline('.')
    let pos = getpos('.')
    let pat = '^.\{' . pos[2] . '\}\s\+.*$'
    let active = 0
    if empty(line_info)
        let active = 1
    elseif len(line_info) == pos[2]
        let active = 2
    elseif line_info =~ pat
        let active = 3
    endif
    "echo pat
    "echo active
    "echo virtcol('.') col(',') getpos('.')[2] wincol()
    let bracket = active > 0 ? a:bracket : strpart(a:bracket, 0, 1)
    let result = strpart(line_info, 0, pos[2]) . bracket . strpart(line_info, pos[2])

    if a:bracket[0] == '{' && active == 1
        let indent_n = cindent(line('.') - 1)
        let pos[2] = indent_n + 1
        let result = repeat(' ', indent_n) . result
    elseif active == 1
        let pos[2] = wincol()
        let result = repeat(' ', wincol() - 1) . result
    else
        let pos[2] = pos[2] + 1
    endif

    call setline('.', result)
    call setpos('.', pos)
endfunc

" end () [] {}
func! cppenv#end_brackets(bracket)
    let line_info = getline('.')
    let pos = getpos('.')
    let active = 0
    if empty(line_info)
        let active = 0
    elseif line_info[pos[2]] == a:bracket[1]
        let active = 1
    endif

    let bracket = active == 0 ? a:bracket[1] : ''
    let result = strpart(line_info, 0, pos[2]) . bracket . strpart(line_info, pos[2])
    call setline('.', result)
    let pos[2] = pos[2] + 1
    call setpos('.', pos)
endfunc

" enter in {}
func! cppenv#enter()
    let line_info = getline('.')
    let pos = getpos('.')
    if strpart(line_info, pos[2] - 1, 2) =~ '{}' && line_info =~ '{}\s*$'
        let before = strpart(line_info, 0, pos[2] - 1)
        call setline('.', before . '{')

        let s:end_bracket = '}'
        if line_info =~ '^\s*{}\s*$' && pos[1] > 1
            let prev_line_info = getline(pos[1] - 1)
            if prev_line_info =~ '^\s*\(class\|struct\|union\)\s\+[^{}]*$' || prev_line_info =~ '^.*=\s*$' || prev_line_info =~ '^\s*go\s\+\[.*\][^{}]*$'
                let s:end_bracket = '};'
            endif
        elseif line_info =~ '^\(\s*\|.*\s\+\)\(class\|struct\|union\)\s\+\(\w\|\d\|_\)\+\s*{}\s*$' || line_info =~ '^.*=\s*{}\s*$' || line_info =~ '^\s*go\s\+\[.*\][^{}]*{}$'
            let s:end_bracket = '};'
        endif
        call append(pos[1], repeat(' ', cindent('.')) . s:end_bracket)
        call setpos('.', pos)
    endif
endfunc

let g:py_dir = fnamemodify(expand('<sfile>'), ':p:h:gs?\\?/?')
let g:pyclang_dir = fnamemodify(expand('<sfile>'), ':p:h:h:gs?\\?/?') . '/pyclang'

" switch in .h/.hpp/.inl/.cpp/.c/.cc files
" @up_deep: 向上搜索的深度(等于-1时, 用locate命令全局搜索)
" @down_deep：向下搜索的深度
" @vsplit: 是否拆分出新的窗口
func! cppenv#switch_dd(up_deep, down_deep, vsplit)
    let s:abs_filename = expand('%:p')
    let s:directory = expand('%:p:h')
    let s:extension = expand('%:e')
    let s:filename = expand('%:r')
    let s:extension_list = ['h', 'hpp', 'ipp', 'inl', 'c', 'cc', 'cpp']

    let s:extension_expr = '^\('
    for ext in s:extension_list
        let s:extension_expr = s:extension_expr . ext . '\|'
    endfor
    let s:extension_expr = s:extension_expr[:-3] . '\)$'
    "echo(s:extension_expr)

    if a:up_deep >= 0 && s:extension =~ s:extension_expr
        exec(':pyf ' . g:py_dir . '/switch_dd.py')
        return 
    elseif a:up_deep == -1
        let s:grep_pattern = ''
        for ext in s:extension_list
            let s:grep_pattern = s:grep_pattern . '\(\/' . s:filename . '\\.' . ext . '\)' . '\|'
        endfor
        let s:grep_pattern = s:grep_pattern[:-3]

        let s:command = 'locate ' . s:filename . ' | grep -E ' . s:grep_pattern
        let s:locate_result = system(s:command)
        let s:abs_path_list = split(s:locate_result)

        if len(s:abs_path_list) > 1
            exec(':cexpr ""')
            for abs_path in s:abs_path_list
                let s:ccmd = ':caddexpr "' . abs_path . ':1:-"'
                if s:abs_filename == abs_path
                    let s:ccmd = s:ccmd[:-2] . ' <<<<"'
                endif
                exec(s:ccmd)
            endfor
            exec(':cw')
        endif
    endif

    echo('Not find switch files.')
endfunc

""""""""""""""""""""maps"""""""""""""""""""""
let s:is_infect = 0

func! cppenv#infect()
    let s:is_infect = 1

    map <C-k> :call cppenv#comment()<CR>
    imap <C-k> <Esc>:call cppenv#comment()<CR>

    map <C-u> :call cppenv#uncomment()<CR>
    imap <C-u> <Esc>:call cppenv#uncomment()<CR>

    imap ( <Esc>:call cppenv#auto_brackets('()')<CR>a
    imap [ <Esc>:call cppenv#auto_brackets('[]')<CR>a
    imap { <Esc>:call cppenv#auto_brackets('{}')<CR>a

    imap ) <Esc>:call cppenv#end_brackets('()')<CR>a
    imap ] <Esc>:call cppenv#end_brackets('[]')<CR>a
    imap } <Esc>:call cppenv#end_brackets('{}')<CR>a

    imap <C-l> <ESC>:call cppenv#enter()<CR>a<CR>

    if has("unix")
        "imap < <Esc>:call cppenv#auto_brackets('<>')<CR>a
        "imap > <Esc>:call cppenv#end_brackets('<>')<CR>a
        inoremap <CR> <ESC>:call cppenv#enter()<CR>a<CR>
    endif

    map gs :call cppenv#switch_dd(0, 0, 0)<CR>
    map gns :call cppenv#switch_dd(1, 0, 0)<CR>
    map gvs :call cppenv#switch_dd(0, 0, 1)<CR><C-W>L<C-W>h
    map gvns :call cppenv#switch_dd(1, 0, 1)<CR><C-W>L<C-W>h
    map gS :call cppenv#switch_dd(-1, 0, 0)<CR>
endfunc

func! cppenv#uninfect()
    let s:is_infect = 0

    unmap <C-k>
    iunmap <C-k>

    unmap <C-u>
    iunmap <C-u>

    iunmap (
    iunmap [
    iunmap {

    iunmap )
    iunmap ]
    iunmap }

    iunmap <C-l>

    if has("unix")
        "iunmap <
        "iunmap >
        iunmap <CR>
    endif

    call cppenv#warn("Close cppenv.")
    unmap gs
    unmap gns
    unmap gvs
    unmap gvns
    unmap gS
endfunc

func! cppenv#toggle()
    if s:is_infect == 0
        call cppenv#infect()
    else
        call cppenv#uninfect()
    endif
endfunc

map <C-F2> :call cppenv#toggle()<CR>
