@echo off
set currentpath=%~dp0
echo %currentpath%
cd /d %currentpath%
echo You may want to update your pip packages before using this script - there may be problems running robotpy-installer otherwise

:start
set ch="0"
echo. &echo What would you like to do? &
echo.1 - Download Python for Roborio&
echo.2 - Install python to Roborio&
echo.3 - Download robot pip packages&
echo.4 - Install robot pip packages&
echo.5 - Download robotpy&echo.6 - Install robotpy&
echo.6 - Download robotpy packages&
echo.7 - Install robotpy packages to robot &
echo.7 - Deploy robot code&
echo.Anything else - Quit
set /P ch="Choice: "

if "%ch%"=="1" (
    goto downloadpython
)
if "%ch%"=="2" (
    goto installpython
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
    goto downloadrp
)
if "%ch%"=="8" (
    goto installrp
)
if "%ch%"=="9" (
    goto deployrc
)

goto:eof

:downloadpython
robotpy-installer download-python
goto start

:installpython
robotpy-installer install-python
goto start


:downloadrp
robotpy-installer opkg download -r .\opkg_requirements.txt
goto start


:installrp
robotpy-installer opkg install --force-reinstall -r .\opkg_requirements.txt
goto start


:downloadrpip
rem TODO update to work with pip reqs
rem robotpy-installer download -r .\pip_requirements.txt
robotpy-installer download robotpy robotpy-ctre robotpy-navx robotpy-rev robotpy-wpilib-utilities pynetworktables
goto start


:installrpip
rem TODO update to work with reqs file
rem robotpy-installer install-python -r .\pip_requirements.txt
robotpy-installer install robotpy robotpy-ctre robotpy-navx robotpy-rev robotpy-wpilib-utilities pynetworktables

goto start


:deployrc
python ..\robot.py deploy
goto start
