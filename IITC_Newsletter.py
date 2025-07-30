import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib3

# Disable SSL warning (optional)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Target URL
url = "https://iica.nic.in/newsletter.aspx"

# User-Agent header to avoid 403 errors
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/115.0.0.0 Safari/537.36"
}

# Send request
response = requests.get(url, headers=headers, verify=False)
response.raise_for_status()

# Parse HTML
soup = BeautifulSoup(response.content, 'html.parser')

base_url = "https://iica.nic.in"
data = []

# Find all <a> tags that may contain newsletters or PDFs
for link in soup.find_all("a", href=True):
    title = link.get_text(strip=True)
    href = link['href'].strip()

    # Skip empty titles or junk
    if not title or not href:
        continue

    # Fix malformed relative links
    if not href.startswith("http"):
        if not href.startswith("/"):
            href = "/" + href
        full_link = base_url + href
    else:
        full_link = href

    # Optional: filter only for PDFs or newsletters
    if ".pdf" in full_link.lower():
        data.append({"title": title, "link": full_link})

# Convert to DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv("iica_newsletters.csv", index=False)
print("Saved to iica_newsletters.csv")
