from dateutil.parser import parse
import re
import json
import requests
from requests import get
import xml.etree.ElementTree as ET
from xml.dom import minidom

def replace_chunk(content, marker, chunk):
    replacer = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    chunk = "<!-- {} starts -->\n{}\n<!-- {} ends -->".format(marker, chunk, marker)
    return replacer.sub(chunk, content)


def ord(n):
    return str(n)+("th" if 4<=n%100<=20 else {1:"st",2:"nd",3:"rd"}.get(n%10, "th"))


def dtStylish(dt,f):
    return dt.strftime(f).replace("{th}", ord(dt.day))


def pprint(string):
    json_formatted_str = json.dumps(string, indent=2)
    print(json_formatted_str)

def date_to_iso(string):
    dt = parse(string)
    return dt.strftime('%Y-%m-%d')

def get_data(endpoint):
    print(endpoint)
    response = get(endpoint, timeout=20)
    if response.status_code >= 400:
        print(response.status_code)
        print(f"Request failed: { response.text }")
    return response.json()

def replace_chunk(content, marker, chunk):
    replacer = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    chunk = "<!-- {} starts -->\n{}\n<!-- {} ends -->".format(marker, chunk, marker)
    return replacer.sub(chunk, content)

# Replacer function
def replace_chunk(content, marker, chunk):
    replacer = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    chunk = "<!-- {} starts -->\n{}\\n<!-- {} ends -->".format(marker, chunk, marker)
    return replacer.sub(chunk, content)

def fetch_flood_data():
    url = "https://environment.data.gov.uk/flood-monitoring/id/floods"
    params = {
        "county": "Gloucestershire"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def convert_to_rss(data, filename):
        rss = ET.Element("rss", version="2.0")
        channel = ET.SubElement(rss, "channel")
        title = ET.SubElement(channel, "title")
        title.text = "Flood Warnings"
        link = ET.SubElement(channel, "link")
        link.text = "https://environment.data.gov.uk/flood-monitoring/id/floods"
        description = ET.SubElement(channel, "description")
        description.text = "Current flood warnings for Gloucestershire"

        for item in data.get("items", []):
            item_element = ET.SubElement(channel, "item")
            title = ET.SubElement(item_element, "title")
            severity = item.get("severity", "No severity")
            description_text = item.get("description")
            title.text = f"{severity}: {description_text}"
            description = ET.SubElement(item_element, "description")
            description.text = item.get("message", "No message")
            pubDate = ET.SubElement(item_element, "pubDate")
            pubDate.text = item.get("timeRaised", "No date")

        tree = ET.ElementTree(rss)
        tree.write(filename, encoding="utf-8", xml_declaration=True)

        # Pretty-print the XML
        with open(filename, "r") as f:
            xml_content = f.read()
        xml_pretty = minidom.parseString(xml_content).toprettyxml(indent="  ")
        with open(filename, "w") as f:
            f.write(xml_pretty)