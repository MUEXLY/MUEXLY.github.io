from dataclasses import dataclass
from datetime import datetime
from string import Template
import json
from pathlib import Path

import pyalex


@dataclass
class Publication:

    doi: str
    title: str
    publication_date: str
    abstract: str
    authors: str
    id: str

    def __dict__(self):

        return {
            "url": self.doi,
            "title": self.title.strip("\n"),
            "date": datetime.strftime(self.publication_date, r"%B %Y"),
            "abstract": self.abstract,
            "authors": self.authors
        }
        
    def __hash__(self):
    
        return hash(self.id)
    

@dataclass
class Config:

    pi_author_ids: list[str]
    max_works: int
    excluded_publications: list[str]
    authors_to_bold: list[str]


CONFIG_PATH = Path("config.json")
with open(CONFIG_PATH, "r") as file:
    CONFIG = Config(**json.load(file))

EXCLUDED_URLS = [
    f"https://openalex.org/{pub}" for pub in CONFIG.excluded_publications
]


def main():

    publications = []
    
    for author_id in CONFIG.pi_author_ids:
    
        works = pyalex.Works() \
            .filter(author={"id": author_id}) \
            .sort(publication_year="desc") \
            .get(per_page=CONFIG.max_works)
        for w in works:
            if w["id"] in EXCLUDED_URLS:
                continue
    
            abstract = w["abstract"]
            if not abstract:
                abstract = ''
    
            authors = ', '.join(
                authorship["author"]["display_name"] for authorship in w["authorships"]
            )

            # replace double last name with single last name

            if "Enrique Martínez Sáez" in authors:
                authors = authors.replace("Enrique Martínez Sáez", "Enrique Martínez")

            for author in CONFIG.authors_to_bold:
                authors = authors.replace(author, f"<b>{author}</b>")
            
            publications.append(
                Publication(
                    doi=w["doi"],
                    title=w["title"],
                    publication_date=datetime.strptime(w["publication_date"], r"%Y-%m-%d"),
                    abstract=abstract,
                    authors=authors,
                    id=w["id"]
                )
            )

    # remove duplicates
    publications = list(set(publications))
    
    # sort
    publications.sort(key=lambda x: x.publication_date, reverse=True)

    with open("header.txt", "r") as file:
        src = Template(file.read())

    print(src.substitute({
        "date": str(datetime.today().strftime(r"%B %d, %Y"))
    }))

    with open("template.txt", "r") as file:
        src = Template(file.read())
    
    for p in publications[:CONFIG.max_works]:

        print(src.substitute(p.__dict__()))
    

if __name__ == '__main__':

    main()
