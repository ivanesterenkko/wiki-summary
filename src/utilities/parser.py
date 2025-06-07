import httpx
from bs4 import BeautifulSoup

from src.crud.article import crud_article
from src.schemas.article import ArticleCreateDB

class WikiParserService:
    def __init__(self):
        self.visited = set()
        self.crud_article = crud_article

    async def parse(self, db, url: str, parent_id: int = None, depth: int = 0, max_depth: int = 5):
        if depth >= max_depth or url in self.visited:
            return 0
        links = None
        article_obj = await crud_article.get_by_url(db, url)
        if article_obj:
            links = [child.url for child in article_obj.children]
        if not article_obj:
            async with httpx.AsyncClient() as client:
                try:
                    resp = await client.get(url)
                    resp.raise_for_status()
                    soup = BeautifulSoup(resp.text, "html.parser")
                    title_tag = soup.find("h1")
                    content_tag = soup.find("div", {"id": "mw-content-text"})
                    if not title_tag or not content_tag:
                        raise ValueError("Не удалось получить заголовок или текст страницы")
                    title = title_tag.text
                    content = content_tag.text
                    links = get_main_section_links(soup)
                    article_obj = await self.crud_article.create(
                        db=db,
                        create_schema=ArticleCreateDB(
                            url=url, 
                            title=title, 
                            content=content, 
                            parent_id=parent_id
                        ),
                    )
                except httpx.TimeoutException:
                    raise httpx.ReadTimeout(f"Timeout for {url}")
                except httpx.HTTPStatusError as ex:
                    raise ValueError(f"Ошибка HTTP {ex.response.status_code} для {url}")
                except Exception as ex:
                    raise RuntimeError(f"Ошибка при парсинге {url}: {str(ex)}") from ex
        self.visited.add(article_obj.url)
        if not links:
            return 0
        total_links = 0
        for link in links[:5]:
            count = await self.parse(db, link, parent_id=article_obj.id, depth=depth + 1, max_depth=max_depth)
            total_links += 1 + count
        return total_links
        

BASE_URL = "https://ru.wikipedia.org"

def get_main_section_links(soup):
    content_div = soup.find("div", {"id": "mw-content-text"})
    if not content_div:
        return []
    parser_output = content_div.find("div", class_="mw-parser-output")
    if not parser_output:
        parser_output = content_div

    stop_sections = {"См. также", "Литература", "Источники", "Примечания"}
    links = []
    in_main = True

    for tag in parser_output.find_all(["p", "ul", "ol", "h2", "h3"]):
        if tag.name in ["h2", "h3"]:
            header_text = tag.get_text(strip=True).lower()
            for stop in stop_sections:
                if stop in header_text:
                    in_main = False
                    break
            if not in_main:
                break
        if in_main:
            for a in tag.find_all("a", href=True):
                href = a["href"]
                if href.startswith("/wiki/") and not href.startswith("/wiki/Special:"):
                    full_url = BASE_URL + href
                    links.append(full_url)
    return links