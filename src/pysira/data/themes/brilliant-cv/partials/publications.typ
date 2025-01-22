// Imports
#import "../overrides.typ": cvSection, cvPublication, language, resume, resume_has

#if resume_has("publications") {

cvSection(language.titles.publications)

// todo: requires jinja for bib
for pub in resume.publications {

}

cvPublication(
    bib: bibliography("../static/publications.bib"),
  keyList: (
    "smith2020",
    "jones2021",
    "wilson2022",
  ),
  refStyle: "apa",
)

}
