from exa_py import Exa

exa = Exa()

def web_search(query:str)->list[dict]:
    results = exa.search_and_contents(query, num_results = 5)
    return [{"title": r.title, "url": r.url, "text": r.text} for r in results.results]
