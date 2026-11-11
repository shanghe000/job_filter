"""Package desktop build, documentation, synthetic samples and checksum."""
import hashlib
from pathlib import Path
import platform
import shutil
import tempfile

root = Path(__file__).resolve().parents[1]
system = platform.system().lower()
arch = platform.machine().lower().replace('amd64', 'x86_64')
name = f'JobFilter-{system}-{arch}'
release = root / 'release'
release.mkdir(exist_ok=True)
with tempfile.TemporaryDirectory() as tmp:
    stage = Path(tmp) / name
    stage.mkdir()
    binary = root / 'dist' / ('JobFilter.app' if system == 'darwin' else 'JobFilter')
    if not binary.is_dir():
        raise SystemExit(f'Expected desktop bundle not found: {binary.name}')
    shutil.copytree(binary, stage / binary.name)
    for file in ['README.md', 'README.en.md', 'LICENSE', 'CHANGELOG.md']:
        shutil.copy2(root / file, stage / file)
    shutil.copytree(root / 'examples', stage / 'examples')
    shutil.copytree(root / 'docs', stage / 'docs')
    archive = Path(shutil.make_archive(str(release / name), 'zip', tmp))
digest = hashlib.sha256(archive.read_bytes()).hexdigest()
archive.with_suffix('.zip.sha256').write_text(f'{digest}  {archive.name}\n')
print(f'Packaged {archive.name} with SHA-256 checksum.')
