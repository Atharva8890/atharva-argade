#!/usr/bin/env python3
"""Convert ev_answers.md to a COMPACT PDF for micro-notes use.

Design goals (per user request):
- No wasted whitespace
- Tight margins, small but readable fonts
- Sections don't auto-page-break (only break when needed)
- Compact lists/tables/headings
- Suitable for printing & reducing to micro-notes
"""
import markdown
import subprocess
from pathlib import Path

SRC = Path("/workspace/ev_answers.md")
HTML = Path("/workspace/ev_answers.html")
PDF = Path("/workspace/EV_Exam_Answers.pdf")

md_text = SRC.read_text(encoding="utf-8")

html_body = markdown.markdown(
    md_text,
    extensions=["extra", "tables", "fenced_code", "sane_lists", "nl2br"],
)

css = """
@page {
    size: A4;
    margin: 8mm 9mm 9mm 9mm;
    @bottom-right {
        content: counter(page) " / " counter(pages);
        font-size: 7pt;
        color: #6b7280;
    }
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
    font-size: 9.2pt;
    line-height: 1.25;
    color: #111827;
    text-align: justify;
    column-gap: 0;
}

/* SECTION HEADING (h1) - keeps section starts visible but no forced new page */
h1 {
    font-size: 12pt;
    color: #ffffff;
    background: #1e3a8a;
    padding: 3px 8px;
    margin-top: 6px;
    margin-bottom: 4px;
    border-radius: 2px;
    page-break-after: avoid;
    page-break-before: auto;
}
h1:first-of-type { margin-top: 0; }

/* QUESTION HEADING (h2) */
h2 {
    font-size: 10.4pt;
    color: #1e3a8a;
    border-bottom: 1px solid #1e3a8a;
    padding: 1px 0;
    margin-top: 6px;
    margin-bottom: 2px;
    page-break-after: avoid;
}

h3 {
    font-size: 9.6pt;
    color: #1e40af;
    margin-top: 3px;
    margin-bottom: 1px;
    page-break-after: avoid;
}

p {
    margin: 1px 0;
    text-align: justify;
    orphans: 2;
    widows: 2;
}

strong { color: #000; font-weight: 700; }
em { color: #1f2937; }

ul, ol {
    margin: 1px 0 1px 14px;
    padding-left: 12px;
}
ul { list-style-type: disc; }
ol { list-style-type: decimal; }

li {
    margin: 0;
    padding: 0;
    line-height: 1.22;
}
li > ul, li > ol {
    margin: 0 0 0 8px;
    padding-left: 10px;
}

/* Compact horizontal rule between answers */
hr {
    border: none;
    border-top: 0.7px dashed #6b7280;
    margin: 4px 0;
}

/* Tables - very compact */
table {
    border-collapse: collapse;
    width: 100%;
    margin: 2px 0;
    font-size: 8.2pt;
    line-height: 1.15;
    page-break-inside: avoid;
}

th {
    background: #1e3a8a;
    color: white;
    padding: 2px 4px;
    text-align: left;
    border: 0.5px solid #1e3a8a;
    font-weight: 600;
}

td {
    padding: 1.5px 4px;
    border: 0.5px solid #9ca3af;
    vertical-align: top;
}

tr:nth-child(even) td { background: #f1f5f9; }

code {
    font-family: "Consolas", "Courier New", monospace;
    background: #f3f4f6;
    padding: 0 2px;
    border-radius: 2px;
    font-size: 8.6pt;
    color: #b91c1c;
}

pre {
    background: #f3f4f6;
    padding: 3px 6px;
    border-left: 2px solid #1e3a8a;
    border-radius: 2px;
    font-size: 8pt;
    line-height: 1.15;
    margin: 2px 0;
    overflow-x: auto;
    page-break-inside: avoid;
}

pre code { background: transparent; color: #111827; padding: 0; }

blockquote {
    border-left: 2px solid #1e3a8a;
    margin: 2px 0;
    padding: 1px 6px;
    background: #eff6ff;
    color: #1e3a8a;
    font-size: 8.8pt;
}

/* Avoid page breaks just after a heading */
h1 + p, h1 + ul, h1 + ol, h1 + table,
h2 + p, h2 + ul, h2 + ol, h2 + table,
h3 + p, h3 + ul, h3 + ol, h3 + table { page-break-before: avoid; }

/* Cover page */
.cover {
    text-align: center;
    padding: 60px 20px 40px;
    page-break-after: always;
}
.cover .title {
    font-size: 28pt;
    color: #1e3a8a;
    font-weight: 700;
    margin-bottom: 6px;
}
.cover .subtitle {
    font-size: 14pt;
    color: #2563eb;
    margin-bottom: 18px;
}
.cover .desc {
    font-size: 10.5pt;
    color: #374151;
    line-height: 1.5;
    margin-top: 18px;
}
.cover .badge {
    display: inline-block;
    background: #1e3a8a;
    color: white;
    padding: 4px 14px;
    border-radius: 14px;
    font-size: 10pt;
    margin-top: 25px;
}
.cover .footer {
    margin-top: 60px;
    font-size: 9pt;
    color: #6b7280;
}
"""

cover_html = """
<div class="cover">
    <div class="title">Electric Vehicle</div>
    <div class="subtitle">Complete 9-Mark Exam Answers</div>
    <div class="desc">
        All 40 Predicted Questions across 4 Sections<br/>
        Motors • Batteries • BMS • Drive-train • Vehicle Dynamics<br/>
        Vehicle Body • Suspension • Testing • Charging Systems • Standards
    </div>
    <div class="badge">Compact Edition - Micro Notes Ready</div>
    <div class="footer">Exam-Ready Reference - Tier-1 Predicted Questions</div>
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
    "--no-sandbox",
    "--disable-gpu",
    "--disable-dev-shm-usage",
    "--hide-scrollbars",
    "--virtual-time-budget=10000",
    "--run-all-compositor-stages-before-draw",
    "--no-pdf-header-footer",
    f"--print-to-pdf={PDF}",
    f"file://{HTML.absolute()}",
]
print("[..] Running Chrome to render PDF ...")
if PDF.exists():
    PDF.unlink()

import time
import signal
proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
last_size = -1
stable_count = 0
for i in range(90):
    time.sleep(1)
    if PDF.exists():
        size = PDF.stat().st_size
        if size == last_size and size > 0:
            stable_count += 1
            if stable_count >= 3:
                break
        else:
            stable_count = 0
            last_size = size
proc.send_signal(signal.SIGTERM)
try:
    proc.wait(timeout=5)
except subprocess.TimeoutExpired:
    proc.kill()

if PDF.exists():
    size_kb = PDF.stat().st_size / 1024
    print(f"[OK] PDF written: {PDF} ({size_kb:.0f} KB)")
else:
    print("[ERR] PDF was not created")
