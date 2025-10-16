from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from dotenv import load_dotenv
import newspaper
from newspaper import Article, news_pool

load_dotenv()

#search_tool = SerperDevTool(n_results=5)
#
#print(
#   search_tool.run(
#       search_query="LLM",
#   )
#)

"""
Output Example:
    {'searchParameters': {'q': 'LLM', 'type': 'search', 'num': 5, 'engine': 'google'}, 'organic': [{'title': 'Large language model - Wikipedia', 'link': 'https://en.wikipedia.org/wiki/Large_language_model', 'snippet': 'A large language model (LLM) is a language model trained with self-supervised machine learning on a vast amount of text, designed for natural language ...', 'position': 1, 'sitelinks': [{'title': 'LLM (disambiguation)', 'link': 'https://en.wikipedia.org/wiki/LLM_(disambiguation)'}, {'title': 'List', 'link': 'https://en.wikipedia.org/wiki/List_of_large_language_models'}, {'title': 'Prompt engineering', 'link': 'https://en.wikipedia.org/wiki/Prompt_engineering'}, {'title': 'Self-supervised learning', 'link': 'https://en.wikipedia.org/wiki/Self-supervised_learning'}]}, {'title': 'What is an LLM (large language model)? - Cloudflare', 'link': 'https://www.cloudflare.com/learning/ai/what-is-large-language-model/', 'snippet': 'LLMs are machine learning AI programs that comprehend and generate human language text, trained on large datasets to recognize and interpret language.', 'position': 2}, {'title': 'Google NotebookLM | AI Research Tool & Thinking Partner', 'link': 'https://notebooklm.google/', 'snippet': 'Meet NotebookLM, the AI research tool and thinking partner that can analyze your sources, turn complexity into clarity and transform your content.', 'position': 3}, {'title': 'What Are Large Language Models (LLMs)? - IBM', 'link': 'https://www.ibm.com/think/topics/large-language-models', 'snippet': 'Large language models are AI systems capable of understanding and generating human language by processing vast amounts of text data.', 'position': 4}, {'title': 'What is LLM (Large Language Model)? - AWS', 'link': 'https://aws.amazon.com/what-is/large-language-model/', 'snippet': 'Large language models, also known as LLMs, are very large deep learning models that are pre-trained on vast amounts of data.', 'position': 5}], 'peopleAlsoAsk': [{'question': 'Is LLM better than AI?', 'snippet': '👉🏼If you need AI-generated images, music, videos, or creative assets, Generative AI is the right fit. 👉🏼If your business relies on text automation, customer support, or research, an LLM is the better choice.', 'title': 'LLM vs. Generative AI – Know the Differences and Use Cases', 'link': 'https://zerogravitymarketing.com/blog/large-language-model-vs-generative-ai/'}], 'relatedSearches': [{'query': 'LLM AI'}, {'query': 'LLM Law'}, {'query': 'LLM model'}, {'query': 'LLM free'}, {'query': 'LLM ChatGPT'}], 'credits': 1}
"""

def download_articles(links):
    articles = [Article(e) for e in links]
    news_pool.set(articles)
    news_pool.join()

    res = []
    for e in articles:
        try:
            e.parse()
            res.append(e.text)
        except newspaper.article.ArticleException:
            res.append("")

    return res

def fetch(query, start_date=1, end_date=1):
    search_tool = SerperDevTool(n_results=5)
    res = search_tool.run(search_query=query)
    links = [e["link"] for e in res["organic"]]
    print(links)

    return download_articles(links)



print(fetch("LLM")[0])
