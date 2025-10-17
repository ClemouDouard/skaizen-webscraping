from src.crew import run_summary, run_prioritize
from src.scraping import fetch
from datetime import date

from datetime import date
import json


def list_to_json_str(articles):
    data = {"articles": []}

    for i, article in enumerate(articles, 1):
        title = article.get("title", "Untitled")
        url = article.get("url", "")
        publish_date = (
            article["publish_date"].isoformat() if article.get("publish_date") else "?"
        )
        text = article.get("text", "").strip()

        if not text:
            continue

        data["articles"].append(
            {
                "id": i,
                "title": title,
                "url": url,
                "publish_date": publish_date,
                "content": text,
            }
        )

    return json.dumps(data, ensure_ascii=False, indent=2)

def parse_search_result(res):
    r = {"link":[], "name":[]}
    for e in res:
        r["link"].append(e["url"])
        r["name"].append(e["title"])

    return r


def summary(topic: str) -> str:
    context = fetch(topic, date(2023, 10, 16), date(2025, 10, 16))

    if not context:
        print("⚠️ Aucun article trouvé, résumé impossible.")
        return "No articles found."

    context_json = list_to_json_str(context)

    return run_crew(topic, context_json)

def priority(request, start, end):
    res = fetch(request,start,end)
    inp = parse_search_result(res)
    return run_prioritize(inp)

if __name__ == "__main__":
    print(summary("LLM"))
