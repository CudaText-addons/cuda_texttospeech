import sys
from os.path import join, dirname
from os import environ
import platform

if platform.architecture()[0] == '64bit':
    arch = 'win64'
else:
    arch = 'win32'

PACKAGE_PATH = join(dirname(__file__), arch)

LIB_PATHS = [
    (PACKAGE_PATH, "win32com"),
    (join(PACKAGE_PATH, "win32"), "win32"),
    (join(PACKAGE_PATH, "win32", "lib"), "win32/lib"),
    (join(PACKAGE_PATH, "win32comext"), "win32comext")
]

for lib in LIB_PATHS:
    if lib[0] not in sys.path:
        sys.path.append(lib[0])
        print("python-pywin32: Added '%s'" % lib[1])

pywin32_path = join(PACKAGE_PATH, "pywin32_system32")
if pywin32_path not in environ["PATH"]:
    environ["PATH"] = environ["PATH"] + ";" + pywin32_path
