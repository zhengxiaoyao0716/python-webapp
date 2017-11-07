@echo off
if exist "ipython.bat" (
    set SRC=.\..
) else (
    set SRC=.
)

set args=

:READ_ARGS
set arg=%1
if defined arg (
    set args=%args% %arg%
    shift /0
    goto READ_ARGS
)

if not defined args (
    set args= -i -c "import os;os.sys.path.append(os.path.abspath(os.environ.get('SRC')));from script import *;from imp import reload;get, post = init_requests();"
)
%SRC%\.env\Scripts\ipython%args%
