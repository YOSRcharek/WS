@echo off

rem This file is UTF-8 encoded, so we need to update the current code page while executing it
for /f "tokens=2 delims=:." %%a in ('"%SystemRoot%\System32\chcp.com"') do (
    set _OLD_CODEPAGE=%%a
)
if defined _OLD_CODEPAGE (
    "%SystemRoot%\System32\chcp.com" 65001 > nul
)

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< Updated upstream
set "VIRTUAL_ENV=C:\Users\ASUS\Desktop\web semantique\WS\wsback\venv"
=======
set VIRTUAL_ENV=C:\Users\Lenovo\Desktop\Esprit\5\WebSem\WS\wsback\venv
>>>>>>> Stashed changes
=======
set VIRTUAL_ENV=C:\Users\DOUAA\Desktop\web semantique1\WS\wsback\venv
>>>>>>> doua
=======
set "VIRTUAL_ENV=C:\Users\ASUS\Desktop\Nouveau dossier (8)\web semantique1\WS\wsback\venv"
>>>>>>> doua

if not defined PROMPT set PROMPT=$P$G

if defined _OLD_VIRTUAL_PROMPT set PROMPT=%_OLD_VIRTUAL_PROMPT%
if defined _OLD_VIRTUAL_PYTHONHOME set PYTHONHOME=%_OLD_VIRTUAL_PYTHONHOME%

set _OLD_VIRTUAL_PROMPT=%PROMPT%
set PROMPT=(venv) %PROMPT%

if defined PYTHONHOME set _OLD_VIRTUAL_PYTHONHOME=%PYTHONHOME%
set PYTHONHOME=

if defined _OLD_VIRTUAL_PATH set PATH=%_OLD_VIRTUAL_PATH%
if not defined _OLD_VIRTUAL_PATH set _OLD_VIRTUAL_PATH=%PATH%

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< Updated upstream
set "PATH=%VIRTUAL_ENV%\Scripts;%PATH%"
set "VIRTUAL_ENV_PROMPT=(venv) "
=======
set PATH=%VIRTUAL_ENV%\Scripts;%PATH%
set VIRTUAL_ENV_PROMPT=(venv) 
>>>>>>> Stashed changes
=======
set PATH=%VIRTUAL_ENV%\Scripts;%PATH%
set VIRTUAL_ENV_PROMPT=(venv) 
>>>>>>> doua
=======
set "PATH=%VIRTUAL_ENV%\Scripts;%PATH%"
set "VIRTUAL_ENV_PROMPT=(venv) "
>>>>>>> doua

:END
if defined _OLD_CODEPAGE (
    "%SystemRoot%\System32\chcp.com" %_OLD_CODEPAGE% > nul
    set _OLD_CODEPAGE=
)
