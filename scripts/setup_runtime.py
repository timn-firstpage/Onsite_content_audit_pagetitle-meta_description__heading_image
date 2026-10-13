#!/usr/bin/env python3
"""Create/check a portable local Python environment; never change global Python."""
import argparse
from pathlib import Path
import subprocess
import sys
import venv

VERSION_CHECK = 'import sys; assert sys.version_info >= (3, 10), "Python 3.10+ is required"'
DEPENDENCY_CHECK = ('import openpyxl; from zoneinfo import ZoneInfo; '
                    'ZoneInfo("Asia/Hong_Kong"); '
                    'assert tuple(map(int, openpyxl.__version__.split(".")[:2])) >= (3, 1); '
                    'print("Runtime verified: openpyxl " + openpyxl.__version__ + ", timezone ready")')


def python_path(environment, platform=None):
    return Path(environment) / ('Scripts/python.exe' if (platform or sys.platform) == 'win32' else 'bin/python')


def setup(environment, check_only=False):
    if sys.version_info < (3, 10):
        raise ValueError('Run this setup with Python 3.10+; system Python is not installed or upgraded automatically')
    environment = Path(environment).expanduser().resolve()
    executable = python_path(environment)
    if environment.exists():
        if not (environment / 'pyvenv.cfg').is_file() or not executable.is_file():
            raise ValueError('Selected directory is not a usable venv; choose a new directory, existing files are preserved')
    elif check_only:
        raise ValueError('Runtime not found; run setup without --check-only first')
    else:
        venv.EnvBuilder(with_pip=True).create(environment)
    subprocess.run([str(executable), '-c', VERSION_CHECK], check=True)
    if not check_only:
        requirements = Path(__file__).resolve().parents[1] / 'requirements.txt'
        subprocess.run([str(executable), '-m', 'pip', 'install', '-r', str(requirements)], check=True)
    subprocess.run([str(executable), '-c', DEPENDENCY_CHECK], check=True)
    return executable


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--venv', type=Path, default=Path('.venv'), help='Local venv directory, relative to current directory')
    parser.add_argument('--check-only', action='store_true', help='Verify existing runtime without installing dependencies')
    args = parser.parse_args()
    try:
        executable = setup(args.venv, args.check_only)
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f'Runtime setup failed: {exc}', file=sys.stderr)
        return 1
    print(f'AUDIT_PYTHON={executable}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
