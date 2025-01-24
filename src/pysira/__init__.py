from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
TEMPLATES_DIR = DATA_DIR / "templates"
THEMES_DIR = DATA_DIR / "themes"
EXTRA_DIR = DATA_DIR / "extra"
LANGUAGE_DIR = DATA_DIR / "language"
LANGUAGE_OVERRIDES_KEY = "language_overrides"


__version__ = "0.1.0"

__all__ = ["DATA_DIR", "TEMPALTE_DIR", "THEMES_DIR", "LANGUAGE_DIR", "__version__"]
