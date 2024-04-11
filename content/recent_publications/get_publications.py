from dataclasses import dataclass
from datetime import datetime
from string import Template

import pyalex


@dataclass
class Publication:

    doi: str
    title: str
    publication_date: str
    abstract: str
    authors: str

    def __dict__(self):

        return {
            "url": self.doi,
            "title": self.title.strip("\n"),
            "date": datetime.strftime(self.publication_date, r"%B %d, %Y"),
            "abstract": self.abstract,
            "authors": self.authors
        }


PI_AUTHOR_ID = "Aa5041305461"
MAX_WORKS = 50
EXCLUDED_PUBLICATIONS = [
    "W4389939228",
    "W4391351611",
    "W4380482838"
]

EXCLUDED_URLS = [
    f"https://openalex.org/{pub}" for pub in EXCLUDED_PUBLICATIONS
]


def main():

    works = pyalex.Works() \
        .filter(author={"id": PI_AUTHOR_ID}) \
        .sort(publication_year="desc") \
        .get(per_page=MAX_WORKS)
    
    publications = []
    for w in works:
        if w["id"] in EXCLUDED_URLS:
            continue

        abstract = w["abstract"]
        if not abstract:
            abstract = ''

        authors = ', '.join(
            authorship["author"]["display_name"] for authorship in w["authorships"]
        )
        
        publications.append(
            Publication(
                doi=w["doi"],
                title=w["title"],
                publication_date=datetime.strptime(w["publication_date"], r"%Y-%m-%d"),
                abstract=abstract,
                authors=authors
            )
        )

    publications.sort(key=lambda x: x.publication_date, reverse=True)

    with open("header.txt", "r") as file:
        src = Template(file.read())

    print(src.substitute({
        "date": str(datetime.today().strftime(r"%B %d, %Y"))
    }))

    with open("template.txt", "r") as file:
        src = Template(file.read())
    
    for p in publications:

        print(src.substitute(p.__dict__()))
    

if __name__ == '__main__':

    main()
