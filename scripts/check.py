#!/usr/bin/env python3
"""Validate a real Hugo site at domain-root and subdirectory URLs."""
import json
from html.parser import HTMLParser
import os
from pathlib import Path
import shutil
import subprocess
import struct
import tomllib
import tempfile
from urllib.parse import unquote, urlsplit


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links = []
        self.search_index = None
        self.active = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for key in ("href", "src"):
            if key in attrs:
                self.links.append((tag, attrs[key]))
        if attrs.get("id") == "search-input":
            self.search_index = attrs.get("data-index")
        if attrs.get("aria-current") == "page":
            self.active.append(attrs.get("href"))


def check_site(source, *, theme_repo=None, themes=("searchbase",)):
    source = Path(source).resolve()
    with tempfile.TemporaryDirectory(prefix="dockleaf-check-") as directory:
        scratch = Path(directory)
        if theme_repo:
            installed = scratch / "site"
            shutil.copytree(source, installed, ignore=shutil.ignore_patterns("public", "resources", ".hugo_build.lock"))
            theme = installed / "themes/dockleaf"
            theme.mkdir(parents=True)
            for name in ("layouts", "static", "assets", "i18n", "hugo.toml", "theme.toml"):
                origin = theme_repo / name
                if origin.is_dir():
                    shutil.copytree(origin, theme / name)
                else:
                    shutil.copy2(origin, theme / name)
            source = installed
            overrides = source / "assets/css/custom.css"
            overrides.parent.mkdir(parents=True)
            overrides.write_text(":root { --brand: #34d399; }\n")
        for look, prefix in [(look, prefix) for look in themes for prefix in ("/", "/project/")]:
            destination = scratch / look / ("root" if prefix == "/" else "subdirectory")
            command = ["hugo", "--source", str(source), "--destination", str(destination),
                       "--baseURL", "https://example.org" + prefix, "--panicOnWarning"]
            subprocess.run(command, check=True, env=os.environ | {"HUGO_PARAMS_THEME": look})
            home = Document((destination / "index.html").read_text())
            assert home.search_index == prefix + "index.json", home.search_index
            pages = json.loads((destination / "index.json").read_text())
            assert pages, "Search index is empty"
            assert len({page["href"] for page in pages}) == len(pages)
            for page in pages:
                assert page["href"].startswith(prefix), page
                assert isinstance(page["content"], str)
                target = destination / page["href"].removeprefix(prefix) / "index.html"
                assert target.is_file(), target
                doc = Document(target.read_text())
                assert page["href"] in doc.active, (target, doc.active)
            for html in destination.rglob("*.html"):
                doc = Document(html.read_text())
                for tag, link in doc.links:
                    url = urlsplit(link)
                    if url.scheme or url.netloc or not url.path:
                        continue
                    assert url.path.startswith(prefix), (html, link)
                    target = destination / unquote(url.path.removeprefix(prefix))
                    if url.path.endswith("/"):
                        target /= "index.html"
                    assert target.is_file(), (html, link, target)
            if theme_repo:
                assert "Searchbase" not in (destination / "index.html").read_text()
                assert (destination / "guide/advanced/deployment/index.html").is_file()
                assert prefix + "guide/advanced/deployment/" in [link for _, link in home.links]
                assert prefix + "css/custom.css" in [link for _, link in home.links]
                assert (destination / "404.html").is_file()
                stylesheet = prefix + f"dockleaf/themes/{look}/style.css"
                if look == "searchbase":
                    assert not (destination / "dockleaf").exists()
                else:
                    assert stylesheet in [link for _, link in home.links], (look, home.links)
                    assert (destination / f"dockleaf/themes/{look}/style.css").is_file()
            print(f"Validated {len(pages)} searchable pages at {prefix} with the {look} theme")
        if theme_repo:
            command = ["hugo", "--source", str(source), "--destination", str(scratch / "unknown")]
            build = subprocess.run(command, capture_output=True, text=True, env=os.environ | {"HUGO_PARAMS_THEME": "nope"})
            assert build.returncode and "Dockleaf has no theme" in build.stdout + build.stderr, build.stderr
            print("Validated that an unknown theme stops the build")
    theme = theme_repo if theme_repo else source / "themes/dockleaf"
    if shutil.which("node"):
        for script in (theme / "static/js").glob("*.js"):
            subprocess.run(["node", "--check", str(script)], check=True)
    else:
        print("Node.js not installed; skipped optional JavaScript syntax checks")


def check_publication_assets(root):
    metadata = tomllib.loads((root / "theme.toml").read_text())
    for key in ("name", "license", "licenselink", "description", "homepage", "demosite", "tags", "features", "author", "original"):
        assert metadata.get(key), f"Missing theme metadata: {key}"
    assert metadata["homepage"] == "https://github.com/coolapso/hugo-theme-dockleaf"
    for name, minimum in (("screenshot.png", (1500, 1000)), ("tn.png", (900, 600))):
        data = (root / "images" / name).read_bytes()
        assert data[:8] == b"\x89PNG\r\n\x1a\n", name
        width, height = struct.unpack(">II", data[16:24])
        assert width >= minimum[0] and height >= minimum[1], (name, width, height)
        assert width * 2 == height * 3, (name, "Expected 3:2 aspect ratio")
    print("Validated theme metadata and Hugo Themes preview images")


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    check_publication_assets(root)
    check_site(root / "exampleSite", theme_repo=root, themes=("searchbase", "notekpr"))
