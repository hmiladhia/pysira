#import "../overrides.typ": cvSection, cvEntry, language, resume, format_cv_date, resume_has, markdown

#if resume_has("education") {

  cvSection(language.titles.education)

  for ed in resume.education {
    let desc = ()
    if "score" in ed.keys() {desc.push(ed.score)}
    desc.push(ed.at("courses", default: ()))
    let title = ()
    if "studyType" in ed.keys() {title.push(ed.studyType)}
    if "area" in ed.keys() {title.push(ed.area)}
    let title=title.join(" - ")

    cvEntry(
      title: markdown(title),
      society: markdown(ed.institution),
      date: format_cv_date(ed),
      location: markdown(ed.at("location", default: "")),
      description: list(
        ..desc.flatten().map(markdown)
      ),
    )
  }
}
