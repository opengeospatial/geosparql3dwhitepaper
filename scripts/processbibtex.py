#!/usr/bin/env python3
"""
Generate Metanorma bibliography entries from a BibTeX file,
formatted in Springer LNCS (MathPhys) style, with numeric citation tags.
"""

import re
import bibtexparser
from bibtexparser.model import Entry

BIB_FILE = "document/bibliography.bib"
OUT_FILE = "document/sections/99-annex-bibliography.adoc"


def clean(text: str) -> str:
    """Remove common LaTeX commands and braces for plain-text output."""
    if not text:
        return ""
    text = re.sub(r"\\[a-zA-Z]+\s*", "", text)          # \command
    text = re.sub(r"[{}]", "", text)                     # braces
    text = re.sub(r"\s+", " ", text).strip()
    return text


def format_authors(author_field: str) -> str:
    """
    Convert BibTeX author list to LNCS style:
    "Last1, F., Last2, F.M., Last3, F."
    """
    if not author_field:
        return ""

    # Split on ' and '
    raw_authors = re.split(r"\s+and\s+", author_field, flags=re.IGNORECASE)
    formatted = []

    for a in raw_authors:
        a = clean(a)
        if not a:
            continue

        # Handle "Last, First" or "First Last"
        if "," in a:
            last, first = [x.strip() for x in a.split(",", 1)]
        else:
            parts = a.split()
            if len(parts) == 1:
                last, first = parts[0], ""
            else:
                last = parts[-1]
                first = " ".join(parts[:-1])

        # Initials only
        initials = "".join(
            p[0].upper() + "." for p in re.split(r"[\s\-]+", first) if p
        )
        if initials:
            formatted.append(f"{last}, {initials}")
        else:
            formatted.append(last)

    if not formatted:
        return ""

    # LNCS: up to all authors, separated by commas, last one also with comma
    return ", ".join(formatted)


def get_field(entry: Entry, *keys: str) -> str:
    """Return the first matching field (case-insensitive)."""
    fields = {f.key.lower(): f.value for f in entry.fields}
    for k in keys:
        if k.lower() in fields:
            return clean(fields[k.lower()])
    return ""


def format_entry(entry: Entry) -> str:
    """Return a single LNCS-formatted reference string (without the Metanorma wrapper)."""
    etype = entry.entry_type.lower()
    authors = format_authors(get_field(entry, "author", "editor"))
    title = get_field(entry, "title")
    year = get_field(entry, "year")
    doi = get_field(entry, "doi")
    url = get_field(entry, "url")

    parts = []

    if authors:
        parts.append(f"{authors}:")

    if title:
        # LNCS puts title in italics for most types
        parts.append(f"_{title}_.")

    # ----- type-specific core -----
    if etype in ("article",):
        journal = get_field(entry, "journal")
        volume = get_field(entry, "volume")
        number = get_field(entry, "number")
        pages = get_field(entry, "pages").replace("--", "–").replace("-", "–")

        core = []
        if journal:
            core.append(journal)
        if volume:
            vol = f"vol. {volume}"
            if number:
                vol += f"({number})"
            core.append(vol)
        if pages:
            core.append(f"pp. {pages}")
        if core:
            parts.append(" ".join(core) + ".")

    elif etype in ("inproceedings", "conference", "incollection", "inbook"):
        booktitle = get_field(entry, "booktitle")
        series = get_field(entry, "series")
        volume = get_field(entry, "volume")
        pages = get_field(entry, "pages").replace("--", "–").replace("-", "–")
        publisher = get_field(entry, "publisher")
        address = get_field(entry, "address")
        editor = format_authors(get_field(entry, "editor"))

        if booktitle:
            parts.append(f"In: {booktitle}")
            if editor:
                parts[-1] += f" ({editor} ed.)"
            parts[-1] += "."

        if series or volume:
            ser = series or "LNCS"
            if volume:
                ser += f", vol. {volume}"
            parts.append(ser + ".")

        if pages:
            parts.append(f"pp. {pages}.")

        pub = []
        if publisher:
            pub.append(publisher)
        if address:
            pub.append(address)
        if pub:
            parts.append(", ".join(pub) + ".")

    elif etype in ("book", "proceedings"):
        publisher = get_field(entry, "publisher")
        address = get_field(entry, "address")
        series = get_field(entry, "series")
        volume = get_field(entry, "volume")

        if series or volume:
            ser = series or ""
            if volume:
                ser = (ser + ", " if ser else "") + f"vol. {volume}"
            if ser:
                parts.append(ser + ".")

        pub = []
        if publisher:
            pub.append(publisher)
        if address:
            pub.append(address)
        if pub:
            parts.append(", ".join(pub) + ".")

    elif etype in ("techreport", "manual", "mastersthesis", "phdthesis"):
        inst = get_field(entry, "institution", "school", "organization")
        number = get_field(entry, "number")
        if inst:
            parts.append(inst + ".")
        if number:
            parts.append(f"Technical Report {number}.")

    elif etype in ("software", "misc", "online", "electronic"):
        howpublished = get_field(entry, "howpublished")
        note = get_field(entry, "note")
        if howpublished:
            parts.append(howpublished + ".")
        if note:
            parts.append(note + ".")

    # year is almost always present
    if year:
        parts.append(f"({year}).")

    # DOI / URL at the end (optional but useful)
    if doi:
        parts.append(f"https://doi.org/{doi}")
    elif url:
        parts.append(url)

    # Join and clean double spaces / stray dots
    result = " ".join(p for p in parts if p)
    result = re.sub(r"\s+\.", ".", result)
    result = re.sub(r"\.\.+", ".", result)
    result = re.sub(r"\s{2,}", " ", result).strip()
    return result


def main():
    with open(BIB_FILE, "r", encoding="utf-8") as f:
        bib = bibtexparser.parse_string(f.read())

    lines = []
    for entry in bib.entries:
        key = entry.key
        formatted = format_entry(entry)
        # Numeric tag → in-text citations become [1], [2], …
        lines.append(f"* [[[{key}, 1]]], {formatted}")

    with open(OUT_FILE, "a", encoding="utf-8") as f:
        f.write("\n\n".join(lines) + "\n")

    print(f"Wrote {len(lines)} LNCS-formatted entries to {OUT_FILE}")


if __name__ == "__main__":
    main()