
## Welcome to Robot 2020

Please take a look at the [wiki](https://github.com/Raptacon/Robot-2020/wiki) for the most up to date documenation

Also make sure to check out the [Kanban board](https://github.com/Raptacon/Robot-2020/projects/1)
test

# Installation
There is a general setup that is needed for each OS before you can build the code. Please look at the ![FRC Zero to Robot](https://docs.wpilib.org/en/stable/docs/zero-to-robot/step-2/frc-game-tools.html) to get the initial setup for NI and then ![WPILib](https://docs.wpilib.org/en/stable/docs/zero-to-robot/step-2/wpilib-setup.html) which has an amazing need to mount an ISO this year so make sure to pay attention to the "Mount" instructions. Once you have those completed in theory you can clone our code and type make. Make sure to see the OS specific instructions below.

## OSX Users
If you're using OSX you probably want to install python from python.org. Brew python has problems with Tk (simulator) where the widgets won't render correctly.

## Windows Users
![Raptacon (Team 3200) CI Pipeline](https://github.com/Raptacon/Robot-2020/workflows/Raptacon%20(Team%203200)%20CI%20Pipeline/badge.svg)

### Initial Installation
The easiest way to get things working is to install the package manager ![Chocolatey](https://chocolatey.org/) by going ![here](https://chocolatey.org/install) and going to Step 2 and following the directions OR just opening a PowerShell windows as Admin (yes...be careful) and doing:
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
```
once you have that completed you may install the Make system for windows by doing
```powershell
choco install make
```
after make has been installed, you can simply just go to the root of the Robot-2021 source and type in ```make``` and it should create a venv and install the required packages for building the robot code.
# Use
#Windows setup from cmd
python -m venv raptaconVenv
raptaconVenv\Scripts\activate.bat
pip install -r requirements.txt


