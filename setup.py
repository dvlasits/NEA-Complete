from cx_Freeze import setup, Executable
import sys

base = None

if sys.platform == 'win32':
    base = "Win32GUI"


executables = [Executable("SoftwareAnalyser.py", base=base, icon = "GraphSquareSmall.ico")]

packages = ["idna"]
options = {
    'build_exe': {

        'packages':packages,
    },

}

setup(
    name = "Unit Tester",
    options = options,
    version = "1.0",
    description = 'Software to analyse python code',
    executables = executables
    )
