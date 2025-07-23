from datetime import date, datetime
from urllib.parse import urljoin

from bs4 import BeautifulSoup, Tag


# нужен ли?
class WrongDiapasonDate(Exception):
    pass


class TagClass:
    href = "href"
    a = "a"


class Settings:
    tags = TagClass()
    class_temp = "accordeon-inner__item-title link xls"
    parser = "html.parser"
    url: str = ("https://spimex.com",)


def parse_page_links(
    html: str,
    start_date: date,
    end_date: date,
    settings: Settings,
) -> list[tuple[str, date]]:

    results = []
    links = _get_links(html=html, settings=settings)

    for link in links:
        href = link.get(settings.tags.href, "").split("?")[0]

        if not _is_valid_oil_xls_link(href):
            continue

        try:
            file_date = _extract_date_from_href(href)
            if start_date <= file_date <= end_date:
                full_url = _build_full_url(href, settings.url)
                results.append((full_url, file_date))
            else:
                print(f"Ссылка {href} вне диапазона дат {start_date}-{end_date}")
        except Exception as e:  # вот тут лучше сделать конкретные ошибки
            print(f"Не удалось обработать ссылку {href}: {str(e)}")

    return results


def _get_links(html: str, settings: Settings) -> list[Tag]:
    """Собираем со страницы все ссылки по классу."""
    soup = BeautifulSoup(html, features=settings.parser)
    links = soup.find_all(name=settings.tags.a, class_=settings.class_temp)
    return links


def _is_valid_oil_xls_link(href: str) -> bool:
    """Проверяет, что ссылка соответствует ожидаемому формату."""
    return href.startswith("/upload/reports/oil_xls/oil_xls_") and href.endswith(".xls")


def _extract_date_from_href(href: str) -> date:
    """Извлекает дату из ссылки."""
    date_str = href.split("oil_xls_")[1][:8]
    return datetime.strptime(date_str, "%Y%m%d").date()


def _build_full_url(href: str, url: str) -> str:
    """Собирает полный URL из относительной ссылки."""
    return href if href.startswith("http") else urljoin(url, href)
