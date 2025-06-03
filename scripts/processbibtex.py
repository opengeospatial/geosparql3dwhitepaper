import bibtexparser

with open("document/bibliography.bib", 'r') as file:
    bibcontent = file.read()
parser = BibTexParser(common_strings=False)
parser.ignore_nonstandard_types = False
bibtexlib=parser.parse_string(bibcontent)
bibstring=""
for entry in bibtexlib.entries:
    print(entry.fields)
    if "doi" in entry.fields:
        bibstring+="* [[["+entry.key+", doi:"+entry.fields["doi"]+"]]]\n\n"
    elif "DOI" in entry.fields:
        bibstring+="* [[["+entry.key+", doi:"+entry.fields["DOI"]+"]]]\n\n"
    else:
        bibstring+="* [[["+entry.key+", local-file("+entry.key+")]]]\n\n"
with open("document/sections/99-annex-bibliography.adoc","a") as bibdoc:
    bibdoc.write(bibstring)
