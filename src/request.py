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


def get_random_date_interval(start: date, end: date) -> DateInterval:
    days: int = (end - start).days
    duration = timedelta(days=random.randrange(1, days))
    return DateInterval(start, start + duration)


def launchRequest(keywords: str, start_date: date, end_date: date) -> RequestResult:
    # Dummy request result for the moment
    ks = keywords.split()
    sources = [get_dummy_url() for _ in ks]
    bullet_points = [
        BulletPoint(
            get_random_date_interval(start_date, end_date),
            " ".join(
                (
                    lorem.sentence()
                    + (
                        f"[{random.randrange(0, len(sources))}]"
                        if random.randrange(0, 100) > 65
                        else ""
                    )
                    for _ in range(random.randrange(1, 4))
                )
            ),
        )
        for _ in ks
    ]
    return RequestResult(keywords, sources, bullet_points)


@final
class DateInterval:
    def __init__(self, start: date, end: date):
        self.start = start
        self.end = end

    def to_md(self):
        return f"""**{self.start.strftime("%Y-%m-%d")} - {self.end.strftime("%Y-%m-%d")}**"""

    def to_json(self):
        pass


@final
class BulletPoint:
    def __init__(self, date: DateInterval, text: str):
        self.date = date
        self.text = text

    def to_md(self, sources: list[str]):
        # todo: handle source references
        return "- " + self.date.to_md() + " - " + self.text

    def to_json(self):
        pass


@final
class RequestResult:
    def __init__(
        self, request: str, sources: list[str], bullet_points: list[BulletPoint]
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
