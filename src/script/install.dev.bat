@echo off
if exist "dev.install.bat" (
    set SRC=.\..
) else (
    set SRC=.
)
if exist "%SRC%\.env" (
    echo virtual environment already exist.
) else (
    echo create virtual environment (.env^).
    py -3 -m venv %SRC%\.env
)
echo.
echo install requirements.
%SRC%\.env\Scripts\pip install -r %SRC%\script\requirements.txt
%SRC%\.env\Scripts\pip install flake8 ipython requests
