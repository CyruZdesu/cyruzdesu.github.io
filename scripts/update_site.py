#!/usr/bin/env python3
"""
Auto-maintain Docsify navigation, directory indexes, changelog entries,
and homepage recent updates for cyruzdesu.github.io.

Uses only the Python standard library.
"""

from __future__ import annotations

import re
import subprocess
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent

CATEGORIES = [
    {
        "dir": "code",
        "sidebar_name": "Code",
        "heading": "# Code",
        "intro": "Directory of programming notes, algorithms, and source files.",
    },
    {
        "dir": "math",
        "sidebar_name": "Mathematics",
        "heading": "# Mathematics",
        "intro": "Directory of coursework notes, proofs, and mathematical derivations.",
    },
    {
        "dir": "thoughts",
        "sidebar_name": "Thoughts",
        "heading": "# Thoughts",
        "intro": "Directory of study workflows and informal reflections.",
    },
]

RECENT_UPDATES_LIMIT = 3
RECENT_START = "<!-- RECENT_UPDATES_START -->"
RECENT_END = "<!-- RECENT_UPDATES_END -->"
LIST_START = "<!-- AUTO_LIST_START -->"
LIST_END = "<!-- AUTO_LIST_END -->"


def extract_title(md_path: Path) -> str:
    """Extract the note title from the first non-empty line of the file."""
    text = md_path.read_text(encoding="utf-8")
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            # Strip leading Markdown heading hashes if present (e.g. '# Title' -> 'Title')
            title = re.sub(r"^#+\s*", "", stripped).strip()
            if title:
                return title
    return md_path.stem.replace("_", " ").replace("-", " ")


def get_file_date(md_path: Path) -> str:
    """Get last git commit date (YYYY-MM-DD), falling back to file mtime."""
    rel = md_path.relative_to(ROOT).as_posix()
    try:
        out = subprocess.check_output(
            ["git", "log", "-1", "--format=%cs", "--", rel],
            cwd=ROOT,
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        if out:
            return out
    except (subprocess.SubprocessError, FileNotFoundError):
        pass
    return datetime.fromtimestamp(md_path.stat().st_mtime).strftime("%Y-%m-%d")


def encode_web_path(category_dir: str, filename: str) -> str:
    """Build a root-relative Docsify URL path safely."""
    return f"/{category_dir}/{quote(filename)}"


def scan_notes() -> dict[str, list[dict[str, str]]]:
    """Scan all category folders for Markdown notes (excluding README.md)."""
    catalog: dict[str, list[dict[str, str]]] = {}
    for cat in CATEGORIES:
        cat_dir = ROOT / cat["dir"]
        notes: list[dict[str, str]] = []
        if cat_dir.is_dir():
            for md_file in sorted(cat_dir.glob("*.md")):
                if md_file.name.lower() == "readme.md":
                    continue
                notes.append(
                    {
                        "title": extract_title(md_file),
                        "date": get_file_date(md_file),
                        "url": encode_web_path(cat["dir"], md_file.name),
                        "rel_path": md_file.relative_to(ROOT).as_posix(),
                    }
                )
        # Newest first, then alphabetical by title
        notes.sort(key=lambda item: (item["date"], item["title"].lower()), reverse=True)
        catalog[cat["dir"]] = notes
    return catalog


def update_sidebar(catalog: dict[str, list[dict[str, str]]]) -> None:
    """Regenerate _sidebar.md from scanned categories and notes."""
    lines = [
        "* [Home](/)",
        "* [Changelog](/changelog.md)",
        "* [Guestbook](/guestbook.md)",
        "",
    ]
    for cat in CATEGORIES:
        lines.append(f"* [{cat['sidebar_name']}](/{cat['dir']}/)")
        for note in catalog[cat["dir"]]:
            lines.append(f"  * [{note['title']}]({note['url']})")
        lines.append("")

    content = "\n".join(lines).rstrip() + "\n"
    (ROOT / "_sidebar.md").write_text(content, encoding="utf-8")


def update_category_readmes(catalog: dict[str, list[dict[str, str]]]) -> None:
    """Update the note index table in each category's README.md."""
    for cat in CATEGORIES:
        readme_path = ROOT / cat["dir"] / "README.md"
        notes = catalog[cat["dir"]]

        if notes:
            table_lines = [
                "| Title | Updated |",
                "| :--- | :--- |",
            ]
            for note in notes:
                table_lines.append(f"| [{note['title']}]({note['url']}) | {note['date']} |")
            table_block = "\n".join(table_lines)
        else:
            table_block = "_No notes yet._"

        wrapped = f"{LIST_START}\n{table_block}\n{LIST_END}"

        if readme_path.exists():
            existing = readme_path.read_text(encoding="utf-8")
            pattern = re.compile(
                re.escape(LIST_START) + r"[\s\S]*?" + re.escape(LIST_END)
            )
            if pattern.search(existing):
                updated = pattern.sub(wrapped, existing, count=1)
                readme_path.write_text(updated, encoding="utf-8")
                continue

        # Fallback: create a clean category README with markers
        fresh = f"{cat['heading']}\n\n{cat['intro']}\n\n{wrapped}\n"
        readme_path.write_text(fresh, encoding="utf-8")


def sync_new_notes_to_changelog(catalog: dict[str, list[dict[str, str]]]) -> None:
    """Automatically append newly discovered notes to changelog.md if not yet listed."""
    changelog_path = ROOT / "changelog.md"
    if not changelog_path.exists():
        return

    content = changelog_path.read_text(encoding="utf-8")
    all_notes = [note for notes in catalog.values() for note in notes]

    # Check which note URLs are missing from changelog.md
    missing = [note for note in all_notes if note["url"] not in content]
    if not missing:
        return

    # Group missing notes by date (newest date first)
    by_date: dict[str, list[dict[str, str]]] = {}
    for note in missing:
        by_date.setdefault(note["date"], []).append(note)

    new_blocks = []
    for date_str in sorted(by_date.keys(), reverse=True):
        bullets = "\n".join(
            f"* **add**: [{n['title']}]({n['url']})" for n in by_date[date_str]
        )
        new_blocks.append(f"### {date_str}\n{bullets}")

    insertion = "\n\n".join(new_blocks) + "\n\n"

    # Insert right before the first existing '### ' entry
    match = re.search(r"^### ", content, flags=re.MULTILINE)
    if match:
        updated = content[: match.start()] + insertion + content[match.start() :]
    else:
        updated = content.rstrip() + "\n\n" + insertion

    changelog_path.write_text(updated, encoding="utf-8")


def update_homepage_recent_updates() -> None:
    """Sync the latest N entries from changelog.md into README.md."""
    changelog_path = ROOT / "changelog.md"
    readme_path = ROOT / "README.md"
    if not changelog_path.exists() or not readme_path.exists():
        return

    changelog_text = changelog_path.read_text(encoding="utf-8")
    # Split changelog by level-3 headings (### ...)
    matches = list(re.finditer(r"^### .+$", changelog_text, flags=re.MULTILINE))

    sections: list[str] = []
    for i, m in enumerate(matches[:RECENT_UPDATES_LIMIT]):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(changelog_text)
        section_text = changelog_text[start:end].strip()
        # Strip trailing horizontal rules if any
        section_text = re.sub(r"\n+---\s*$", "", section_text).strip()
        sections.append(section_text)

    recent_body = "\n\n".join(sections)
    recent_block = (
        f"{RECENT_START}\n"
        f"{recent_body}\n\n"
        f"[see more history](/changelog.md)\n"
        f"{RECENT_END}"
    )

    readme_text = readme_path.read_text(encoding="utf-8")
    pattern = re.compile(
        re.escape(RECENT_START) + r"[\s\S]*?" + re.escape(RECENT_END)
    )
    if pattern.search(readme_text):
        updated = pattern.sub(recent_block, readme_text, count=1)
    else:
        updated = readme_text.rstrip() + "\n\n" + recent_block + "\n"

    readme_path.write_text(updated, encoding="utf-8")


def main() -> None:
    catalog = scan_notes()
    sync_new_notes_to_changelog(catalog)
    update_sidebar(catalog)
    update_category_readmes(catalog)
    update_homepage_recent_updates()


if __name__ == "__main__":
    main()
