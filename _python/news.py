# importing modules
import pathlib
import feedparser
import helper
from datetime import datetime, timedelta

URL_1 ="https://www.insurancebusinessmag.com/uk/rss/"
URL_2 ="https://ifamagazine.com/category/insurance-and-protection/feed/"
URL_3 ="https://fintech.global/category/insurtech/feed/"  # REMOVE (invalid)
URL_4 ="https://www.postonline.co.uk/feeds/rss/"
URL_5 ="https://www.reinsurancene.ws/feed/"
URL_6 ="https://www.insurancejournal.com/rss/"
URL_7 ="https://www.dig-in.com/feed.rss"
URL_8 ="https://insurance-edge.net/feed/"
URL_9 ="https://thefintechtimes.com/category/fintech/insurtech/feed/"
URL_10 ="https://insurtechinsights.com/feed/"
URL_11 ="https://www.fca.org.uk/news/rss.xml"

def time_ago(published_parsed):
            published_date = datetime(*published_parsed[:6])
            now = datetime.now()
            diff = now - published_date
            if diff.days > 0:
                return f"{diff.days} days ago"
            elif diff.seconds > 3600:
                return f"{diff.seconds // 3600} hours ago"
            elif diff.seconds > 60:
                return f"{diff.seconds // 60} minutes ago"
            else:
                return "just now"



# processing
if __name__ == "__main__":
    try:
        root = pathlib.Path(__file__).parent.parent.resolve()

        urls = [URL_1, URL_2, URL_4, URL_5, URL_6, URL_7, URL_8, URL_9, URL_10, URL_11]
        all_items = []

        for URL in urls:
            feed = feedparser.parse(URL)
            all_items.extend(feed["items"][:25])

        # Filter out items without 'published_parsed' or where it is None
        all_items = [item for item in all_items if 'published_parsed' in item and item['published_parsed'] is not None]
        all_items.sort(key=lambda x: x["published_parsed"], reverse=True)

        for item in all_items:
            item["published"] = time_ago(item["published_parsed"])

        cutoff_date = datetime.now() - timedelta(days=10)
        all_items = [item for item in all_items if datetime(*item["published_parsed"][:6]) > cutoff_date]

        string = ""
        for item in all_items:
            string += f"- {item['title']} ([{item['published']}]({item['link']}))\n"

        f = root / "index.md"
        m = f.open().read()
        c = helper.replace_chunk(m, "news_marker", string)
        f.open("w").write(c)
        print("News completed")

    except FileNotFoundError:
        print("File does not exist, unable to proceed")