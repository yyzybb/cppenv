# Cppenv: complete vim environment for coding C++
***

## Overview ##

My aim was making coding C++ fast, automation, and correctly. So, I choosed vim as our editor, because his shortcut keys often need sing``le press. But, I want to more...

This project has two parts:

- **Complete vim environment installer.**
- **Vim plugin for coding C++**
  
Vim environment includes some tools below:

 - g++
 - git
 - cmake
 - python2
    
and some plugins below:

- Vundle
- YouCompleteMe
- NerdTree
- Airline
- taglist
- vim-snippet
    
You can run the script `autoconf/install.sh` to install all of the vim environment I provide. It will automation install all of the tools and plugins above. If you are in Chinese, it maybe cost only 4 minutes.

## Install ##

If you want use the complete `cppenv`, please step by step below:

1. clone this git repository
2. run script `autoconf/install.sh` with the user that you coding with
3. wait about 4 minutes

The script will install `_vimrc`, `.ycm_extra_conf.py` and other plugins in `~/.vim`.

But, if you want use the plugin `cppenv` only, you can install `cppenv` to you vim runtime path.
And add code `execute cppenv#infect()` into your `.vimrc` when open c++ code files.
Look likes:

- `au BufNewFile,BufRead *.h,*.hpp,*.inl,*.ipp,*.cpp,*.c,*.cc,*.go execute cppenv#infect()`

## AutoComplete ##

`cppenv` provides some simple auto complete. And others, supported by `YouCompleteMe`.

![brackets](http://img.hoop8.com/attachments/1511/4511900695509.gif)

**Auto complete brackets:**
This feature supports `class`, `struct`, `union`, `function`, `lambda` and `C++ coroutine lambda`.
The `C++ coroutine lambda` refer to [https://github.com/yyzybb537/cpp_features](https://github.com/yyzybb537/cpp_features)
***

![definitions](http://img.hoop8.com/attachments/1511/9291900695509.gif)

**Auto complete class-methods definitions:**
This feature supports all of combination `class` and `method` types below:

- `normal class`
- `template class`

**and**

- `normal method`
- `template method`
- `static method`
- `static template method`


## Jump File ##

`cppenv` provides some shortcut keys for jump between c/c++ `header file` and c/c++ `source file`.

- `gs`
- `gns`
- `gS`
- `gvs`
- `gvns`

The `gs` can jump between `header` and `source` if there were in a same folder. If the two files have the same parent folder, you can use `gns` to jump between there. If the two files were not in a same folder and have not the same parent folder, the `gs` cannot work, here, you can use `gS`. `gS` will use `locate` command to find the files in all of your file-system, and show the results in `quickfix` window when the results more than one.

`gvs`, `gvns` are as same as `gs`, `gns` nearly. Difference was the shortcut key including `v` will split the window vertical, and show the other file buffer on right.

## Vim environment ##

If you install the complete vim environment, the `_vimrc` taken effect. It will give you a lot of shortcut key to boost your coding efficiency.

#### Plugins

`YouCompleteMe` provides syntax complete and check.

![YouCompleteMe GIF demo](http://img.hoop8.com/attachments/1511/1801900695509.gif)

`NerdTree` provides show the files tree.

![NerdTree](http://img.hoop8.com/attachments/1511/4341900695509.gif)

`TagList` provides show the functions in current file.

![taglist](http://img.hoop8.com/attachments/1511/6051900695509.gif)

#### ShortcutKey

I used `;` as the vim leader charactor, so seted below:

- **`;b`**  jump to begin of line. as `^`
- **`;e`**  jump to end of line. as `$`
- **`;w`**  save to file. as `:w`
- **`;q`**  quit the buffer. as `:quit` 
- **`;Q`**  quit the vim. as `:quitall`
- **`;hw`** jump to left window. as `<C-w>h`
- **`;jw`** jump to under window. as `<C-w>j`
- **`;kw`** jump to over window. as `<C-w>k`
- **`;lw`** jump to right window. as `<C-w>l`
- **`;/`**  cancel highlight. as `:nohls<CR>`
- **`;`** as `"`, e.g. you can use `;ay` to copy selection into `a` register, and use `;ap` to paste `a` register words into cursor position.

- **`F3`** toggle the `NerdTree` window, show the files tree.
- **`F4`** static syntax check current source file.

#### Jump

- **`gy`** jump to the word on the cursor definition or declaration. as call the YCM method `GoToDefinitionElseDeclaration`.
- **`gY`** show the word on the cursor definition or declaration on right window. 
- **`gl`** jump to last buffer. as `:b#<CR>`
- **`gL`** jump to last buffer and show current buffer on right window


#### TabPage

- **`<C-h>`** jump to previous tabpage. as `:tabprevious<CR>`
- **`<C-l>`** jump to next tabpage. as `:tabnext<CR>`

#### Build and Run

- **`F7`** build current file, output `out.exe`
- **`F5`** build and run. output `out.exe`
- **`F8`** build and run with libboost. output `out.exe`

#### Complete By Snippet

- **`<C-j>`** trigge the snippet.

Support snippet trigger list below:

- **`time`** the output for e.g:  `2015-11-20 23:56:18`
- **`date`** output for e.g: `2015-11-20`
- **`namespace <name>`**

	e.g.

	input:

		namespace ucorf

	output:

        namespace ucorf
    	{
    
    	} //namespace ucorf

- **`GNU License <name>`** Make gnu license copyright header in source file.

	e.g: 

	input

		`GNU License Ucorf`

	output

        // Copyright (C) 2011, 2012  Google Inc.   
	    // 
	    // This file is part of Ucorf  
	    // 
	    // Ucorf is free software: you can redistribute it and/or modify   
	    // it under the terms of the GNU General Public License as published by
	    // the Free Software Foundation, either version 3 of the License, or   
	    // (at your option) any later version. 
	    // 
	    // Ucorf is distributed in the hope that it will be useful,
	    // but WITHOUT ANY WARRANTY; without even the implied warranty of  
	    // MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the   
	    // GNU General Public License for more details.
	    // 
	    // You should have received a copy of the GNU General Public License   
	    // along with Ucorf.  If not, see <http://www.gnu.org/licenses/>.

- **`def <class name>`** First, you must save your class definition. Then, input `def <class name>`, will output all method definitions of the class.
  
	e.g:

	intput

		class A                                                                            
		{                                                                                  
		    void foo();                                                                    
		};                                                                                 
		                                                                                   
		def A

	output

		class A                                                                            
		{                                                                                  
		    void foo();                                                                    
		};                                                                                 
		                                                                                   
		void A::foo()                                                                   
		{                                                                               
		                                                                                
		}
