"if exists("g:loaded_cppenv")
"    finish
"endif
"let g:loaded_cppenv = 1

function! cppenv#warn(msg)
  "if &verbose
    echohl WarningMsg
    echomsg a:msg
    echohl NONE
  "endif
endfunction

function! cppenv#test()
    echo "This is cppenv#test"
endfunction

" comment one line code
function! cppenv#comment()
    call setline('.', '//' . getline('.'))
endfunction

" uncomment one line code
function! cppenv#uncomment()
    let line_info = getline('.')
    "echo line_info
    if line_info =~ '^\s*//'
        let result = substitute(line_info, "///*", "", "")
        call setline('.', result)
    endif
endfunction

""""""""""""""""""""maps"""""""""""""""""""""
map <C-k><C-c> :call cppenv#comment()<CR>
imap <C-k><C-c> <Esc>:call cppenv#comment()<CR>

map <C-k><C-u> :call cppenv#uncomment()<CR>
imap <C-k><C-u> <Esc>:call cppenv#uncomment()<CR>

