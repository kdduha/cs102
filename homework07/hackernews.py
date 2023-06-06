import re

import pymorphy2  # type: ignore
from bayes import NaiveBayesClassifier
from bottle import redirect, request, route, run, template  # type: ignore
from db import News, session
from scraputils import get_news


@route("/")
@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template("news_template", rows=rows)


@route("/add_label/")
def add_label():
    s = session()
    label, id = request.query.label, request.query.id
    row = s.query(News).filter(News.id == id).one()
    row.label = label
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    s = session()
    table = get_news("https://news.ycombinator.com/newest")
    for news in table:
        if len(s.query(News).filter(News.title == news["title"] and News.author == news["author"]).all()) == 0:
            n = News(
                title=news["title"],
                author=news["author"],
                url=news["url"],
                comments=news["comments"],
                points=news["points"],
                label=None,
            )
            s.add(n)
        s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    s = session()
    bayes = NaiveBayesClassifier()
    classified = s.query(News).filter(News.label != None).all()
    X = [i.title for i in classified]
    Y = [i.label for i in classified]

    # лемматизация
    morph = pymorphy2.MorphAnalyzer()
    for i, x in enumerate(X):
        X[i] = re.sub(r"[^А-Яа-я]+", " ", X[i].lower()).strip(" ")
        normalized = []
        for word in x.split(" "):
            normal_word = morph.parse(word)[0].normal_form
            normalized.append(normal_word)
        X[i] = " ".join(normalized)

    bayes.fit(X, Y)
    news = s.query(News).filter(News.label == None).all()[:3]
    X_test = [i.title if i.title is not None else "" for i in news]
    result = bayes.predict(X_test)
    for i in range(len(news)):
        news[i].label = result[i]
    s.commit()
    classified_new = sorted(news, key=lambda x: x.label)
    return classified_new


@route("/recommendations")
def recommend():
    classified_news = classify_news()
    return template("news_recommendations", rows=classified_news)


if __name__ == "__main__":
    run(host="localhost", port=8080)
