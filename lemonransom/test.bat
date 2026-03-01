@echo off
set /a passcode=(%RANDOM% * 32768 + %RANDOM%) %% 1000000
set passcode=000000%passcode%
set passcode=%passcode:~-6%
echo this is a test program for you to crack, it uses a 6 digit code, alongside this i have provided a list of every combination possible in 6 digits for you to use on this. below, the generated 6 digit code will be shown.
echo %passcode%
pause
cls
:start
set /p x=Enter passcode: 
if %x% neq %passcode% (
cls
goto :start
) else (
echo congrats ig
pause
exit
)