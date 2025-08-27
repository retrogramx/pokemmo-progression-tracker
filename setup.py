"""Setup script for PokeMMO Companion App."""

from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(
        name="pokemmo-companion",
        version="0.1.0",
        description="A non-intrusive PokeMMO companion app for planning and tracking progress",
        long_description=open("README.md").read(),
        long_description_content_type="text/markdown",
        author="PokeMMO Companion Team",
        license="MIT",
        packages=find_packages(),
        python_requires=">=3.11",
        install_requires=[
            "PySide6>=6.5.0",
            "sqlmodel>=0.0.14",
            "SQLAlchemy>=2.0.0",
            "alembic>=1.13.0",
            "pydantic>=2.0.0",
        ],
        extras_require={
            "dev": [
                "pytest>=7.4.0",
                "pytest-cov>=4.1.0",
                "mypy>=1.5.0",
                "ruff>=0.1.0",
                "black>=23.0.0",
                "pre-commit>=3.3.0",
            ]
        },
        entry_points={
            "console_scripts": [
                "pokemmo-companion=pokemmo_companion.app:main",
            ],
        },
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: End Users/Desktop",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
            "Topic :: Games/Entertainment",
        ],
    )
