#import "../overrides.typ": cvSection, cvHonor, language, resume, extract_year, resume_has, markdown

#if resume_has("certificates") {

  cvSection(language.titles.certificates)

  for cert in resume.certificates {
    cvHonor(
      date: extract_year(cert.date),
      title: cert.name,
      issuer: cert.at("issuer", default: ""),
      url: cert.at("url", default: ""),
    )
  }

}
