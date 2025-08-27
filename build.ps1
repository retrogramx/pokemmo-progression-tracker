# PowerShell script to build PokeMMO Companion App executable

Write-Host "Building PokeMMO Companion App..." -ForegroundColor Green
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found Python: $pythonVersion" -ForegroundColor Yellow
} catch {
    Write-Host "Error: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.11+ and try again" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if PyInstaller is available
try {
    python -c "import PyInstaller" 2>$null
    Write-Host "PyInstaller is available" -ForegroundColor Yellow
} catch {
    Write-Host "Installing PyInstaller..." -ForegroundColor Yellow
    pip install pyinstaller
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Failed to install PyInstaller" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host "Building executable..." -ForegroundColor Yellow

# Build the executable
python -m PyInstaller --onefile --windowed --name "PokeMMO Companion" `
    --add-data "data;data" `
    --add-data "migrations;migrations" `
    --hidden-import sqlalchemy.sql.default_comparator `
    --hidden-import sqlalchemy.dialects.sqlite `
    --hidden-import alembic `
    --hidden-import pydantic `
    --hidden-import sqlmodel `
    --exclude-module matplotlib `
    --exclude-module numpy `
    --exclude-module pandas `
    --exclude-module scipy `
    --exclude-module tkinter `
    --exclude-module test `
    --exclude-module tests `
    --exclude-module pytest `
    --exclude-module mypy `
    --exclude-module ruff `
    --exclude-module black `
    --exclude-module pre_commit `
    pokemmo_companion/app.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Build failed" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Build completed successfully!" -ForegroundColor Green
Write-Host "Executable location: dist\PokeMMO Companion.exe" -ForegroundColor Yellow
Write-Host ""
Write-Host "You can now run the app by double-clicking the executable file." -ForegroundColor Cyan
Read-Host "Press Enter to exit"
