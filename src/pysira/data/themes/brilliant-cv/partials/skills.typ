#import "../overrides.typ": cvSection, cvSkill, hBar, get, language, resume, format_cv_date, resume_has


#if resume_has("skills") {

  cvSection(language.titles.skills)

  if "languages" in resume {
    cvSkill(
      type: language.titles.languages,
      info: resume.languages.map(get.with(key: "language")).join(hBar()),
    )
  }

  for skill in resume.at("skills", default: ()) {
    cvSkill(
      type: [#skill.name],
      info: skill.keywords.join(hBar()),
    )
  }
}
