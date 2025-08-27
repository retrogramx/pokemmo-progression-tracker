#!/usr/bin/env python3
"""Script to verify the PyInstaller build process and executable."""

import os
import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print("❌ Python 3.11+ is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True


def check_dependencies():
    """Check if required dependencies are installed."""
    required = ['PySide6', 'sqlmodel', 'alembic', 'pydantic']
    missing = []
    
    for dep in required:
        try:
            __import__(dep.lower())
            print(f"✅ {dep} is installed")
        except ImportError:
            print(f"❌ {dep} is missing")
            missing.append(dep)
    
    if missing:
        print(f"\nInstall missing dependencies with:")
        print(f"pip install {' '.join(missing)}")
        return False
    
    return True


def check_pyinstaller():
    """Check if PyInstaller is available."""
    try:
        import PyInstaller
        print(f"✅ PyInstaller {PyInstaller.__version__} is available")
        return True
    except ImportError:
        print("❌ PyInstaller is not installed")
        print("Install with: pip install pyinstaller")
        return False


def check_project_structure():
    """Check if the project structure is correct."""
    required_files = [
        'pokemmo_companion/app.py',
        'pokemmo_companion/core/models.py',
        'pokemmo_companion/ui/guides_view.py',
        'data/guide_kanto.json',
        'migrations/env.py'
    ]
    
    missing = []
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} is missing")
            missing.append(file_path)
    
    if missing:
        print(f"\nMissing {len(missing)} required files")
        return False
    
    return True


def run_build():
    """Run the PyInstaller build process."""
    print("\n🚀 Starting build process...")
    
    try:
        # Run PyInstaller
        cmd = [
            sys.executable, '-m', 'PyInstaller',
            '--onefile',
            '--windowed',
            '--name', 'PokeMMO Companion',
            '--add-data', 'data:data',
            '--add-data', 'migrations:migrations',
            'pokemmo_companion/app.py'
        ]
        
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Build completed successfully!")
            
            # Check if executable was created
            exe_path = Path('dist/PokeMMO Companion.exe')
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"✅ Executable created: {exe_path}")
                print(f"   Size: {size_mb:.1f} MB")
                return True
            else:
                print("❌ Executable not found in dist/ folder")
                return False
        else:
            print("❌ Build failed!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Build error: {e}")
        return False


def main():
    """Main verification process."""
    print("🔍 PokeMMO Companion Build Verification")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("PyInstaller", check_pyinstaller),
        ("Project Structure", check_project_structure),
    ]
    
    all_passed = True
    for check_name, check_func in checks:
        print(f"\n📋 {check_name}:")
        if not check_func():
            all_passed = False
    
    if not all_passed:
        print("\n❌ Some checks failed. Please fix the issues above.")
        return 1
    
    print("\n✅ All checks passed! Ready to build.")
    
    # Ask if user wants to run the build
    try:
        response = input("\n🚀 Run the build now? (y/N): ").strip().lower()
        if response in ['y', 'yes']:
            if run_build():
                print("\n🎉 Build verification complete!")
                print("You can now distribute the executable file.")
                return 0
            else:
                print("\n❌ Build failed. Check the output above.")
                return 1
        else:
            print("\n📝 Build verification complete. Run 'build.bat' or 'python verify_build.py' when ready.")
            return 0
    except KeyboardInterrupt:
        print("\n\n⏹️ Build verification cancelled.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
