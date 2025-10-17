from src.crew import run_summary, run_prioritize
from src.scraping import fetch
from datetime import date

import json


def list_to_json_str(texts):
    data = {"articles": []}

    for i, text in enumerate(texts, 1):
        data["articles"].append({"id": i, "content": text.strip()})

    return json.dumps(data, ensure_ascii=False, indent=2)

def parse_search_result(res):
    r = {"link":[], "name":[]}
    for e in res:
        r["link"].append(e["url"])
        r["name"].append(e["title"])

    return r


def summary(topic: str) -> str:
    context = fetch(topic)

    return run_summary(topic, list_to_json_str(context))

def priority(request, start, end):
    res = fetch(request,start,end)
    inp = parse_search_result(res)

    return run_prioritize(inp)

#summary("LLM")

print(priority("LLM",date(2025,4,1), date(2025,7,7)))
