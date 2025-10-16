from __future__ import annotations
from datetime import date, timedelta
from typing import final
import random
from src.crew import run_crew
from src.scraping import fetch
import json


def list_to_json_str(texts):
    data = {"articles": []}

    for i, text in enumerate(texts, 1):
        data["articles"].append({"id": i, "content": text.strip()})

    return json.dumps(data, ensure_ascii=False, indent=2)


def summary(topic: str) -> str:
    context = fetch(topic)

    return run_crew(topic, list_to_json_str(context))


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
        start_date, bullet_point = bullet_point.split("-", 1)
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


def launchRequest(keywords: str, _start_date: date, _end_date: date) -> RequestResult:
    res = parse_result(summary(keywords))
    if res is None:
        raise NotImplementedError("PARSE ERROR")
    return res


def launchRequestDebug(keywords: str) -> str:
    return summary(keywords)


def date_to_json(d: date | None):
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
