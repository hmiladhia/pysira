#import "../overrides.typ": cvSection, cvSkill, diomand, get, language, resume, format_cv_date, resume_has, markdown


#if resume_has("skills") {

  cvSection(language.titles.skills)

  if "languages" in resume {
    cvSkill(
      type: language.titles.languages,
      info: resume.languages.map(get.with(key: "language")).join(diomand()),
    )
  }

  for skill in resume.at("skills", default: ()) {
    cvSkill(
      type: markdown(skill.name),
      info: skill.keywords.join(diomand()),
    )
  }
}
