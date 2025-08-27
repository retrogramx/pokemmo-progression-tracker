# PokeMMO Companion App

A non-intrusive companion application for PokeMMO players to plan and track their progress. This app provides guides, checklists, and tracking tools without automating gameplay or violating PokeMMO's Terms of Service.

## Features

- **Guides Viewer**: Browse step-by-step guides for each region (Kanto, Johto, Hoenn, Sinnoh, Unova)
- **Progress Tracking**: Mark sections as completed or skipped
- **Always on Top**: Keep the guide visible while playing
- **Cross-Platform**: Windows-first design with cross-platform compatibility
- **Single Executable**: Can be built into a standalone .exe file for easy distribution

## Installation

### Prerequisites

- Python 3.11 or higher
- Windows 10/11 (primary target), macOS, or Linux

### Quick Start (Windows)

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

### Quick Start (macOS/Linux)

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

## Building the Executable

### Windows (Recommended)

**Option 1: Use the build script**
```cmd
build.bat
```

**Option 2: Use PowerShell**
```powershell
.\build.ps1
```

**Option 3: Manual build**
```cmd
pip install pyinstaller
python -m PyInstaller --onefile --windowed --name "PokeMMO Companion" --add-data "data;data" --add-data "migrations;migrations" pokemmo_companion/app.py
```

### macOS/Linux

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed --name "PokeMMO Companion" \
    --add-data "data:data" \
    --add-data "migrations:migrations" \
    pokemmo_companion/app.py
```

### Build Output

After building, you'll find:
- **Windows**: `dist/PokeMMO Companion.exe`
- **macOS/Linux**: `dist/PokeMMO Companion`

The executable is completely self-contained and can be distributed to users who don't have Python installed.

## Development

### Code Quality

The project uses strict code quality tools:

- **Black**: Code formatting
- **Ruff**: Linting and import sorting
- **MyPy**: Static type checking (strict mode)
- **Pre-commit**: Automated quality checks

### Available Commands

```bash
make help          # Show all available commands
make format        # Format code with Black
make lint          # Lint with Ruff
make typecheck     # Type check with MyPy
make test          # Run tests with pytest
make migrate       # Run database migrations
make import-guides # Import guides from JSON
make run           # Run the application
make build         # Build executable with PyInstaller
make build-exe     # Quick build using PyInstaller directly
make clean         # Clean generated files
make distclean     # Clean all build artifacts
```

### Project Structure

```
pokemmo_companion/
├── app.py                 # Main application entry point
├── core/                  # Core business logic
│   ├── db.py             # Database utilities
│   ├── models.py         # SQLModel data models
│   └── services/         # Business logic services
│       └── guide_loader.py
├── ui/                   # User interface components
│   ├── main_window.py    # Main application window
│   └── guides_view.py    # Guides viewer widget
├── data/                 # Sample guide data
│   ├── guide_kanto.json
│   └── guide_johto.json
├── scripts/              # Utility scripts
│   └── import_guides.py
├── migrations/           # Database migrations
├── assets/               # Application assets (icons, etc.)
└── tests/                # Test suite
```

## Database

The app uses SQLite with SQLModel (SQLAlchemy + Pydantic) for data persistence. Alembic handles database migrations.

### Models

- **Guide**: Represents a region guide (Kanto, Johto, etc.)
- **GuideStep**: Individual steps within guide sections

## Guide Data Format

Guides are stored in JSON format with the following structure:

```json
{
  "region": "Kanto",
  "sections": [
    {
      "section_id": 1,
      "title": "PALLET TOWN",
      "steps": [
        "Start your journey in Pallet Town",
        "Talk to Professor Oak to get your starter Pokemon"
      ]
    }
  ]
}
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes following the coding standards
4. Run quality checks: `make lint typecheck test`
5. Commit your changes: `git commit -m "Add amazing feature"`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

### Coding Standards

- Follow Black formatting (88 character line limit)
- Use type hints everywhere
- Write docstrings for all public functions
- Keep functions under 40 lines
- Write tests for new functionality
- No emojis in code or commits

## Testing

Run the test suite:

```bash
make test
```

Tests use pytest with coverage reporting. Aim for 90%+ coverage on non-UI code.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This application is not affiliated with PokeMMO or its developers. It is designed to be a companion tool that does not automate gameplay, inject code, or simulate inputs. Users are responsible for ensuring compliance with PokeMMO's Terms of Service.

## Roadmap

- [x] Team/Party tracker with suggested movesets
- [x] Economy notebook with ironman toggle
- [x] Per-badge checklists
- [x] CSV import/export functionality
- [x] User profiles and progress persistence
- [x] PyInstaller one-file Windows build
- [ ] Additional region guides (Hoenn, Sinnoh, Unova)
- [ ] Progress synchronization across devices
- [ ] Custom guide creation tools
