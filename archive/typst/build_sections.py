#!/usr/bin/env python3
"""
Per-Section Build Script
========================
Builds each section individually into its own folder under per_section/,
each containing the JSON source, generated Typst file, and compiled PDF.

Usage:
    python build_sections.py              # build all sections
    python build_sections.py 01_geography # build one section by name
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

# Reuse all generators from the main build script
from build import generate_section

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "data"
PER_SECTION_DIR = SCRIPT_DIR / "per_section"


def build_one_section(json_path: Path):
    """Build a single section: create folder, generate .typ, compile PDF."""
    stem = json_path.stem  # e.g. "01_geography"
    section_dir = PER_SECTION_DIR / stem
    section_dir.mkdir(parents=True, exist_ok=True)

    # 1. Copy JSON into the folder
    dest_json = section_dir / json_path.name
    shutil.copy2(json_path, dest_json)
    print(f"  {stem}/")
    print(f"    -> {json_path.name}")

    # 2. Generate standalone .typ
    with open(json_path) as f:
        data = json.load(f)

    typ_content = generate_section(data, standalone=True)
    # Fix import path: section is in per_section/<name>/, template is in typst/
    typ_content = typ_content.replace(
        '#import "../template.typ": *',
        '#import "../../template.typ": *',
    )

    typ_path = section_dir / (stem + ".typ")
    with open(typ_path, "w") as f:
        f.write(typ_content)
    print(f"    -> {stem}.typ")

    # 3. Compile PDF
    pdf_path = section_dir / (stem + ".pdf")
    result = subprocess.run(
        [
            "typst", "compile",
            "--root", str(SCRIPT_DIR),
            "--font-path", str(SCRIPT_DIR / "fonts"),
            str(typ_path),
            str(pdf_path),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"    !! PDF compilation failed:\n{result.stderr}")
    else:
        print(f"    -> {stem}.pdf")
        if result.stderr:
            print(f"    Warnings: {result.stderr.strip()}")


def main():
    PER_SECTION_DIR.mkdir(exist_ok=True)

    # Determine which sections to build
    if len(sys.argv) > 1:
        # Build specific section(s)
        for name in sys.argv[1:]:
            json_path = DATA_DIR / f"{name}.json"
            if not json_path.exists():
                # Try without extension
                matches = list(DATA_DIR.glob(f"*{name}*.json"))
                if matches:
                    json_path = matches[0]
                else:
                    print(f"  !! No JSON found for '{name}'")
                    continue
            build_one_section(json_path)
    else:
        # Build all sections
        json_files = sorted(DATA_DIR.glob("*.json"))
        if not json_files:
            print("No JSON files found in data/")
            sys.exit(1)
        print(f"Building {len(json_files)} sections...\n")
        for jf in json_files:
            build_one_section(jf)

    print("\nDone!")


if __name__ == "__main__":
    main()
