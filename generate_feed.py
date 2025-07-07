import feedparser
from feedgen.feed import FeedGenerator
import yaml
from datetime import datetime, timezone
from dateutil import parser as date_parser
from email.utils import format_datetime

with open("feeds.yaml") as f:
    feed_config = yaml.safe_load(f)

with open("keywords.yaml") as f:
    keywords = yaml.safe_load(f)["keywords"]

fg = FeedGenerator()
fg.title("Volt SH – Aggregierter Nachrichtenfeed")
fg.link(href="https://robi1928.github.io/sh_rss/shrss.xml", rel="self")
fg.description("Relevante Artikel für Volt Schleswig-Holstein")
fg.language("de")
fg.lastBuildDate(format_datetime(datetime.now(timezone.utc)))

entries = []
for feed in feed_config["feeds"]:
    d = feedparser.parse(feed["url"])
    for entry in d.entries:
        title = entry.get("title", "")
        description = entry.get("description", "")

        if any(keyword.lower() in title.lower() or keyword.lower() in description.lower() for keyword in keywords):
            entries.append(entry)

def parse_date_safe(entry):
    try:
        dt = date_parser.parse(entry.get("published", ""))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        return datetime.now(timezone.utc)

entries.sort(key=parse_date_safe, reverse=True)

for entry in entries[:50]:
    fe = fg.add_entry()
    fe.title(entry.get("title", "Kein Titel"))
    fe.link(href=entry.get("link", "#"))
    fe.description(entry.get("description", ""))
    fe.guid(entry.get("link", "#"))

    pub_date = parse_date_safe(entry)
    fe.pubDate(pub_date)

fg.rss_file("docs/shrss.xml")
