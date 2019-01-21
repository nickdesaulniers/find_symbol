# Find Symbol

I frequently have this problem when linking
`<archive>(<file>):<mangled symbol> undefined reference to <unmangled symbol>`.
This tool just finds which object, given a list, defines the given symbol so I
can link against it.

Example linker error:
```
/home/nick/llvm/build/lib/libclangFrontend.a(TextDiagnosticBuffer.cpp.o):(.data.rel.ro._ZTVN5clang20TextDiagnosticBufferE[_ZTVN5clang20TextDiagnosticBufferE]+0x40): undefined reference to `clang::DiagnosticConsumer::IncludeInDiagnosticCounts() const'
```

## Usage

Usage: `./find_symbol.py <symbol> [directories/files]`

Takes the symbol you're searching for (unmangled), and a list of directories
or files to search (searching the current working directory if these aren't
specified).

Example:
```sh
./find_symbol.py clang::DiagnosticConsumer::IncludeInDiagnosticCounts ~/llvm/build/lib
found clang::DiagnosticConsumer::IncludeInDiagnosticCounts in:
t /home/nick/llvm/build/lib/libclang.so.8svn
U /home/nick/llvm/build/lib/libclangFrontend.aT /home/nick/llvm/build/lib/libclangBasic.a
t /home/nick/llvm/build/lib/libclang.so.8
U /home/nick/llvm/build/lib/libclangTooling.a
U /home/nick/llvm/build/lib/libclangARCMigrate.at /home/nick/llvm/build/lib/libclang.so

$ cd ~/llvm/build/lib
$ ~/code/python/find_symbol/find_symbol.py clang::DiagnosticConsumer::IncludeInDiagnosticCounts
found clang::DiagnosticConsumer::IncludeInDiagnosticCounts in:
t /home/nick/llvm/build/lib/libclang.so.8svn
U /home/nick/llvm/build/lib/libclangFrontend.a
T /home/nick/llvm/build/lib/libclangBasic.a
t /home/nick/llvm/build/lib/libclang.so.8
U /home/nick/llvm/build/lib/libclangTooling.a
U /home/nick/llvm/build/lib/libclangARCMigrate.a
t /home/nick/llvm/build/lib/libclang.so

$ ~/code/python/find_symbol/find_symbol.py clang::DiagnosticConsumer::IncludeInDiagnosticCounts libclangBasic.a libclang.so
found clang::DiagnosticConsumer::IncludeInDiagnosticCounts in:
T libclangBasic.a
t libclang.so
```

## License

"THE BEER-WARE LICENSE" (Revision 42):
<nnn@google.com> wrote this file.  As long as you retain this notice you
can do whatever you want with this stuff. If we meet some day, and you think
this stuff is worth it, you can buy me a beer in return.   Nick Desaulniers
