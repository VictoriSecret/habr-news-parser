import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


def parse_habr_news(pages=2):
    """
    Парсит заголовки и ссылки новостей с Хабра
    pages: количество страниц для парсинга
    """
    news_list = []

    for page in range(1, pages + 1):

        url = f"https://habr.com/ru/news/page{page}/"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        print(f"Парсинг страницы {page}: {url}")


        response = requests.get(url, headers=headers)


        if response.status_code != 200:
            print(f"Ошибка: страница {page} вернула код {response.status_code}")
            continue


        soup = BeautifulSoup(response.text, "html.parser")

        articles = soup.find_all("article", class_="tm-articles-list__item")

        if not articles:
            print(f"На странице {page} не найдено статей. Возможно, изменилась структура сайта.")
            continue

        for article in articles:

            title_tag = article.find("a", class_="tm-title__link")
            if not title_tag:
                continue

            title = title_tag.get_text(strip=True)
            link = "https://habr.com" + title_tag.get("href", "")

            author_tag = article.find("a", class_="tm-user-info__username")
            author = author_tag.get_text(strip=True) if author_tag else "Не указан"

            date_tag = article.find("time")
            date = date_tag.get("datetime", "") if date_tag else "Не указана"


            hubs = []
            hub_tags = article.find_all("a", class_="tm-hubs-list__link")
            for hub in hub_tags:
                hubs.append(hub.get_text(strip=True))

            news_list.append({
                "title": title,
                "link": link,
                "author": author,
                "date": date,
                "hubs": ", ".join(hubs) if hubs else "Без хаба"
            })

        print(f"Страница {page}: собрано {len(articles)} статей")


        time.sleep(1)

    return news_list


if __name__ == "__main__":
    print("Начинаю парсинг новостей Хабра...")

    pages = int(input("Введите количество страниц, которые будем парсить: "))

    news_data = parse_habr_news(pages)

    if news_data:

        df = pd.DataFrame(news_data)
        df.to_csv("habr_news.csv", index=False, encoding="utf-8-sig")

        print(f"\n✅ Готово! Собрано {len(news_data)} новостей.")
        print(f"Файл сохранён: habr_news.csv")

        print("\nПервые 5 новостей:")
        print(df.head().to_string())
    else:
        print("❌ Не удалось собрать новости. Проверьте соединение с интернетом.")