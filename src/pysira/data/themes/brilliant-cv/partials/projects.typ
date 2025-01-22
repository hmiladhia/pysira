#import "../overrides.typ": cvSection, cvEntry, language, resume, format_cv_date, resume_has

#if resume_has("projects") {

  cvSection(language.titles.projects)

  for project in resume.projects {
    let desc = ()
    desc.push(project.at("highlights", default: ()))

    let description = []
    if "description" in project.keys() {description = project.description + linebreak()}
    if "highlights" in project.keys() {description = description + list(..project.highlights)}

    cvEntry(
      title: link(project.at("url", default: "")),
      society: [#project.name],
      date: format_cv_date(project),
      location: [#project.at("location", default: "")],
      description: description,
      tags: project.keywords,
    )
  }
}
