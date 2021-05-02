import sys
from cx_Freeze import setup, Executable
from functions import *

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "includes": ["selenium", "functions"]}

# # GUI applications require a different base on Windows (the default is for
# # a console application).
base = None
# if sys.platform == "win32":
#     base = "Win32GUI"

setup(
    name="Bot",
    version="0.1",
    description="Tweet brazilian tax evasion",
    options={"build_exe": build_exe_options},
    executables=[Executable("bot.py", base=base)]
)
