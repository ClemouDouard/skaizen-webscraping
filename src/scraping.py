from crewai_tools import SerperDevTool
from newspaper import Article, news_pool
from datetime import datetime, date

def download_articles(links, max_articles=5):
    """
    Télécharge les articles depuis les liens fournis via Newspaper3k.
    Aucun filtrage de date ici, car déjà géré dans la requête Google.
    """
    articles = [Article(e) for e in links]
    news_pool.set(articles)
    news_pool.join()

    res = []
    for e in articles:
        try:
            e.parse()
            res.append({
                "title": e.title,
                "url": e.url,
                "publish_date": e.publish_date.date() if e.publish_date else None,
                "text": e.text
            })
            if len(res) >= max_articles:
                break
        except Exception:
            continue

    return res


def fetch(keyword, start_date, end_date, max_articles=5):
    """
    Effectue une recherche Google via SerperDevTool entre deux dates précises,
    puis télécharge les articles correspondants.
    """
    # 🔹 Construire la requête avec filtres de date Google
    formatted_start = start_date.strftime("%Y-%m-%d")
    formatted_end = end_date.strftime("%Y-%m-%d")
    query = f'{keyword} after:{formatted_start} before:{formatted_end}'

    print(f"🔎 Recherche envoyée à Google : {query}")

    # 🔹 Exécuter la recherche Serper
    search_tool = SerperDevTool(n_results=30)
    res = search_tool.run(search_query=query)

    if "organic" not in res:
        print("⚠️ Aucun résultat trouvé ou erreur de Serper.")
        return []

    links = [e["link"] for e in res["organic"]]
    print(f"📄 {len(links)} liens trouvés via Serper")

    # 🔹 Télécharger les articles (sans filtrage de date)
    return download_articles(links, max_articles)


# 🔹 Exemple d’utilisation
if __name__ == "__main__":
    start = date(2023, 10, 1)
    end = date(2025, 10, 16)

    articles = fetch("LLM", start, end, max_articles=5)

    # 🔹 Affichage final
    for i, art in enumerate(articles, 1):
        print(f"\n--- Article {i} ---")
        print(f"Titre : {art['title']}")
        print(f"URL : {art['url']}")
        print(f"Date : {art['publish_date']}")
        # print(f"Contenu (500 premiers caractères) :\n{art['text'][:500]}...\n")
