@echo off
setlocal
set EMPTY_FILE = ""
set "ps=Add-Type -AssemblyName System.windows.forms | Out-Null;"
set "ps=%ps% $f=New-Object System.Windows.Forms.OpenFileDialog;"
set "ps=%ps% $f.Filter='All files (*.*)|*.*';"
set "ps=%ps% $f.showHelp=$true;"
set "ps=%ps% $f.ShowDialog() | Out-Null;"
set "ps=%ps% $f.FileName"

for /f "delims=" %%I in ('powershell "%ps%"') do set "filename=%%I"

if defined filename (
    echo %filename%
) else (
    echo %EMPTY_FILE%
)

goto :EOF