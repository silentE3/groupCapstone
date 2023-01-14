"""
Build script for compilation via PyInstaller
"""
import PyInstaller.__main__

PyInstaller.__main__.run([
    'grouper.py',
    '--onefile',
])
