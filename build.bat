@echo off
echo Building PokeMMO Companion App...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.11+ and try again
    pause
    exit /b 1
)

REM Check if PyInstaller is available
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo Error: Failed to install PyInstaller
        pause
        exit /b 1
    )
)

echo Building executable...
python -m PyInstaller --onefile --windowed --name "PokeMMO Companion" ^
    --add-data "data;data" ^
    --add-data "migrations;migrations" ^
    --hidden-import sqlalchemy.sql.default_comparator ^
    --hidden-import sqlalchemy.dialects.sqlite ^
    --hidden-import alembic ^
    --hidden-import pydantic ^
    --hidden-import sqlmodel ^
    --exclude-module matplotlib ^
    --exclude-module numpy ^
    --exclude-module pandas ^
    --exclude-module scipy ^
    --exclude-module tkinter ^
    --exclude-module test ^
    --exclude-module tests ^
    --exclude-module pytest ^
    --exclude-module mypy ^
    --exclude-module ruff ^
    --exclude-module black ^
    --exclude-module pre_commit ^
    pokemmo_companion/app.py

if errorlevel 1 (
    echo Error: Build failed
    pause
    exit /b 1
)

echo.
echo Build completed successfully!
echo Executable location: dist\PokeMMO Companion.exe
echo.
echo You can now run the app by double-clicking the executable file.
pause
