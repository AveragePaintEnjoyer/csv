#!/usr/bin/env python3

import csv
from pathlib import Path
from html import escape
import json

DATA_DIR = Path("data")
TEMPLATE = Path("template/template.html")
OUTPUT_DIR = Path("public")
COLUMN_MAP = json.loads(
    Path("template/columns.json").read_text(encoding="utf-8")
)

def generate(csv_file):
    with csv_file.open(newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))

    if not rows:
        return

    headers = rows[0]

    # Find optional "<column>_link" columns.
    link_columns = {
        h[:-5]: i
        for i, h in enumerate(headers)
        if h.endswith("_link") and h[:-5] in headers
    }

    # Hide *_link columns from the table.
    display_headers = [
        h for h in headers
        if not h.endswith("_link")
    ]

    # Use friendly names from columns.json, falling back to CSV name.
    thead = "".join(
        f"<th>{escape(COLUMN_MAP.get(h, h))}</th>"
        for h in display_headers
    )

    # Map column names to indexes once.
    column_indexes = {
        h: i for i, h in enumerate(headers)
    }

    tbody = []

    for row in rows[1:]:
        cells = []

        for header in display_headers:
            value = row[column_indexes[header]]

            # If a matching *_link column exists, make the value a link.
            if header in link_columns:
                link = row[link_columns[header]]

                if link:
                    value = (
                        f'<a href="{escape(link, quote=True)}">'
                        f'{escape(value)}</a>'
                    )
                else:
                    value = escape(value)
            else:
                value = escape(value)

            cells.append(f"<td>{value}</td>")

        tbody.append(f"<tr>{''.join(cells)}</tr>")

    html = TEMPLATE.read_text(encoding="utf-8")
    html = html.replace("{{TITLE}}", escape(csv_file.stem))
    html = html.replace("{{HEADERS}}", thead)
    html = html.replace("{{ROWS}}", "\n".join(tbody))

    output_file = OUTPUT_DIR / f"{csv_file.stem}.html"
    output_file.write_text(html, encoding="utf-8")

    print(f"{csv_file} -> {output_file}")

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for csv_file in sorted(DATA_DIR.glob("*.csv")):
        generate(csv_file)

if __name__ == "__main__":
    main()