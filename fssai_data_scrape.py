import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv

BASE_URL = "https://fssai.gov.in/notifications.php?notification=draft-notification"

def fetch_page(url):
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.text

def parse_notifications(html):
    soup = BeautifulSoup(html, "html.parser")
    items = []
    for li in soup.select("div[class*='list'] li, li"):
        a = li.find("a", href=True)
        if a:
            title = a.get_text(strip=True)
            link = urljoin(BASE_URL, a["href"])
            items.append({"Title": title, "Link": link})
    return items

def find_next_page(html):
    soup = BeautifulSoup(html, "html.parser")
    nxt = soup.select_one("a[rel='next']")
    return urljoin(BASE_URL, nxt["href"]) if nxt else None

def scrape_all():
    url = BASE_URL
    all_items = []
    while url:
        print("Scraping:", url)
        html = fetch_page(url)
        items = parse_notifications(html)
        all_items.extend(items)
        url = find_next_page(html)
    return all_items

def save_to_csv(data, filename):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Title", "Link"])
        writer.writeheader()
        writer.writerows(data)
    print(f"Saved {len(data)} records to {filename}")

if __name__ == "__main__":
    results = scrape_all()
    save_to_csv(results, "fssai_draft_notifications.csv")
