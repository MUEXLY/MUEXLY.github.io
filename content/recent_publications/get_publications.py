import requests
import re
import time
from dataclasses import dataclass
from datetime import datetime
from string import Template
from pathlib import Path

from scholarly_publications import fetch_publications


@dataclass
class Publication:

    title: str
    date: datetime
    url: str

    def __dict__(self):

        return {
            "title": self.title,
            "date": self.date.strftime("%B %d, %Y"),
            "url": self.url
        }


HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
}

COOKIES = {
    'CONSENT': 'PENDING+300',
}


DATE_PATTERNS = [
    re.compile(r'<div class="gsc_oci_value">([0-9]+/[0-9]+/[0-9]+)</div>'),
    re.compile(r'<div class="gsc_oci_value">([0-9]+/[0-9]+)</div>'),
    re.compile(r'<div class="gsc_oci_value">([0-9]+)</div>')
]

DATETIME_PATTERNS = [
    r"%Y/%m/%d",
    r"%Y/%m",
    r"%Y"
]

MAX_PUBS = 50

PI_AUTHOR_ID = "Zy5TYLjEDukC"

WAIT_TIME = 10


def main():

    all_pubs = []
        
    for p in fetch_publications(PI_AUTHOR_ID, max_publications=MAX_PUBS, sortby='pubdate'):
        url = p["link"]
        request_kwargs = {
            "proxies": {
                "http": FreeProxy(rand=True).get(),
                "https": FreeProxy(rand=True).get()
            },
            "verify": False
        }
        response = requests.get(url, cookies=COOKIES, headers=HEADERS)
        if response.status_code != 200:
            raise ValueError(response)
        
        match = None
        for pattern in DATE_PATTERNS:
            match = re.search(pattern, response.text)
            if match:
                break
        if not match:
            raise ValueError(url)
        
        pub_date = None
        for pattern in DATETIME_PATTERNS:
            try:
                pub_date = datetime.strptime(match.group(1), pattern)
                break
            except ValueError:
                continue
        if not pub_date:
            raise ValueError(url)
        publication = Publication(
            title=p["title"],
            date=pub_date,
            url=url
        )
        all_pubs.append(publication)
        
        time.sleep(WAIT_TIME)
        print('pub added')

    all_pubs.sort(key=lambda x: x.date, reverse=True)
    all_pubs = all_pubs[:MAX_PUBS]
    
    with open(Path("header.txt"), "r") as file:
        print(file.read())

    with open(Path("template.txt"), "r") as file:

        template = Template(file.read())
    
    for pub in all_pubs:
        
        result = template.substitute(
            {
                "title": pub.title,
                "date": pub.date.strftime("%B %d, %Y"),
                "url": pub.url
            }
        )
        print(result)



if __name__ == '__main__':

    main()
