#import "../overrides.typ": cvSection, cvEntry, language, resume, format_cv_date, resume_has

#if resume_has("work") {

  cvSection(language.titles.work)

  for work in resume.work {
    cvEntry(
      title: [#work.position],
      society: [#work.at("name", default: "")],
      date: format_cv_date(work),
      location: [#work.at("location", default: "")],
      description: list(..work.highlights),
    )
  }
}
