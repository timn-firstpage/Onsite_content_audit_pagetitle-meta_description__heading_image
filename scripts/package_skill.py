"""Build a portable single skill archive; omit tests, customer data and repo metadata."""
import argparse
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED


def package(output):
    root = Path(__file__).resolve().parents[1]
    files = [root / p for p in ('SKILL.md', 'README.md', 'CHANGELOG.md', 'requirements.txt', 'config.template.json', 'assets/onsite-audit-cover.png',
                                'scripts/extract.py', 'scripts/report.py', 'scripts/onsite_checklist.py', 'scripts/shared_config.py',
                                'scripts/setup_runtime.py')]
    files += sorted((root / 'references').glob('*.md'))
    files += sorted((root / 'agents').glob('*.yaml'))
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        raise FileExistsError(f'Package exists: {output}')
    with ZipFile(output, 'x', ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, path.relative_to(root).as_posix())
    with ZipFile(output) as archive:
        if 'SKILL.md' not in archive.namelist() or archive.testzip():
            raise ValueError('Skill package verification failed')
    print(f'Verified {output} ({len(files)} files)')
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    package(parser.parse_args().output)
