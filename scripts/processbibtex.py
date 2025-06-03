import bibtexparser

with open("document/bibliography.bib", 'r') as file:
    bibcontent = file.read()
bibtexlib=bibtexparser.parse_string(bibcontent)
bibstring=""
for entry in bibtexlib.entries:
    if "doi" in entry.fields:
        bibstring+="* [[["+entry.key+", doi:"+entry.fields["doi"]+"]]]\n\n"
    else:
        bibstring+="* [[["+entry.key+", local-file("+entry.key+")]]]\n\n"
with open("document/sections/99-annex-bibliography.adoc","a") as bibdoc:
    bibdoc.write(bibstring)
