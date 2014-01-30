" Vim syntax file
" : Turing machine
" Maintainer: Maxim Yaskevich
" Latest Revision: 29 December 2013

if exists("b:current_syntax")
  finish
endif


" Keywords
syn keyword turingStat if else is then endif
syn keyword turingAction do move assume move
syn keyword turingDecl state
syn keyword turingBuiltin head right left nothing write erase
syn keyword turingTodo contained TODO FIXME XXX NOTE

" Matches
syn match turingComment "#.*$" contains=turingTodo
syn match turingNumber '\d\+' display
syn match turingNumber '[-+]\d\+' display
syn match turingNoAction 'no\s\+move' display
syn match turingStateModifier '\(initial\s\+\|final\s\+\)*\(initial\s\+\|final\s\+\)*state' display
syn match turingStateName 'state\s\*\(\.\*\)' display

" Regions
syn region turingRegion start="{" end="}" fold transparent
syn region turingString start='"' end='"'
syn region turingString start="'" end="'"


let b:current_syntax = "turing"

hi def link turingTodo                 Todo
hi def link turingComment              Comment
hi def link turingStat                 Operator
hi def link turingDecl                 Type
hi def link turingStateModifier        Type
hi def link turingStateName            Constant
hi def link turingString               String
hi def link turingAction               Special
hi def link turingNoAction             Special
hi def link turingNumber               Number
hi def link turingBuiltin              Function
