import requests  # type: ignore
from bs4 import BeautifulSoup  # type: ignore


def extract_news(parser):
    """Extract news from a given web page"""
    news_list = []

    tbl_news_list = parser.table.findAll("table")[1]
    title_line = tbl_news_list.findAll("span", {"class": "titleline"})
    sub_line = tbl_news_list.findAll("td", {"class": "subtext"})

    titles, links, points, auths, comments = [], [], [], [], []

    for line in title_line:
        titles.append(line.a.text)
        links.append(line.a["href"])

    for line in sub_line:
        if line.find("span", {"class": "subline"}) is None:
            point = 0
            auth = "None"
            comment = 0
        else:
            point = line.span.span.text.split()[0]
            all_a_objects = line.findAll("a")
            auth = all_a_objects[0].text
            comment = all_a_objects[-1].text.split()[0]

        points.append(point)
        auths.append(auth)
        comments.append(comment)

    for i, _ in enumerate(titles):
        news_list.append(
            {
                "author": auths[i],
                "comments": int(comments[i]) if comments[i] != "discuss" else 0,
                "points": int(points[i]),
                "title": titles[i],
                "url": links[i],
            }
        )

    return news_list


def extract_next_page(parser):
    """Extract next page URL"""
    tbl_news_list = parser.table.findAll("table")[1]
    link = tbl_news_list.find("a", {"class": "morelink"})
    return link["href"] if link is not None else ""


def get_news(url, n_pages=1):
    """Collect news from a given web page"""
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news
