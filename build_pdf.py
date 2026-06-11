#!/usr/bin/env python3
"""Convert ev_answers.md to a nicely styled PDF using markdown + Chrome headless."""
import markdown
import subprocess
import os
from pathlib import Path

SRC = Path("/workspace/ev_answers.md")
HTML = Path("/workspace/ev_answers.html")
PDF = Path("/workspace/EV_Exam_Answers.pdf")

md_text = SRC.read_text(encoding="utf-8")

html_body = markdown.markdown(
    md_text,
    extensions=[
        "extra",
        "tables",
        "fenced_code",
        "sane_lists",
        "toc",
        "nl2br",
    ],
)

css = """
@page {
    size: A4;
    margin: 18mm 14mm 18mm 14mm;
    @bottom-center {
        content: "Page " counter(page) " of " counter(pages);
    }
}

* { box-sizing: border-box; }

body {
    font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
    font-size: 11.5pt;
    line-height: 1.55;
    color: #1f2937;
    margin: 0;
    padding: 0;
}

h1 {
    font-size: 22pt;
    color: #ffffff;
    background: linear-gradient(90deg, #1e3a8a, #2563eb);
    padding: 14px 18px;
    border-radius: 6px;
    margin-top: 28px;
    margin-bottom: 16px;
    page-break-before: always;
    page-break-after: avoid;
}

h1:first-of-type { page-break-before: avoid; }

h2 {
    font-size: 15pt;
    color: #1e40af;
    border-bottom: 2px solid #1e40af;
    padding-bottom: 4px;
    margin-top: 22px;
    margin-bottom: 10px;
    page-break-after: avoid;
}

h3 {
    font-size: 13pt;
    color: #1e3a8a;
    margin-top: 14px;
    margin-bottom: 8px;
    page-break-after: avoid;
}

p {
    margin: 6px 0;
    text-align: justify;
}

strong { color: #111827; }

em { color: #374151; }

ul, ol {
    margin: 6px 0 6px 18px;
    padding-left: 18px;
}

li {
    margin: 3px 0;
}

li > ul, li > ol {
    margin: 3px 0 3px 14px;
}

hr {
    border: none;
    border-top: 1.5px dashed #93c5fd;
    margin: 18px 0;
}

table {
    border-collapse: collapse;
    width: 100%;
    margin: 10px 0;
    font-size: 10.5pt;
    page-break-inside: avoid;
}

th {
    background: #1e40af;
    color: white;
    padding: 6px 8px;
    text-align: left;
    border: 1px solid #1e3a8a;
}

td {
    padding: 5px 8px;
    border: 1px solid #cbd5e1;
    vertical-align: top;
}

tr:nth-child(even) td {
    background: #f1f5f9;
}

code {
    font-family: "Consolas", "Courier New", monospace;
    background: #f3f4f6;
    padding: 1px 5px;
    border-radius: 3px;
    font-size: 10.5pt;
    color: #b91c1c;
}

pre {
    background: #f3f4f6;
    padding: 8px 12px;
    border-left: 3px solid #2563eb;
    border-radius: 4px;
    font-size: 10pt;
    overflow-x: auto;
    page-break-inside: avoid;
}

pre code {
    background: transparent;
    color: #111827;
    padding: 0;
}

blockquote {
    border-left: 4px solid #2563eb;
    margin: 8px 0;
    padding: 6px 12px;
    background: #eff6ff;
    color: #1e3a8a;
}

.cover {
    text-align: center;
    margin-top: 80px;
    margin-bottom: 60px;
    page-break-after: always;
}

.cover h1 {
    background: none;
    color: #1e3a8a;
    border: none;
    font-size: 32pt;
    margin-bottom: 18px;
    page-break-before: avoid;
}

.cover h2 {
    color: #2563eb;
    border: none;
    font-size: 18pt;
    margin-top: 8px;
}

.cover .sub {
    font-size: 14pt;
    color: #4b5563;
    margin-top: 30px;
}

.cover .meta {
    margin-top: 80px;
    font-size: 12pt;
    color: #6b7280;
}

/* Avoid splitting answer blocks if possible */
h2 + p, h2 + ul, h2 + ol, h3 + p, h3 + ul, h3 + ol { page-break-before: avoid; }
"""

cover_html = """
<div class="cover">
    <h1>Electric Vehicle</h1>
    <h2>Complete 9-Mark Exam Answers</h2>
    <div class="sub">All 40 Predicted Questions across 4 Sections</div>
    <div class="sub" style="margin-top:12px;">Motors • Batteries • BMS • Drive-train • Vehicle Dynamics<br/>
    Vehicle Body • Suspension • Testing • Charging Systems • Standards</div>
    <div class="meta">
        Exam-Ready Reference<br/>
        Tier-1 Predicted Questions
    </div>
</div>
"""

html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>EV Exam Answers</title>
<style>{css}</style>
</head>
<body>
{cover_html}
{html_body}
</body>
</html>
"""

HTML.write_text(html_doc, encoding="utf-8")
print(f"[OK] HTML written: {HTML} ({HTML.stat().st_size//1024} KB)")

cmd = [
    "google-chrome",
    "--headless=new",
    "--disable-gpu",
    "--no-sandbox",
    "--no-pdf-header-footer",
    "--print-to-pdf-no-header",
    f"--print-to-pdf={PDF}",
    f"file://{HTML.absolute()}",
]
print("[..] Running Chrome to render PDF ...")
result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
if PDF.exists():
    print(f"[OK] PDF written: {PDF} ({PDF.stat().st_size//1024} KB)")
else:
    print("[ERR] PDF was not created")
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
