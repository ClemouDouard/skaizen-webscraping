from src.summary.crew import run_summary
from src.priority.crew import run_prioritize
from src.scraping import fetch, search_query
from datetime import date

from datetime import date
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


def summary(topic: str) -> str:
    context = fetch(topic, date(2023, 10, 16), date(2025, 10, 16))

    if not context:
        print("⚠️ Aucun article trouvé, résumé impossible.")
        return "No articles found."

    context_json = list_to_json_str(context)

    return run_summary(topic, context_json)


def priority(request, start, end):
    search_results = search_query(request, start, end)
    return run_prioritize(search_results)


if __name__ == "__main__":
    priority("LLM", date(2025, 4, 1), date(2025, 7, 1))
