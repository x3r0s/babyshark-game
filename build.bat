@echo off
echo ========================================
echo Baby Shark - EXE Build Script
echo ========================================
echo.

echo Installing PyInstaller if needed...
pip install pyinstaller

echo.
echo Building EXE file...
pyinstaller babyshark.spec --clean

echo.
echo ========================================
echo Build complete!
echo EXE file location: dist\BabyShark.exe
echo ========================================
pause
