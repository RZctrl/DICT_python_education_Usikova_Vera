import requests
import os
import string
from bs4 import BeautifulSoup
from typing import List, Dict

class ArticleParseError(Exception):
    pass

def sanitize_name(title: str) -> str:
    """
    Очищує заголовок статті для використання як ім'я файлу

    Parameters:
        title (str): оригінальний заголовок

    Returns:
        str: рядок з підкресленнями замість пробілів
    """
    translator = str.maketrans('', '', string.punctuation)
    cleaned = title.translate(translator)
    cleaned = cleaned.replace(' ', '_')
    while '__' in cleaned:
        cleaned = cleaned.replace('__', '_')
    return cleaned.strip('_')


def fetch_html(url: str) -> str:
    """
    Виконує запит і повертає текст відповіді

    Parameters:
        url (str): URL-адреса
        accept_language (str): значення заголовка Accept-Language

    Returns:
        str: текст HTML-сторінки

    Raises:
        ArticleParseError: якщо статус не 200
        """
    headers = {'Accept-Language': 'en-US,en;q=0.5'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
    except requests.RequestException as e:
        raise ArticleParseError(f"Request failed: {e}")

    if response.status_code != 200:
        raise ArticleParseError(f"HTTP {response.status_code}")
    return response.text


def get_article(page_url: str, article_type: str) -> List[Dict[str, str]]:
    """
    Збирає всі елементи заданого типу зі сторінки списку Nature

    Parameters:
        page_url (str): URL сторінки зі списком статей
        article_type (str): тип статті

    Returns:
        List[Dict[str, str]]: список словників з ключами title та link

    Raises:
        ArticleParseError: якщо не знайдено статей потрібного типу
    """
    html = fetch_html(page_url)
    soup = BeautifulSoup(html, 'html.parser')

    articles = []
    for article in soup.find_all('article'):
        type_span = article.find('span', {'data-test': 'article.type'})
        if not type_span or type_span.text.strip() != article_type:
            continue

        link_tag = article.find('a', {'data-track-action': 'view article'})
        if not link_tag or not link_tag.get('href'):
            continue

        rel_link = link_tag['href']
        if rel_link.startswith('/'):
            abs_link = "https://www.nature.com" + rel_link
        else:
            abs_link = rel_link

        title = link_tag.text.strip()
        if not title:
            heading = article.find('h3') or article.find('h2')
            if heading:
                title = heading.text.strip()

        if title:
            articles.append({'title': title, 'link': abs_link})

    if not articles:
        raise ArticleParseError(f"No articles of type '{article_type}' found on page")
    return articles


def extract_article(article_url: str) -> str:
    """
    Витягує текст статті

    Parameters:
        article_url (str): URL статті

    Returns:
        str: текст статті

    Raises:
        ArticleParseError: якщо не вдалося знайти тіло статті
    """
    html = fetch_html(article_url)
    soup = BeautifulSoup(html, 'html.parser')

    possible_select = [
        'div.c-article-body',
        'div.article__content',
        'div[class*="article-body"]',
        'div[class*="body"]',
        'main.article-main',
    ]

    for selector in possible_select:
        body_div = soup.select_one(selector)
        if body_div:
            text = body_div.get_text(separator=' ', strip=True)
            if text:
                return text

    meta_desc = soup.find('meta', {'name': 'description'})
    if meta_desc and meta_desc.get('content'):
        return meta_desc['content']

    raise ArticleParseError("No article body found with any known selector")


def save_article(title: str, body: str, output_dir: str) -> str:
    """
    Зберігає статтю у текстовий файл

    Parameters:
        title (str): заголовок статті
        body (str): текст статті
        output_dir (str): шлях до директорії

    Returns:
        str: шлях до створеного файлу
    """
    name = sanitize_name(title)
    filename = f"{name}.txt"
    filepath = os.path.join(output_dir, filename)

    os.makedirs(output_dir, exist_ok=True)

    with open(filepath, 'wb') as f:
        f.write(body.encode('utf-8'))
    return filepath


def main():
    """
    Основна функція для цього етапу, запускає повну версію всієї практичної роботи
    """
    try:
        num_pages = int(input("Enter number of pages: "))
    except ValueError:
        print("Invalid number. Please enter an integer.")
        return

    article_type = input("Enter article type (e.g., News, Nature Briefing): ").strip()
    if not article_type:
        print("Article type cannot be empty.")
        return

    base_url = "https://www.nature.com/nature/articles?sort=PubDate&year=2022&page={}"

    for page_num in range(1, num_pages + 1):
        print(f"\nProcessing page {page_num}...")
        page_url = base_url.format(page_num)
        dir_name = f"Page_{page_num}"
        os.makedirs(dir_name, exist_ok=True)

        try:
            articles = get_article(page_url, article_type)
        except ArticleParseError as e:
            print(f"  Skipping page {page_num}: {e}")
            continue

        save_count = 0
        for art in articles:
            title = art['title']
            link = art['link']
            print(f"  Saving article: {title}")
            try:
                body = extract_article(link)
                save_article(title, body, dir_name)
                save_count += 1
            except ArticleParseError as e:
                print(f"    Failed to save '{title}': {e}")

        print(f"  Page {page_num}: saved {save_count} articles of type '{article_type}'")

    print("\nSaved all articles.")


#Головна функція для запуску програми
if __name__ == "__main__":
    main()