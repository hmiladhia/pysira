#import "lib/brilliant-cv.typ": cv, cvSection, cvEntry, cvHonor, hBar, cvSkill, cvPublication

#let resume = yaml("resume.yaml")
#let options = yaml("options.yaml")
#let language = yaml("language.yaml")
#let extra = yaml("extra.yaml")
#let personal = resume.basics

#let resume_has(str)=resume.at(str, default: ()).len() > 0

// #let empty_dict() = {let d=("hello": none); d.remove("hello"); d}
#let empty_dict() = ().to-dict()
#let insert_if_not_none(d, k, v) = {
  if v != none {d.insert(k, v)}
  d
}

#let get(dict, key: str)= dict.at(key, default: none)
#let by_key(pr, key: str, val: str)=get(pr, key: key) == val
// #let get_profile(network)={
//   let cprofiles = personal.at("profiles", default: ()).filter(by_key.with(key: "network", val: network))
//   cprofiles.at(0, default: empty_dict()).at("url", default: none)
// }
#let get_profile(network)={
  let cprofiles = personal.at("profiles", default: ()).filter(by_key.with(key: "network", val: network))
  cprofiles.at(0, default: none)
}
#let get_profile_link(network)={
  let profile = get_profile(network)
  if profile == none { return none }
  let profile_url = profile.at("url", default: none)
  if profile_url == none { return none }

  profile.at("username", default: profile_url)
}


#let extract_year(date)= date.split("-").at(0, default: none)
#let format_cv_date(entry)={
  let start_date = extract_year(entry.startDate)
  let end_date = extract_year(entry.at("endDate", default: ""))

  if end_date in (none, "") {end_date = language.phrases.present}
  [ #start_date - #end_date]
}

#let greenList = (
    "github",
    "linkedin",
    "gitlab",
    "orcid",
    "researchgate",
    "extraInfo"
  )

#let metadata = {
  let metadata = (
    layout: (
        awesome_color: options.awesome_color,
        before_section_skip: options.before_section_skip,
        before_entry_skip: options.before_entry_skip,
        before_entry_description_skip: options.before_entry_description_skip,
        paper_size: options.paper_size,
        fonts: (
          regular_fonts: options.regular_fonts,
          header_font: options.header_font,
        ),
        header: (
          header_font: options.header_font,
          header_align: options.header_align,
          display_profile_photo: options.display_profile_photo,
        ),
        entry: (
          display_entry_society_first: options.display_entry_society_first,
          display_tags_first: options.display_tags_first,
          display_logo: options.display_logo,
        ),
        skill: (
          category_size: options.skill_category_size
        )
    ),
    inject: (
      inject_ai_prompt: options.inject_ai_prompt,
      inject_keywords: options.inject_keywords,
      injected_keywords_list: options.injected_keywords_list,
    ),
  )

  let _full_personal_info=(
        phone: get(personal, key: "phone"),
        email: get(personal, key: "email"),
        homepage: get(personal, key: "url"),
        github: get_profile_link("github"),
        linkedin: get_profile_link("linkedin"),
        gitlab: get_profile_link("gitlab"),
        orcid: get_profile_link("orcid"),
        researchgate: get_profile_link("researchgate"),
        extraInfo: get_profile_link("extraInfo"),
      )
  let personal_info=empty_dict()
  for (key, value) in _full_personal_info.pairs() {
    personal_info = insert_if_not_none(personal_info, key, value)
  }

  for profile in personal.profiles {
    let network = profile.network
    if network in greenList {continue
    }
    personal_info = insert_if_not_none(personal_info, "custom" + network, (
      "awesomeIcon": profile.network,
      "link": profile.url,
      "text": profile.at("username", default: profile.url),
    ))
  }

  metadata.insert("personal",
    (
      first_name: personal.name.split(" ").at(0),
      last_name: personal.name.split(" ").slice(1).join(" "),
      info: personal_info
    )
  )

  metadata.insert("language", language.id)

  let additional_info = (
    "header_quote": personal.at("summary", default: "").split("\n").at(0),
    "cv_footer": options.at("footer", default: "")
  )

  metadata.insert("lang", (language.id: additional_info))

  metadata
}

#let cvSection = cvSection.with(metadata: metadata)
#let cvEntry = cvEntry.with(metadata: metadata)
#let cvHonor = cvHonor.with(metadata: metadata)
#let cvSkill = cvSkill.with(metadata: metadata)
