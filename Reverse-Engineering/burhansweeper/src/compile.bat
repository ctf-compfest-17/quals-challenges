powershell -ExecutionPolicy Bypass -File script.ps1

set ICON_PATH=.\icon\game.ico
set PUBLIC_ICON_PATH=..\public\game.ico
set EXE_PATH=..\public\game.exe
set OUTPUT_EXE=..\public\game2.exe

ResourceHacker.exe -open "%EXE_PATH%" -save "%OUTPUT_EXE%" -action addoverwrite -res "%ICON_PATH%" -mask ICONGROUP,MAINICON,

timeout /t 1 >nul

del "%EXE_PATH%"
move "%OUTPUT_EXE%" "%EXE_PATH%"
del "%PUBLIC_ICON_PATH%"
copy "%ICON_PATH%" "%PUBLIC_ICON_PATH%"

@REM powershell -Command "Stop-Process -Name explorer -Force; Start-Process explorer"
