#!c:\programing\frc\2021\robot-2021\raptaconvenv\scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'pynetconsole==2.0.2','console_scripts','netconsole'
__requires__ = 'pynetconsole==2.0.2'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('pynetconsole==2.0.2', 'console_scripts', 'netconsole')()
    )
