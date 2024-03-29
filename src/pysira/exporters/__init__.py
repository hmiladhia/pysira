import json

from pysira import THEMES_DIR
from pysira.exporters.exporter_base import ExporterBase
from pysira.exporters.html_exporter import HtmlExporter
from pysira.exporters.tex_exporter import LatexExporter


class ExportFactory:
    def __init__(self, theme_name: str) -> None:
        theme_path = THEMES_DIR / theme_name
        config_path = theme_path / "config.json"
        self.config = json.loads(config_path.read_text())
        self.config["theme_path"] = str(theme_path.resolve())

    def build(self) -> ExporterBase:
        markup = self.config["markup"].lower()

        if markup == "html":
            return HtmlExporter(self.config)

        if markup == "latex":
            return LatexExporter(self.config)

        raise ValueError("Unsupported Markup")
