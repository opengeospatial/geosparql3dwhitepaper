import bibtexparser

with open("document/bibliography.bib", 'r') as file:
    bibcontent = file.read()
bibtexlib=bibtexparser.parse_string(bibcontent)
bibstring=""
for entry in bibtexlib.entries:
    founddoi=False
    thedoi=None
    for field in entry.fields:
        if field.key=="doi" or field.key=="DOI":
            thedoi=field.value
            founddoi=True
    if founddoi:
        bibstring+="* [[["+entry.key+", doi:"+thedoi+"]]]\n\n"
    else:
        bibstring+="* [[["+entry.key+", local-file("+entry.key+")]]]\n\n"
with open("document/sections/99-annex-bibliography.adoc","a") as bibdoc:
    bibdoc.write(bibstring)
