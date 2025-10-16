from __future__ import annotations
from datetime import date, timedelta
from lorem_text import lorem
from typing import final
import random


def get_dummy_url() -> str:
    res = "https://"
    for _ in range(random.randrange(1, 3)):
        res += lorem.words(random.randrange(5, 10))
    res += ".com"
    return res


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
    topic = current_line.lstrip("#").strip
    cursor += 1
    current_line = lines[cursor].strip()

    # Parsing the bullet points
    bullet_points: list[BulletPoint] = []
    while length > cursor and current_line:
        bullet_point = current_line.lstrip("-").strip()
        start_date, bullet_point = bullet_point.split(":", 1)
        bullet_points.append(BulletPoint(parse_date(start_date), bullet_point))

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


def launchRequest(keywords: str, start_date: date, end_date: date) -> RequestResult:
    # Dummy request result for the moment
    ks = keywords.split()
    sources: list[tuple[str, str]] = [(get_dummy_url(), lorem.sentence()) for _ in ks]
    bullet_points = [
        BulletPoint(
            get_random_date_between(start_date, end_date),
            " ".join(
                [
                    lorem.sentence()
                    + (
                        f"[{random.randrange(0, len(sources))}]"
                        if random.randrange(0, 100) > 65
                        else ""
                    )
                    for _ in range(random.randrange(1, 4))
                ]
            ),
        )
        for _ in ks
    ]
    return RequestResult(keywords, sources, bullet_points)


def date_to_json(self):
    pass


def date_to_md(d: date | None):
    return f"""**{d.strftime("%Y-%m-%d") if d is not None else "?"}**"""


@final
class BulletPoint:
    def __init__(self, d: date | None, text: str):
        self.date = d
        self.text = text

    def to_md(self, sources: list[tuple[str, str]]):
        # todo: handle source references
        return "- " + date_to_md(self.date) + " - " + self.text

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
