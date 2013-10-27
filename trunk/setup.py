import sys

from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "Web-Server",
    version = "1.0",
    description = "Very simple web server program.",
    options = {"build_exe": {"includes": ['re', 'traceback']}},
    executables = [Executable("webserver.py", base = base)]
)
