from copy import deepcopy
from datetime import datetime
from dataclasses import dataclass
from functools import partial
import json
from string import Template


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


def bold_contributors_with_group(paper: Paper, group_members: list[str]) -> Paper:

    new_paper = deepcopy(paper)
    for i, contributor in enumerate(paper.contributors):
        if contributor not in group_members:
            continue
        new_paper.contributors[i] = f'<b>{contributor}</b>'

    return new_paper


def main():

    with open("group_members.txt", "r") as file:
        group_members = file.read().splitlines()

    bold = partial(bold_contributors_with_group, group_members=group_members)

    with open("publications.json", "r") as file:
        paper_dicts = json.load(file)['papers']

    papers = [
        bold(Paper(**paper_dict)) for paper_dict in paper_dicts
    ]

    papers = sorted(papers, key=lambda x: x.date_published, reverse=True)
    snippet = '<hr>\n'.join(paper.html_snippet for paper in papers)
    with open('publications.html', 'w') as file:
        print(f'<hr>\n{snippet}<hr>', file=file)


if __name__ == '__main__':

    main()
