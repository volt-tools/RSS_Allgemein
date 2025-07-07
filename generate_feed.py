import feedparser
from feedgen.feed import FeedGenerator
import yaml
from datetime import datetime
from dateutil import parser as date_parser

# Laden der Feeds und Stichwörter
with open("feeds.yaml") as f:
    feed_config = yaml.safe_load(f)

with open("keywords.yaml") as f:
    keywords = yaml.safe_load(f)["keywords"]

# Feed-Generator vorbereiten
fg = FeedGenerator()
fg.title("SH – Aggregierter Nachrichtenfeed")
fg.link(href="https://<dein-github-name>.github.io/voltsh_rss_feed/output/voltsh.xml", rel="self")
fg.description("Relevante Artikel für Schleswig-Holstein")
fg.language("de")

# Feeds einlesen
entries = []
for feed in feed_config["feeds"]:
    d = feedparser.parse(feed["url"])
    for entry in d.entries:
        if any(keyword.lower() in entry.title.lower() or keyword.lower() in entry.get("description", "").lower() for keyword in keywords):
            entries.append(entry)

# Nach Datum sortieren
entries.sort(key=lambda x: date_parser.parse(x.get("published", datetime.now().isoformat())), reverse=True)

# Artikel zum Feed hinzufügen
for entry in entries[:50]:
    fe = fg.add_entry()
    fe.title(entry.title)
    fe.link(href=entry.link)
    fe.description(entry.get("description", ""))
    fe.pubDate(entry.get("published", datetime.now().isoformat()))
    fe.guid(entry.link)

# Feed speichern
fg.rss_file("output/shrss.xml")
