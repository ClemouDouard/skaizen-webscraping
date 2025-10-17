from __future__ import annotations
from datetime import date, timedelta
from typing import final
import random
from src.summary.crew import run_summary
from src.scraping import fetch
import json


def list_to_json_str(articles):
    """
    Transforme une liste de dictionnaires {'url', 'title', 'text'}
    en une chaîne JSON formatée proprement.
    """
    data = {"articles": []}

    for i, article in enumerate(articles, 1):
        url = article.get("url", "").strip()
        title = article.get("title", "Untitled").strip()
        text = article.get("text", "").strip()

        # On ignore les entrées vides
        if not text:
            continue

        data["articles"].append({"id": i, "url": url, "title": title, "content": text})

    return json.dumps(data, ensure_ascii=False, indent=2)


def summary(topic: str, start_date: date, end_date: date):
    context = fetch(topic, start_date, end_date)

    if not context:
        print("⚠️ Aucun article trouvé, résumé impossible.")
        return ("No articles found.", [])

    context_json = list_to_json_str(context)
    sources = [(dict["url"], "Dummy Title") for dict in context]

    return (run_summary(topic, context_json), sources)


def parse_date(input: str) -> date | None:
    year, month, day = map(lambda x: int(x), input.strip().strip('"').split("-"))
    return date(year, month, day)


def parse_result(markdown: str) -> RequestResult | None:
    lines = map(lambda x: x.strip(), markdown.split("\n"))
    lines = [line for line in lines if len(line) > 0]

    if lines[0] != "# Sources":
        return None
    cursor = 1
    current_line = lines[cursor].strip()
    length = len(lines)

    # Parsing the sources
    sources: list[tuple[str, str]] = []
    while length > cursor and current_line and current_line[0] != "#":
        source = current_line.lstrip("-").strip()
        source, title = source.split("-", 1)
        sources.append((source.strip(), title.strip()))

        cursor += 1
        if length <= cursor:
            break
        current_line = lines[cursor]

    if length <= cursor:
        # There is no summary after the links ?
        return None

    # Parsing the topic
    topic: str = current_line.lstrip("#").strip()
    cursor += 1
    current_line = lines[cursor].strip()

    # Parsing the bullet points
    bullet_points: list[BulletPoint] = []
    while length > cursor and current_line:
        bullet_point = current_line.lstrip("-").strip()
        start_date, bullet_point = bullet_point.split(":", 1)
        bullet_points.append(BulletPoint(start_date, bullet_point))

        cursor += 1
        if length <= cursor:
            break
        current_line = lines[cursor].strip()

    return RequestResult(topic, sources, bullet_points)


def get_random_date_between(start: date, end: date) -> date:
    # Return a random date between start and end (inclusive)
    if start > end:
        start, end = end, start
    delta_days = (end - start).days
    return start + timedelta(days=random.randint(0, delta_days))


def launchRequest(
    keywords: str, start_date: date, end_date: date, advanced: bool
) -> RequestResult | DummyToMd:
    (sum, sources) = summary(keywords, start_date, end_date)
    res = parse_result(sum)
    if res is None:
        return DummyToMd(sum, sources)
    return res


class DummyToMd:
    def __init__(self, txt: str, sources):
        self.txt = txt
        self.sources = sources

    def to_md(self):
        return self.txt

    def get_sources(self):
        return self.sources


def date_to_json(d: date | None):
    pass


def date_to_md(d: date | None):
    return f"""**{d.strftime("%Y-%m-%d") if d is not None else "?"}**"""


@final
class BulletPoint:
    def __init__(self, d: str, text: str):
        self.date = d
        self.text = text

    def to_md(self, sources: list[tuple[str, str]]):
        # todo: handle source references
        return "- " + self.text

    def to_json(self):
        pass


@final
class RequestResult:
    def __init__(
        self,
        request: str,
        sources: list[tuple[str, str]],
        bullet_points: list[BulletPoint],
    ):
        self.request = request
        self.sources = sources
        self.bullet_points = bullet_points

    def to_md(self):
        res = ""
        for bullet in self.bullet_points:
            res += bullet.to_md(self.sources) + "\n"
        return res

    def to_json(self):
        pass

    def get_sources(self):
        return self.sources
