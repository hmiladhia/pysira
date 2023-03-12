from pathlib import Path

DATA_DIR = Path(__file__).parent / 'data'
TEMPLATES_DIR = DATA_DIR / 'templates'
THEMES_DIR = DATA_DIR / 'themes'
LANGUAGE_DIR = DATA_DIR / 'language'


__version__ = (Path(__file__).parent / 'VERSION').read_text().strip()

__all__ = ['DATA_DIR', 'TEMPALTE_DIR', 'THEMES_DIR', 'LANGUAGE_DIR', '__version__']
