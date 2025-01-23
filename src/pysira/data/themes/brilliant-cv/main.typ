#import "./overrides.typ": cv, metadata, options, personal

#let include_partials(partial, lang: metadata.language) = {
  for module in partial {
    if module == "break" {
      pagebreak()
    }
    else {
      include {
        "partials/" + module + ".typ"
      }
    }
  }
}


#show: cv.with(
  metadata,
  profilePhoto: image(personal.at("image", default: "./static/avatar.jpg")),
)
#include_partials(
  options.at("sections", default:
    (
    "education",
    "work",
    "projects",
    "certificates",
    "publications",
    "skills",
    )
  )
)
