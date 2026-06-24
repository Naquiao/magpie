#!/usr/bin/env python3
"""
ingest_arxiv.py — pull an arXiv paper into raw/ with clean metadata, zero pip deps.

Usage:
    python scripts/ingest_arxiv.py 2404.01234
    python scripts/ingest_arxiv.py https://arxiv.org/abs/2404.01234

What it does:
  1. Fetches title/authors/abstract from the arXiv API (Atom XML, stdlib only).
  2. Downloads the PDF to raw/papers/<id>.pdf.
  3. Writes raw/papers/<id>.md with metadata + abstract + a pointer to the PDF.
  4. Appends a stub line to wiki/_meta/sources.md.

The agent reads the .md for fast triage and opens the .pdf when it needs full detail.
Run this from the brain root (the folder containing BRAIN.md).
"""
import os, re, sys, urllib.request, xml.etree.ElementTree as ET
from datetime import date

ARXIV_API = "http://export.arxiv.org/api/query?id_list={}"
PDF_URL   = "https://arxiv.org/pdf/{}.pdf"
NS = {"a": "http://www.w3.org/2005/Atom"}

def arxiv_id(arg: str) -> str:
    m = re.search(r"(\d{4}\.\d{4,5})(v\d+)?", arg)
    if not m:
        sys.exit(f"Could not parse an arXiv id from: {arg!r}")
    return m.group(1)

def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "brain-template/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()

def get_meta(aid: str) -> dict:
    root = ET.fromstring(fetch(ARXIV_API.format(aid)))
    entry = root.find("a:entry", NS)
    if entry is None:
        sys.exit(f"No arXiv entry found for {aid}")
    def text(tag):
        el = entry.find(f"a:{tag}", NS)
        return (el.text or "").strip().replace("\n", " ") if el is not None else ""
    authors = [ (a.find("a:name", NS).text or "").strip()
                for a in entry.findall("a:author", NS) ]
    return {"title": text("title"), "abstract": text("summary"),
            "published": text("published")[:10], "authors": authors}

def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    root = os.getcwd()
    if not os.path.exists(os.path.join(root, "BRAIN.md")):
        sys.exit("Run this from the brain root (where BRAIN.md lives).")

    aid = arxiv_id(sys.argv[1])
    print(f"[arxiv] {aid} — fetching metadata...")
    meta = get_meta(aid)

    papers = os.path.join(root, "raw", "papers")
    os.makedirs(papers, exist_ok=True)

    pdf_path = os.path.join(papers, f"{aid}.pdf")
    print(f"[arxiv] downloading PDF -> {os.path.relpath(pdf_path, root)}")
    with open(pdf_path, "wb") as f:
        f.write(fetch(PDF_URL.format(aid)))

    md_path = os.path.join(papers, f"{aid}.md")
    authors = ", ".join(meta["authors"]) or "Unknown"
    with open(md_path, "w") as f:
        f.write(f"# {meta['title']}\n\n")
        f.write(f"- **arXiv:** [{aid}](https://arxiv.org/abs/{aid})\n")
        f.write(f"- **Authors:** {authors}\n")
        f.write(f"- **Published:** {meta['published']}\n")
        f.write(f"- **Ingested:** {date.today().isoformat()}\n")
        f.write(f"- **PDF:** `raw/papers/{aid}.pdf`\n\n")
        f.write("## Abstract\n\n")
        f.write(meta["abstract"] + "\n\n")
        f.write("> Full text in the PDF above. The compiler reads this stub for triage and\n")
        f.write("> opens the PDF for detail when writing wiki pages.\n")
    print(f"[arxiv] wrote {os.path.relpath(md_path, root)}")

    src = os.path.join(root, "wiki", "_meta", "sources.md")
    stub = f"- `raw/papers/{aid}.md` — {meta['title']} ({meta['published']}) — _uncompiled_\n"
    if os.path.exists(src):
        with open(src, "a") as f:
            f.write(stub)
        print(f"[arxiv] appended stub to wiki/_meta/sources.md")

    print(f"\nDone. Next: run your agent and say "
          f"'compile any new sources in raw/ into the wiki'.")

if __name__ == "__main__":
    main()
