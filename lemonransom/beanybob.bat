@echo off
setlocal enabledelayedexpansion

set "ROOT_DIR=%~dp0"

for /R "%ROOT_DIR%" %%F in (*) do (
    echo Running script on: %%F

)

echo Done.
pause