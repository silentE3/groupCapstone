"""
Build script for compilation via PyInstaller

The following options are used:

`--onefile` - places the program into a single executable
`--specpath grouper.spec` - static spec file that ensures the same config every time it is compiled
"""
import PyInstaller.__main__

PyInstaller.__main__.run([
    'grouper.py',
    '--onefile',
    '--specpath',
    'grouper.spec'
])
