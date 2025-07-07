import feedparser
from feedgen.feed import FeedGenerator
import yaml
from datetime import datetime
from datetime import timezone
from dateutil import parser as date_parser
from email.utils import format_datetime

with open("feeds.yaml") as f:
    feed_config = yaml.safe_load(f)

with open("keywords.yaml") as f:
    keywords = yaml.safe_load(f)["keywords"]

fg = FeedGenerator()
fg.title("SH RSS – Erstversuch")
fg.link(href="https://robi1928.github.io/sh_rss/shrss.xml", rel="self")
fg.description("Alles was ich wissen will")
fg.language("de")
fg.lastBuildDate(format_datetime(datetime.now()))

entries = []
for feed in feed_config["feeds"]:
    d = feedparser.parse(feed["url"])
    for entry in d.entries:
        if any(keyword.lower() in entry.title.lower() or keyword.lower() in entry.get("description", "").lower() for keyword in keywords):
            entries.append(entry)

entries.sort(
    key=lambda x: date_parser.parse(
        x.get("published", datetime.now(timezone.utc).isoformat())
    ),
    reverse=True
)

for entry in entries[:50]:
    fe = fg.add_entry()
    fe.title(entry.title)
    fe.link(href=entry.link)
    fe.description(entry.get("description", ""))
    fe.pubDate(entry.get("published", datetime.now().isoformat()))
    fe.guid(entry.link)

fg.rss_file("output/shrss.xml")
