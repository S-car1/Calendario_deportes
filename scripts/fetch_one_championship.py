"""Scraping simple (HTML plano server-rendered, sin JS) del calendario de ONE Championship.
Sin API oficial -- se extrae de onefc.com/events/. Probado 2026-10-24.
"""
import requests
from bs4 import BeautifulSoup

from common import BROWSER_HEADERS, write_raw

EVENTS_URL = "https://www.onefc.com/events/"
LOGO_URL = "https://cdn.onefc.com/wp-content/uploads/2020/01/ONE_logo-1024-w.png"


def fetch():
    resp = requests.get(EVENTS_URL, headers=BROWSER_HEADERS, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    events = []
    for card in soup.select("div.simple-post-card.is-event"):
        title_el = card.select_one("a.title")
        datetime_el = card.select_one("div.datetime")
        location_el = card.select_one("div.location")
        if not title_el or not datetime_el:
            continue
        title = title_el.get("title") or title_el.get_text(strip=True)
        href = title_el.get("href", "")
        slug = href.rstrip("/").split("/")[-1]
        timestamp = datetime_el.get("data-timestamp")
        events.append(
            {
                "title": title,
                "slug": slug,
                "url": href,
                "utc_timestamp": int(timestamp) if timestamp else None,
                "location": location_el.get_text(strip=True) if location_el else None,
                "is_fight_night": "fight night" in title.lower(),
            }
        )

    write_raw("one_championship", {"events": events, "logo": LOGO_URL})
    return events


if __name__ == "__main__":
    events = fetch()
    print(f"ONE Championship: {len(events)} eventos encontrados")
