# Installation Guide

This guide will help you install and set up the PokeMMO Companion App on your system.

## Prerequisites

- **Python 3.11 or higher** - Download from [python.org](https://www.python.org/downloads/)
- **Git** (optional, for development) - Download from [git-scm.com](https://git-scm.com/)

## Quick Start (Windows)

1. **Download and extract** the application files to a folder
2. **Open Command Prompt** in that folder
3. **Install dependencies**:
   ```cmd
   pip install -r requirements.txt
   ```
4. **Run the application**:
   ```cmd
   python -m pokemmo_companion.app
   ```

## Quick Start (macOS/Linux)

1. **Download and extract** the application files to a folder
2. **Open Terminal** in that folder
3. **Install dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```
4. **Run the application**:
   ```bash
   python3 -m pokemmo_companion.app
   ```

## Building a Standalone Executable

### Why Build an Executable?

Building an executable provides several benefits:
- **No Python installation required** - Users can run the app directly
- **Easy distribution** - Single file to share with others
- **Professional appearance** - Looks like a native Windows application
- **Portable** - Can be run from USB drives or network locations

### Windows Build (Recommended)

**Option 1: Automatic Build Script**
```cmd
build.bat
```
This script will:
- Check if Python is available
- Install PyInstaller if needed
- Build the executable automatically
- Place the result in `dist/PokeMMO Companion.exe`

**Option 2: PowerShell Script**
```powershell
.\build.ps1
```

**Option 3: Manual Build**
```cmd
# Install PyInstaller
pip install pyinstaller

# Build the executable
python -m PyInstaller --onefile --windowed --name "PokeMMO Companion" --add-data "data;data" --add-data "migrations;migrations" pokemmo_companion/app.py
```

### macOS/Linux Build

```bash
# Install PyInstaller
pip install pyinstaller

# Build the executable
pyinstaller --onefile --windowed --name "PokeMMO Companion" \
    --add-data "data:data" \
    --add-data "migrations:migrations" \
    pokemmo_companion/app.py
```

### Build Output

After building, you'll find:
- **Windows**: `dist/PokeMMO Companion.exe`
- **macOS/Linux**: `dist/PokeMMO Companion`

The executable is completely self-contained and includes:
- All Python dependencies
- Sample guide data
- Database migration files
- Everything needed to run the app

### Running the Executable

1. **Navigate to the `dist` folder**
2. **Double-click the executable file**
3. **The app will start immediately** - no installation needed

**Note**: The first run may take a few seconds as the app initializes the database.

## Development Setup

If you want to contribute to the project:

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd pokemmo-companion
   ```

2. **Install development dependencies**:
   ```bash
   pip install -e .[dev]
   ```

3. **Set up pre-commit hooks**:
   ```bash
   pre-commit install
   ```

4. **Initialize the database**:
   ```bash
   alembic upgrade head
   ```

5. **Import sample guides**:
   ```bash
   python scripts/import_guides.py
   ```

6. **Run the application**:
   ```bash
   python -m pokemmo_companion.app
   ```

## Troubleshooting

### Common Issues

**"Module not found" errors**
- Ensure you're using Python 3.11+
- Try reinstalling dependencies: `pip install --force-reinstall -r requirements.txt`

**Database errors**
- Delete the `pokemmo_tracker.db` file and restart
- Run `alembic upgrade head` to recreate the database

**GUI not showing**
- Ensure PySide6 is properly installed
- Check that you're running the app from the correct directory

**Permission errors (Linux/macOS)**
- Use `pip3` instead of `pip`
- Consider using a virtual environment

**Build failures**
- Ensure PyInstaller is installed: `pip install pyinstaller`
- Check that all dependencies are installed
- Try cleaning build artifacts: `make distclean`

### Virtual Environment (Recommended)

Create a virtual environment to avoid conflicts:

```bash
# Windows
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## First Run

1. **Launch the application** (either Python or executable)
2. **Select a region** from the dropdown (Kanto, Johto, etc.)
3. **Browse sections** in the left panel
4. **View steps** in the right panel
5. **Use the "Always on top" checkbox** to keep the guide visible while playing

## Updating

To update the application:

1. **Download the latest version**
2. **Replace the old files** (keep your database file)
3. **Run database migrations** if needed:
   ```bash
   alembic upgrade head
   ```
4. **Restart the application**

**For executable users**: Download the new executable and replace the old one.

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review the error messages in the console/terminal
3. Check the project's issue tracker
4. Ensure you're using a supported Python version

## System Requirements

- **OS**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **Python**: 3.11 or higher (for development)
- **Memory**: 512MB RAM minimum, 1GB recommended
- **Storage**: 100MB free space
- **Display**: 1024x768 minimum resolution

## Distribution

### Sharing the Executable

Once built, you can share the executable file:
- **Email**: Attach the .exe file directly
- **Cloud Storage**: Upload to Google Drive, Dropbox, etc.
- **USB Drive**: Copy the file to a portable drive
- **Network Share**: Place on a shared network location

### Security Notes

- The executable is safe to run - it's your own code
- Windows may show a security warning (this is normal for unsigned executables)
- Users can right-click and select "Run as administrator" if needed
- The app doesn't require internet access or elevated permissions
