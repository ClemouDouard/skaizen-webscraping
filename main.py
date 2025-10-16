from src.crew import run_crew
from scraping import fetch


def summary(topic: str) -> str:
    context = fetch(topic)

    return run_crew(topic, context)
