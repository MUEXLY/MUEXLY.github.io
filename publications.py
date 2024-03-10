from datetime import datetime
from dataclasses import dataclass
from string import Template
import json


@dataclass
class Paper:

    title: str
    doi: str
    contributors: list[str]
    abstract: str
    day: int
    month: int
    year: int

    @property
    def formatted_contributors(self) -> str:
        return ', '.join(self.contributors)
    
    @property
    def date_published(self) -> datetime:
        return datetime(self.year, self.month, self.day)
    
    @property
    def formatted_date(self) -> str:
        return self.date_published.strftime(r"%B %d, %Y")
    
    @property
    def html_snippet(self) -> str:

        with open('html_snippet_template.txt', 'r') as file:
            src = Template(file.read())
            return src.substitute(
                {
                    "title": self.title,
                    "formatted_contributors": self.formatted_contributors,
                    "formatted_date": self.formatted_date,
                    "abstract": self.abstract,
                    "doi": self.doi
                }
            )

with open("group_members.txt", "r") as file:
    group_members = file.read().splitlines()

def bold(member) -> str:
    if member in group_members:
        return f'<b>{member}</b>'
    return member

with open("papers.jsonl", "r") as file:
    papers = []
    for line in file:
        paper_dict = json.loads(line)
        paper_dict['contributors'] = [
            bold(contributor) for contributor in paper_dict['contributors']
        ]
        papers.append(
            Paper(**paper_dict)
        )

papers = sorted(papers, key=lambda paper: paper.date_published, reverse=True)
snippet = '<hr>\n'.join(paper.html_snippet for paper in papers)
print(f'<hr>\n{snippet}<hr>')