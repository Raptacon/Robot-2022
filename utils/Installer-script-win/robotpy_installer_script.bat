@echo off
set currentpath=%~dp0
echo %currentpath%
cd /d %currentpath%
echo You may want to update your pip packages before using this script - there may be problems running robotpy-installer otherwise

:start
set ch="0"
echo. &echo What would you like to do? & echo.1 - Download robotpy packages&echo.2 - Install robotpy packages to robot &echo.3 - Download robot pip packages&echo.4 - Install robot pip packages&echo.5 - Download robotpy&echo.6 - Install robotpy&echo.7 - Deploy robot code&echo.Anything else - Quit
set /P ch="Choice: "

if "%ch%"=="1" (
    goto downloadrp
)
if "%ch%"=="2" (
    goto installrp
)
if "%ch%"=="3" (
    goto downloadrpip
)
if "%ch%"=="4" (
    goto installrpip
)
if "%ch%"=="5" (
    goto downloadrpy
)
if "%ch%"=="6" (
    goto installrpy
)
if "%ch%"=="7" (
    goto deployrc
)

goto:eof


:downloadrp
robotpy-installer download-opkg -r .\opkg_requirements.txt
goto start


:installrp
robotpy-installer install-opkg --force-reinstall -r .\opkg_requirements.txt
goto start


:downloadrpip
robotpy-installer download-pip -r .\pip_requirements.txt
goto start


:installrpip
robotpy-installer install-pip -r .\pip_requirements.txt
goto start

:downloadrpy
robotpy-installer download-robotpy
goto start

:installrpy
robotpy-installer install-robotpy
goto start

:deployrc
python ..\robot.py deploy
goto start
