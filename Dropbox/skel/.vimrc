"$Id: .vimrc  07-24-2007 02:10PM wimac ver: 11.229.2209
"Last modified: 08-17-2011  10:09PM crunchbang
autocmd BufReadPre *.pdf set ro
autocmd BufReadPost *.pdf %!pdftotext -nopgbrk "%" - 
autocmd VimEnter * echo "Welcome back!"
autocmd VimLeave * echo "See you later.."
autocmd BufReadPre *.doc set ro
autocmd BufReadPre *.doc set hlsearch!
autocmd BufReadPost *.doc %!antiword "%" 
autocmd FileType python set complete+=k~/.vim/syntax/python.vim isk+=.,(

source $VIMRUNTIME/mswin.vim
behave mswin
source ~/.vim/autocorrect.vim
set guiheadroom=0
set background=dark
colorscheme solarized 


"printer options
set popt=paper:letter
set pheader=""
:let mapleader = ","
set wildchar=<Tab> wildmenu wildmode=full
set wildcharm=<C-Z>


set pfn="Arial 10"
set ruler
set bg=dark
set wmh=0 
set rulerformat=%55(%{strftime('%a\ %b\ %e\ %I:%M\ %p')}\ %5l,%-6(%c%V%)\ %P%)
set ignorecase
set statusline=%<[%n]\ %F\ \ \ filetype=\%Y\ \ \ \ %r\ %1*%m%*%w%=%(column:\ %c%V%)%4(%)%-10(line:\ %l%)\ %4(%)%p%%\ %P
set nocompatible
set backspace=indent,eol,start
set nobackup		" do not keep a backup file, use versions instead
set history=50		" keep 50 lines of command line history
set showcmd		" display incomplete commands
set incsearch		" do incremental searching
set ai

set tabstop=8
set shiftwidth=4
set softtabstop=4
set expandtab
set autowrite
set autoindent
set hlsearch
set textwidth=79


"set foldmethod=indent
syntax enable

augroup vimrcEx

 au!
"global mode maps

"utl maps
map <C-P> :Utl o u vs<CR>
map <C-O> :close <CR>

map <M-Left> :tabprev<CR>
map <M-Right> :tabnext<CR>

map <C-J> <C-W>j<C-W>_
map <C-K> <C-W>k<C-W>_

"map ,e :help regexpref<cr>

map <S-F5> :%s//\r/g

map <F3> mzggg?G`z
map gbc yypkA =<ESC>jOscale=2<ESC>:.,+1!bc<CR>kJ


map .f v%zf
map S :let @x=@-<CR>diw"xP
map! <S-space> <esc>
map <C-Up> dd-P
map <C-Down> ddp 
map ,g <Esc>Bm`:r!ghref <cword><CR>"gdd``i<C-R><C-R>g<esc>dw

"normal mode maps
"
nnoremap <Tab> :bnext<CR>
nnoremap <S-Tab> :bprevious<CR>

""post file to blogger
nnoremap <Leader>blog :! wjmBlogger.py %:p<cr>

nnoremap  \  <C-^> 
nnoremap <F10> :b <C-Z>
nmap ,s :source ~/.gvimrc<CR>:source ~/.vimrc<CR><Esc>
nmap ,e :e ~/.gvimrc <CR>:tabnew ~/.vimrc<cr>

"insert mode maps 
imap <C-j> <ESC>lji
imap <C-k> <ESC>lki
imap <Backspace> <left><del>

"visual mode maps
vmap ,c :s/\<\(.\)\(\k*\)\>/\u\1\L\2/g<CR>
vmap sb "zdi<b><C-R>z</b><ESC>  : wrap <b></b> 
vmap st "zdi<?= <C-R>z ?><ESC>  : wrap <?=   ?> 
vmap ,g yvgvdm`:r!ghref '<C-R>=substitute(@0, "['\n]", " ", "g")<cr>'<cr>"gdd``i<C-R><C-R>g<Esc>

augroup syntax
au! BufNewFile,BufReadPost *.spec  so ~/vim/spec.vim
au  BufNewFile,BufReadPost *.spec  so ~/vim/spec.vim
augroup END
let loaded_matchit = 1
let X = getline(1)
let y = match(X, "#!/bin/bash" )
if (y != -1)
so ~/vim/bash.vim
endif
unlet X
unlet y

""taglist settings
let Tlist_Ctags_Cmd='/usr/bin/ctags'
let Tlist_WinWidth = 30
map <F4> :TlistToggle<cr>
set tags=tags;$HOME/vim/tags/

function! FindFileComplete(ArgLead, CmdLine, CursorPos)
    return globpath(&path, a:ArgLead)
endfunction


  hi Error term=reverse ctermbg=Red ctermfg=White guibg=Red guifg=White
  hi Todo term=standout ctermbg=Yellow ctermfg=Black guifg=Blue guibg=Yellow
  hi search guibg=LightBlue 
  hi link String Constant
  hi link Character Constant
  hi link Number Constant
  hi link Boolean Constant
  hi link Float Number
  hi link Conditional Statement
  hi link Label Statement
  hi link Keyword Statement
  hi link Exception Statement
  hi link Include PreProc
  hi link Define PreProc
  hi link Macro PreProc
  hi link PreCondit PreProc
  hi link StorageClass Type
  hi link Structure Type
  hi link Typedef Type
  hi link Tag Special
  hi link SpecialChar Special
  hi link Delimiter Special
  hi link SpecialComment Special
  hi link Debug Special


"HTML/XML tag wrapper
nmap ,t viw<Leader>t
vnoremap ,t <Esc>:call TagSelection()<CR>
nmap ,t viw<Leader>t
vnoremap ,t <Esc>:call TagSelection()<CR>

function! TagSelection()
  let l:tag = input("Tag name? ")
  " exec "normal `>a</" . l:tag . ">\e"
  " Strip off all but the first work in the tag for the end tag
  exec "normal `>a</" .
              \ substitute( l:tag, '[ \t"]*\(\<\w*\>\).*', '\1>\e', "" )
  exec "normal `<i"
              \ substitute( l:tag, '[ \t"]*\(\<.*\)', '<\1>\e', "" )
endfunction 
let g:xml_syntax_folding = 1
""autocmd BufWrite *   ks|call LastMod()|'s
""autocmd BufWrite *   ks|call NewVer()|'s

autocmd FileType python set omnifunc=pythoncomplete#Complete

nmap ,g <Esc>:so ~/.vim/gpl.txt<CR>

iab header #$Id: <C-R>=expand("%:t:r")<CR>  <C-R>=strftime("%m-%d-%Y %I:%M%p")<CR> <C-R>William J. MacLeod <CR>(wimac1@gmail.com) ver: <C-R>=strftime("%y.%j.%H%M")<CR>    $<ESC>

"My Header functions:

let s:V_Email='<wimac1@gmail.com>'

map ,h <Esc>:call Header()<CR> 


function! Header()
        if line("$") < 5
            exe ":s/^/#$Id:"expand("%:t:r") strftime("%m-%d-%Y  %I:%M%p") $USER s:V_Email "ver:" strftime("%y.%j.%H%M")    "$"
        endif
endfun

function! NewVer()
        if &modified
           if line("$") > 5
            let v = 5
        else
            let v = line("$")
        endif
        exe "1," . v . "g/ver: /s/ver: .*/ver: " .
         \ strftime("%y.%j.%H%M")
    endif
endfun

function! LastMod()
        if &modified
           if line("$") > 5
            let l = 5
        else
            let l = line("$")
        endif
        exe "1," . l . "g/Last modified: /s/Last modified: .*/Last modified: " .
            \ strftime("%m-%d-%Y  %I:%M%p") $USER
        endif
endfun

filetype plugin indent on
filetype plugin on
set ofu=syntaxcomplete#Complete

au BufWritePost * if getline(1)=~"^#!/bin/[a-z]*sh" | silent !chmod a+x <afile> 
au BufWritePost * if getline(1)=~"^#!/usr/bin/env*python" | silent !chmod a+x <afile> 
au BufWritePost * | endif

""hex editor
map <Leader>hon :%!xxd<CR>
map <Leader>hof :%!xxd -r<CR>

""minibufferexplorer stuff
let g:miniBufExplMapWindowNavVim = 1
let g:miniBufExplMapWindowNavArrows = 1
let g:miniBufExplMapCTabSwitchBufs = 1
let g:miniBufExplModSelTarget = 1

""python stuff
au BufReadPost * if line("'\"") > 0|if line("'\"") <= line("$")|exe("norm '\"")|else|exe "norm $"|endif|endif

if !exists("autocommands_loaded")
  let autocommands_loaded = 1
  autocmd BufRead,BufNewFile,FileReadPost *.py source ~/.vim/python
endif
