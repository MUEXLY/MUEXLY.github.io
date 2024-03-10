from dataclasses import dataclass
from string import Template
import json


@dataclass
class HighlightedWork:

    media_url: str
    description: str
    
    @property
    def html_snippet(self) -> str:
        
        with open("html_snippet_template.txt", "r") as file:
            src = Template(file.read())
            return src.substitute(
                {
                    "media_url": self.media_url,
                    "description": self.description
                }
            )


def main():

    with open("highlighted_works.json", "r") as file:
        highlighted_works = json.load(file)["highlighted_works"]
        
    highlighted_works = [HighlightedWork(**h) for h in highlighted_works]
    
    snippet = '<hr>\n'.join(work.html_snippet for work in highlighted_works)
    with open("highlighted_works.html", "w") as file, open("highlighted_works_template.txt", "r") as template:
        src = Template(template.read())
        full_html = src.substitute({"content": f'<hr>\n{snippet}<hr>'})
        print(full_html, file=file)
        
        
if __name__ == '__main__':

    main()
