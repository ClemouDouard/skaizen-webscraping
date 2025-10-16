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


summary("LLM")
