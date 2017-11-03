@echo off
if exist "requirements.txt" ( cd .. )
if exist ".env" (
    echo virtual environment already exist.
) else (
    echo create virtual environment (.env^).
    py -3 -m venv .env
)
echo.
echo install requirements.
.env\Scripts\pip install -r script\requirements.txt
.env\Scripts\pip install flake8
