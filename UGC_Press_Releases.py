import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib3

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://www.ugc.gov.in/publication/ugc_pressrelease"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/115.0.0.0 Safari/537.36"
}

# Add headers + bypass SSL check
response = requests.get(url, headers=headers, verify=False)
response.raise_for_status()

soup = BeautifulSoup(response.content, 'html.parser')

base_url = "https://www.ugc.gov.in"
data = []

for link in soup.find_all('a', href=True):
    href = link['href'].strip()
    title = link.get_text(strip=True)

    if href.lower().endswith('.pdf') and title:
        full_link = href if href.startswith("http") else base_url + '/' + href.lstrip('/')
        data.append({"title": title, "link": full_link})

df = pd.DataFrame(data)
df.to_csv("ugc_press_releases.csv", index=False)
print("Saved to ugc_press_releases.csv")
