# setup.py  
from distutils.core import setup
import py2exe

setup(
    #zipfile=None,
    #options = {"py2exe": { "dll_excludes": ["python24.dll"]}, },
    console=["DumpBmp.py"],
    )

