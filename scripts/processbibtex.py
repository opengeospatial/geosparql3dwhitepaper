import bibtexparser

with open("document/bibliography.bib", 'r') as file:
    bibcontent = file.read()
bibtexlib=bibtexparser.parse_string(bibcontent)
bibstring=""
for entry in bibtexlib.entries:
    print(entry.fields)
    print(entry)
    founddoi=False
    thedoi=None
    for field in entry.fields:
        if field.key=="doi" or field.key=="DOI":
            thedoi=field.value
            foundoi=True
    if founddoi:
        bibstring+="* [[["+entry.key+", doi:"+thedoi+"]]]\n\n"
    else:
        bibstring+="* [[["+entry.key+", local-file("+entry.key+")]]]\n\n"
    #if "doi" in entry.fields:
    #    bibstring+="* [[["+entry.key+", doi:"+entry.fields.doi+"]]]\n\n"
    #elif "DOI" in entry.fields:
    #    bibstring+="* [[["+entry.key+", doi:"+entry.fields["DOI"]+"]]]\n\n"
    #else:
    #    bibstring+="* [[["+entry.key+", local-file("+entry.key+")]]]\n\n"
with open("document/sections/99-annex-bibliography.adoc","a") as bibdoc:
    bibdoc.write(bibstring)
