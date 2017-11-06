@echo off
if exist "ipython.bat" (
    set SRC=.\..
) else (
    set SRC=.
)
%SRC%\.env\Scripts\ipython -i -c "import os;os.sys.path.append(os.path.abspath(os.environ.get('SRC')));from script import *;from imp import reload;get, post = init_requests();"
