# BindingGenerator
Generate Python or Lua bindings.

Currently the generator produces Boost Python bindings. To run the generator:

1. Install CLANG 32 bit.
2. Create an environment variable called CLANG_PATH and set it to the LLVM/bin folder in which the libclang.dll file is present.
3. Install Python 2.7 32 bit.
4. Install Python Tools for Visual Studio(not necessary but useful). The solution file is for Visual Studio 2013.
5. Open the CPPBindingGenerator.sln solution.
6. In the Solution Explorer under Python environments, Python 2.7 should be highlighted. Right click the node & Install Python Package - install clang & Mako.
7. Run CPPBindingGenerator.py.
8. The project passes the 'TextComponent.h' as a the first command line argument which is the input file to scan. The Python bindings appear in textcomponent_bind.h in the same directory.
9. Enjoy!
10. Lua bindings support using luabind will be added soon. 

##Note:
1. Remove macros infront of class names first
2. Remove macros infront of function names too - this parser parses one file at a time, so unless the macro is defined in the same file, it has no way of knowing that its a macro and assumes it to be the function name or class name.
