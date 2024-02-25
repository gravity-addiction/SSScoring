" .vimrc - nothing special here.
syntax on
set ai
set nu
set ruler
set sts=4
set bs=2
set noic
set nowrap
set sw=4
set expandtab
set tabstop=4
set background=light
set history=500
set splitright
set hlsearch
set fo-=o
set fo-=c
set fo-=r
color blue
highlight Directory ctermfg=lightcyan

highlight LineNr ctermfg=lightgreen
highlight LineNr ctermbg=black

" Pathogen support:
" execute pathogen#infect()

autocmd VimEnter * if len($TERM)| NERDTree | set nu |endif
autocmd VimEnter * if len($TERM) && argc()|wincmd l|endif

