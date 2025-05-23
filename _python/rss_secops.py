# importing modules
import pathlib
import feedparser
import helper
from datetime import datetime, timedelta

URL_1 = "https://www.cisa.gov/uscert/ncas/alerts.xml"
URL_2 = "https://feeds.feedburner.com/OfficeOfInadequateSecurity"
URL_3 = "http://www.darkreading.com/rss/all.xml"
URL_4 = "http://seclists.org/rss/fulldisclosure.rss"
URL_5 = "http://blogs.technet.com/msrc/rss.xml"
URL_6 = "https://www.ncsc.gov.uk/feeds/guidance.xml"
URL_7 = "https://www.ncsc.gov.uk/api/1/services/v1/report-rss-feed.xml"
URL_8 = "http://blogs.technet.com/mmpc/rss.xml"
URL_9 = "http://seclists.org/rss/bugtraq.rss"
URL_10 = "https://feeds.feedburner.com/HaveIBeenPwnedLatestBreaches"
URL_11 = "http://www.netresec.com/rss.ashx"
URL_12 = "https://krebsonsecurity.com/feed/"
URL_13 = "https://grahamcluley.com/feed/"
URL_14 = "https://feeds.feedburner.com/TroyHunt"
URL_15 = "https://feeds.feedburner.com/TheHackersNews"
URL_16 = "https://feeds.feedburner.com/securityweek"
URL_17 = "https://www.theregister.com/security/headlines.atom"
URL_18 = "https://www.theregister.com/software/headlines.atom"
URL_19 = "https://www.bleepingcomputer.com/feed/"
URL_20 = "https://scotthelme.co.uk/rss/"
URL_21 = "https://blog.cloudflare.com/"
URL_22 = "https://wwww.politico.com/rss/morningcybersecruity.xml"
URL_23 = "https://www.itgovernance.co.uk/blog/feed"
URL_24 = "https://www.githubstatus.com/history.rss"



# processing
if __name__ == "__main__":
    try:
        root = pathlib.Path(__file__).parent.parent.resolve()

        urls = [URL_1, URL_2, URL_3, URL_4, URL_5, URL_6, URL_7, URL_8, URL_9, URL_10,
                URL_11, URL_12, URL_13, URL_14, URL_15, URL_16, URL_17, URL_18, URL_19,
                URL_20, URL_21, URL_22, URL_23, URL_24]
        all_items = []

        for URL in urls:
            feed = feedparser.parse(URL)
            all_items.extend(feed["items"][:25])

        # Use published_parsed or updated_parsed for sorting/filtering
        for item in all_items:
            item["title"] = item["title"].replace("|", " - ").replace(">", " - ")
            if "published_parsed" in item and item["published_parsed"] is not None:
                item["_sort_date"] = item["published_parsed"]
            elif "updated_parsed" in item and item["updated_parsed"] is not None:
                item["_sort_date"] = item["updated_parsed"]
            else:
                item["_sort_date"] = None

        # Filter out items without a valid date
        all_items = [item for item in all_items if item["_sort_date"] is not None]
        all_items.sort(key=lambda x: x["_sort_date"], reverse=True)

        cutoff_date = datetime.now() - timedelta(days=30)
        all_items = [item for item in all_items if datetime(*item["_sort_date"][:6]) > cutoff_date]

        string = ""
        for item in all_items:
            # Use helper.time_ago for display only
            item_time = helper.time_ago(item["_sort_date"])
            string += f"- {item['title']} ([{item_time}]({item['link']}))\n"


        f = root / "secops.md"
        m = f.open().read()
        c = helper.replace_chunk(m, "news_marker", string)
        f.open("w").write(c)
        print(len(all_items),"News completed")

    except FileNotFoundError:
        print("File does not exist, unable to proceed")
