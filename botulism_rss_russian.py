import feedparser
import pandas as pd
from datetime import datetime, timedelta
from googletrans import Translator

# Define the search and RSS feed
rss_url = "https://news.google.com/rss/search?q=ботулизм&hl=ru&gl=RU&ceid=RU:ru"

# Load the feed
feed = feedparser.parse(rss_url)

# Translate and filter
translator = Translator()
cutoff_date = datetime.now() - timedelta(days=730)

entries = []
for entry in feed.entries:
    published = datetime(*entry.published_parsed[:6])
    if published >= cutoff_date:
        translated_title = translator.translate(entry.title, src='ru', dest='en').text
        translated_summary = translator.translate(entry.summary, src='ru', dest='en').text
        entries.append({
            "Date": published.strftime("%Y-%m-%d"),
            "Title (RU)": entry.title,
            "Title (EN)": translated_title,
            "Summary (EN)": translated_summary,
            "Link": entry.link
        })

# Convert to DataFrame and display
df = pd.DataFrame(entries)
print(df)
