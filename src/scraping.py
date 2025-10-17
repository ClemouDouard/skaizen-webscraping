from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from dotenv import load_dotenv
import newspaper
from newspaper import Article, news_pool
from datetime import date
from typing import List, Dict
from src.priority.crew import run_prioritize
import json
from time import sleep


def build_date_query(start_date: date, end_date: date) -> str:
    """
    Construit la partie 'date' de la requête Google dans le format attendu.
    Exemple: 'after:2024-01-01 before:2024-12-31'
    """
    formatted_start = start_date.strftime("%Y-%m-%d")
    formatted_end = end_date.strftime("%Y-%m-%d")
    return f"after:{formatted_start} before:{formatted_end}"


def choose_sites_count(search_type: str) -> int:
    """
    Détermine le nombre de sites à considérer selon le type de recherche.
    - 'avance' : 10
    - sinon (incl. 'simple') : 5
    """
    return 10 if str(search_type).lower().strip() == "avance" else 5


def download_articles(query):
    """
    Télécharge les articles via Newspaper3k et ne retourne que 'title' et 'url'.
    Aucun filtrage par date (géré uniquement via la requête Google).
    """
    articles = [Article(e) for e in query]
    news_pool.set(articles)
    news_pool.join()

    res = []
    for i, a in enumerate(articles):
        try:
            a.parse()
            res.append({"url": query[i], "text": a.text})
        except newspaper.article.ArticleException:
            continue

    return res


def search_query(keyword, start, date, search_type="simple"):
    max_sites = choose_sites_count(search_type)
    date_query = build_date_query(start, date)
    query = f"{keyword} {date_query}"

    print(
        f"🔎 Recherche envoyée à Google : {query} | type='{search_type}', sites={max_sites}"
    )
    search_tool = SerperDevTool(n_results=max_sites * 3)
    res = search_tool.run(search_query=query)

    if not isinstance(res, dict) or "organic" not in res:
        print("⚠️ Aucun résultat trouvé ou erreur de Serper.")
        return []

    res = [
        {"url": e["link"], "title": e["title"]} for e in res["organic"] if e.get("link")
    ]
    res = res[:max_sites]

    return res


def priority(search_results):
    # TODO : et si ça boucle à l’infini ??
    while True:
        try:
            return json.loads(run_prioritize(search_results))
        except json.JSONDecodeError:
            continue


def fetch(
    keyword: str, start_date: date, end_date: date, search_type: str = "simple"
) -> List[Dict[str, str]]:
    """
    Construit une requête Google (mot-clé + after/before), ajuste le nombre de sites selon
    le type de recherche, récupère les liens via Serper, puis télécharge les articles.
    Ne renvoie que 'title' et 'url'.
    """
    sleep(1)  # prevent rate limitation
    search_results = search_query(keyword, start_date, end_date, search_type)
    query = priority(search_results)
    sleep(2)
    return download_articles(query)


# Exemple d’utilisation
if __name__ == "__main__":
    start = date(2024, 1, 1)
    end = date(2025, 10, 16)

    # 'simple' => 5 sites ; 'avance' => 10 sites
    articles = fetch("LLM", start, end, search_type="avance")

    for i, art in enumerate(articles, 1):
        print(f"\n--- Article {i} ---")
        # print(f"Titre : {art['title']}")
        print(f"URL : {art['url']}")
