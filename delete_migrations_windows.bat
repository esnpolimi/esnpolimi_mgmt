@echo off

REM Move files
move esnpolimi_mgmt\migrations\0004_createsuperuser.py .
move esnpolimi_mgmt\migrations\0003_createaccounts.py .

REM Delete migrations .py files, excluding __init__.py and anything under contrib/sites
for /r %%i in (*\migrations\*.py) do (if not "%%~nxi"=="__init__.py" (if not "%%i"=="*contrib\sites*" (del "%%i")))

REM Delete all files in __pycache__ under migrations
for /r %%i in (*\migrations\__pycache__\*) do (del "%%i")

REM Delete all .pyc files under migrations
for /r %%i in (*\migrations\*.pyc) do (del "%%i")

REM Delete all files in __pycache__ directories
for /r %%i in (*\__pycache__\*) do (del "%%i")

REM Run manage.py
python manage.py makemigrations

REM Move files back
move esnpolimi_mgmt\migrations\0002_*.py esnpolimi_mgmt\migrations\0002_initial2.py
move 0004_createsuperuser.py esnpolimi_mgmt\migrations\
move 0003_createaccounts.py esnpolimi_mgmt\migrations\
