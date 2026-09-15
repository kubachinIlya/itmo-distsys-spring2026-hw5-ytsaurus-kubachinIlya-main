import requests
from bs4 import BeautifulSoup
import time
import re

# Страница альбома
ALBUM_URL = "https://genius.com/albums/Zamay-and-slava-kpss/Antihypetrain"

# Заголовки, чтобы Genius не блокировал как бота
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def get_track_links(album_url):
    """Собирает ссылки на все треки со страницы альбома."""
    resp = requests.get(album_url, headers=HEADERS)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    
    # Genius хранит ссылки на треки в тегах <a> с классом, содержащим "u-display_block" или похожим
    # Но ищем все ссылки, ведущие на страницы с текстом
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        # Ссылки на треки имеют вид /Zamay-and-slava-kpss-...-lyrics
        if "/Zamay-and-slava-kpss" in href and "lyrics" in href:
            full_url = href if href.startswith("http") else "https://genius.com" + href
            if full_url not in links:
                links.append(full_url)
    
    return links

def get_lyrics(track_url):
    """Извлекает текст трека со страницы."""
    resp = requests.get(track_url, headers=HEADERS)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    
    # Genius хранит текст в div с атрибутом data-lyrics-container="true"
    containers = soup.find_all("div", attrs={"data-lyrics-container": "true"})
    if not containers:
        # fallback: старый формат
        containers = soup.find_all("div", class_=re.compile("lyrics"))
    
    if not containers:
        return None
    
    # Склеиваем все части и чистим от HTML-тегов
    text_parts = []
    for c in containers:
        # Заменяем <br> на перенос строки
        for br in c.find_all("br"):
            br.replace_with("\n")
        text_parts.append(c.get_text())
    
    lyrics = "\n".join(text_parts)
    # Убираем квадратные скобки с секциями ([Chorus], [Verse] и т.п.) — по желанию
    lyrics = re.sub(r"\[.*?\]", "", lyrics)
    # Убираем лишние пустые строки
    lyrics = "\n".join(line for line in lyrics.splitlines() if line.strip())
    
    return lyrics.strip()

def main():
    print(f"Собираем ссылки со страницы: {ALBUM_URL}")
    links = get_track_links(ALBUM_URL)
    print(f"Найдено треков: {len(links)}")
    
    all_lyrics = []
    for i, url in enumerate(links, 1):
        print(f"[{i}/{len(links)}] {url}")
        try:
            lyrics = get_lyrics(url)
            if lyrics:
                # Заголовок трека из URL
                title = url.split("/")[-1].replace("-lyrics", "").replace("-", " ")
                all_lyrics.append(f"### {title}\n\n{lyrics}\n")
            else:
                print(f"Не удалось извлечь текст")
        except Exception as e:
            print(f"Ошибка: {e}")
        time.sleep(1)  # пауза, чтобы не забанили
    
    output_file = "antihype_train_lyrics.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n\n".join(all_lyrics))
    
    print(f"\nГотово! Сохранено в {output_file}")

if __name__ == "__main__":
    main()