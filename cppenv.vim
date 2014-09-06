"if exists("g:loaded_cppenv")
"    finish
"endif
"let g:loaded_cppenv = 1

let s:indent_space = repeat(' ', 4)

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
    if strpart(line_info, pos[2] - 1, 2) =~ '{}' && line_info =~ '^\s*{}\s*$'
        let spaces = strpart(line_info, 0, pos[2] - 1)
        call setline('.', spaces . '{')

        if pos[1] > 1 && getline(pos[1] - 1) =~ '^\s*\(class\|struct\|union\)\s\+.*$'
            call append(pos[1], spaces . '};')
        else
            call append(pos[1], spaces . '}')
        endif
        let pos[2] = len(spaces) + len(s:indent_space)
        call setpos('.', pos)
    endif
endfunc

""""""""""""""""""""maps"""""""""""""""""""""
let s:is_infect = 0

func! cppenv#infect()
    let s:is_infect = 1

    map <C-k><C-c> :call cppenv#comment()<CR>
    imap <C-k><C-c> <Esc>:call cppenv#comment()<CR>

    map <C-k><C-u> :call cppenv#uncomment()<CR>
    imap <C-k><C-u> <Esc>:call cppenv#uncomment()<CR>

    imap ( <Esc>:call cppenv#auto_brackets('()')<CR>a
    imap [ <Esc>:call cppenv#auto_brackets('[]')<CR>a
    imap { <Esc>:call cppenv#auto_brackets('{}')<CR>a
    "imap < <Esc>:call cppenv#auto_brackets('<>')<CR>a

    imap ) <Esc>:call cppenv#end_brackets('()')<CR>a
    imap ] <Esc>:call cppenv#end_brackets('[]')<CR>a
    imap } <Esc>:call cppenv#end_brackets('{}')<CR>a
    "imap > <Esc>:call cppenv#end_brackets('<>')<CR>a

    map <C-i> :call cppenv#indent('.')<CR>
    imap <C-p> <ESC>:call cppenv#enter()<CR>a<CR>
    imap <CR> <C-p>
endfunc

func! cppenv#uninfect()
    let s:is_infect = 0

    unmap <C-k><C-c>
    iunmap <C-k><C-c>

    unmap <C-k><C-u>
    iunmap <C-k><C-u>

    iunmap (
    iunmap [
    iunmap {
    "iunmap <

    iunmap )
    iunmap ]
    iunmap }
    "iunmap >

    unmap <C-i>
    iunmap <C-p>
    iunmap <CR>

    call cppenv#warn("Close cppenv.")
endfunc

func! cppenv#toggle()
    if s:is_infect == 0
        call cppenv#infect()
    else
        call cppenv#uninfect()
    endif
endfunc

map <C-F2> :call cppenv#toggle()<CR>
