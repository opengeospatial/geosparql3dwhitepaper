import bibtexparser
bibtexlib=bibtexparser.parse_file("../document/bibliography.bib")
bibstring=""
for entry in bibtexlib.entries:
    bibstring+="* [[["+entry.key+", local-file("+entry.key+")]]]\n\n"
with open("../document/sections/99-annex-bibliography.adoc","a") as bibdoc:
    bibdoc.write(bibstring)
