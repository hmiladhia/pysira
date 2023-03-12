from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Award:
    title: str
    awarder: str
    summary: str
    date: str

    @staticmethod
    def from_dict(obj: Any) -> Award:
        _title = obj.get('title')
        _awarder = obj.get('awarder')
        _summary = obj.get('summary')
        _date = obj.get('date')
        return Award(_title, _awarder, _summary, _date)


@dataclass
class Profile:
    network: str
    url: str
    username: str

    @staticmethod
    def from_dict(obj: Any) -> Profile:
        _network = obj.get('network')
        _url = obj.get('url')
        _username = obj.get('username')
        return Profile(_network, _url, _username)


@dataclass
class Location:
    postalCode: str
    city: str
    countryCode: str
    region: str

    @staticmethod
    def from_dict(obj: Any) -> Location:
        _postalCode = obj.get('postalCode')
        _city = obj.get('city')
        _countryCode = obj.get('countryCode')
        _region = obj.get('region')
        return Location(_postalCode, _city, _countryCode, _region)


@dataclass
class Basics:
    name: str
    label: str
    image: str
    email: str
    phone: str
    url: str
    website: str
    summary: str
    location: Location
    profiles: list[Profile]

    image_path: str = None
    image_b64: str = None
    image_b64_mime_type: str = None

    @staticmethod
    def from_dict(obj: Any) -> Basics:
        _name = obj.get('name')
        _label = obj.get('label')
        _image = obj.get('image')
        _email = obj.get('email')
        _phone = obj.get('phone')
        _url = obj.get('url')
        _website = obj.get('website')
        _summary = obj.get('summary')
        _location = Location.from_dict(obj.get('location'))
        _profiles = [Profile.from_dict(y) for y in obj.get('profiles', [])]
        return Basics(
            _name,
            _label,
            _image,
            _email,
            _phone,
            _url,
            _website,
            _summary,
            _location,
            _profiles,
        )


@dataclass
class Certificate:
    name: str
    date: str
    url: str
    issuer: str

    @staticmethod
    def from_dict(obj: Any) -> Certificate:
        _name = obj.get('name')
        _date = obj.get('date')
        _url = obj.get('url')
        _issuer = obj.get('issuer')
        return Certificate(_name, _date, _url, _issuer)


@dataclass
class Education:
    institution: str
    url: str
    area: str
    studyType: str
    startDate: str
    score: str
    courses: list[str]
    endDate: str

    @staticmethod
    def from_dict(obj: Any) -> Education:
        _institution = obj.get('institution')
        _url = obj.get('url')
        _area = obj.get('area')
        _studyType = obj.get('studyType')
        _score = obj.get('score')
        _courses = obj.get('courses', [])

        _startDate = obj.get('startDate')
        _endDate = obj.get('endDate')
        return Education(
            _institution,
            _url,
            _area,
            _studyType,
            _startDate,
            _score,
            _courses,
            _endDate,
        )


@dataclass
class Interest:
    name: str
    keywords: list[str]

    @staticmethod
    def from_dict(obj: Any) -> Interest:
        _name = obj.get('name')
        _keywords = obj.get('keywords', [])
        return Interest(_name, _keywords)


@dataclass
class Language:
    language: str
    fluency: str

    @staticmethod
    def from_dict(obj: Any) -> Language:
        _language = obj.get('language')
        _fluency = obj.get('fluency')
        return Language(_language, _fluency)


@dataclass
class Meta:
    canonical: str
    version: str
    lastModified: str
    language: str

    @staticmethod
    def from_dict(obj: Any) -> Meta:
        _canonical = obj.get('canonical')
        _version = obj.get('version')
        _lastModified = obj.get('lastModified')
        _language = obj.get('language', 'en')
        return Meta(_canonical, _version, _lastModified, _language)


@dataclass
class Project:
    name: str
    description: str
    highlights: list[str]
    keywords: list[str]
    roles: list[str]
    entity: str
    startDate: str
    url: str
    type: str
    endDate: str

    @staticmethod
    def from_dict(obj: Any) -> Project:
        _name = obj.get('name')
        _description = obj.get('description')
        _highlights = obj.get('highlights', [])
        _keywords = obj.get('keywords', [])
        _roles = obj.get('roles', [])
        _entity = obj.get('entity')
        _url = obj.get('url')
        _type = obj.get('type')

        _startDate = obj.get('startDate')
        _endDate = obj.get('endDate')
        return Project(
            _name,
            _description,
            _highlights,
            _keywords,
            _roles,
            _entity,
            _startDate,
            _url,
            _type,
            _endDate,
        )


@dataclass
class Publication:
    name: str
    publisher: str
    summary: str
    releaseDate: str
    url: str

    @staticmethod
    def from_dict(obj: Any) -> Publication:
        _name = obj.get('name')
        _publisher = obj.get('publisher')
        _summary = obj.get('summary')
        _releaseDate = obj.get('releaseDate')
        _url = obj.get('url')
        return Publication(_name, _publisher, _summary, _releaseDate, _url)


@dataclass
class Reference:
    reference: str
    name: str

    @staticmethod
    def from_dict(obj: Any) -> Reference:
        _reference = obj.get('reference')
        _name = obj.get('name')
        return Reference(_reference, _name)


@dataclass
class Skill:
    name: str
    level: str
    keywords: list[str]

    @staticmethod
    def from_dict(obj: Any) -> Skill:
        _name = obj.get('name')
        _level = obj.get('level')
        _keywords = obj.get('keywords', [])
        return Skill(_name, _level, _keywords)


@dataclass
class Volunteer:
    organization: str
    position: str
    url: str
    summary: str
    startDate: str
    highlights: list[str]
    endDate: str

    @staticmethod
    def from_dict(obj: Any) -> Volunteer:
        _organization = obj.get('organization')
        _position = obj.get('position')
        _url = obj.get('url')
        _summary = obj.get('summary')
        _highlights = obj.get('highlights')
        _startDate = obj.get('startDate')
        _endDate = obj.get('endDate')
        return Volunteer(
            _organization, _position, _url, _summary, _startDate, _highlights, _endDate
        )


@dataclass
class Work:
    summary: str
    name: str
    website: str
    location: str
    position: str
    startDate: str
    highlights: list[str]
    url: str
    endDate: str

    @staticmethod
    def from_dict(obj: Any) -> Work:
        _summary = obj.get('summary')
        _name = obj.get('name')
        _website = obj.get('website')
        _location = obj.get('location')
        _position = obj.get('position')
        _highlights = obj.get('highlights', [])
        _url = obj.get('url')

        _startDate = obj.get('startDate')
        _endDate = obj.get('endDate')
        return Work(
            _summary,
            _name,
            _website,
            _location,
            _position,
            _startDate,
            _highlights,
            _url,
            _endDate,
        )


@dataclass
class ResumeData:
    basics: Basics
    work: list[Work]
    volunteer: list[Volunteer]
    education: list[Education]
    skills: list[Skill]
    awards: list[Award]
    languages: list[Language]
    projects: list[Project]
    certificates: list[Certificate]
    interests: list[Interest]
    publications: list[Publication]
    references: list[Reference]
    meta: Meta
    schema: str = None

    @staticmethod
    def from_dict(obj: dict[str]) -> ResumeData:
        _schema = obj.get('$schema', None)
        _basics = Basics.from_dict(obj.get('basics'))
        _work = [Work.from_dict(y) for y in obj.get('work', [])]
        _volunteer = [Volunteer.from_dict(y) for y in obj.get('volunteer', [])]
        _education = [Education.from_dict(y) for y in obj.get('education', [])]
        _skills = [Skill.from_dict(y) for y in obj.get('skills', [])]
        _awards = [Award.from_dict(y) for y in obj.get('awards', [])]
        _languages = [Language.from_dict(y) for y in obj.get('languages', [])]
        _projects = [Project.from_dict(y) for y in obj.get('projects', [])]
        _certificates = [Certificate.from_dict(y) for y in obj.get('certificates', [])]
        _interests = [Interest.from_dict(y) for y in obj.get('interests', [])]
        _publications = [Publication.from_dict(y) for y in obj.get('publications', [])]
        _references = [Reference.from_dict(y) for y in obj.get('references', [])]
        _meta = Meta.from_dict(obj.get('meta', {}))
        return ResumeData(
            _basics,
            _work,
            _volunteer,
            _education,
            _skills,
            _awards,
            _languages,
            _projects,
            _certificates,
            _interests,
            _publications,
            _references,
            _meta,
            schema=_schema,
        )
