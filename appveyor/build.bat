@echo off
:: Batch file for building crlibm on AppVeyor

bash -lc "make -C /c/projects/pycrlibm msys2"

gendef %PYTHON_DLL%
dlltool --dllname %PYTHON_DLL% --def python27.def --output-lib build\crlibm\lib\libpython27.a
