#import "../overrides.typ": cvSection, cvEntry, language, resume, format_cv_date, resume_has, markdown

#if resume_has("work") {

  cvSection(language.titles.work)

  for work in resume.work {
    cvEntry(
      title: markdown(work.position),
      society: markdown(work.at("name", default: "")),
      date: format_cv_date(work),
      location: markdown(work.at("location", default: "")),
      description: list(..work.highlights.map(markdown)),
      tags: work.at("keywords", default: ()),
    )
  }
}
