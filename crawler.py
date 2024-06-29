import sys
import requests
from bs4 import BeautifulSoup

links = []
files = []


def crawl(source: str, url: str = None):
    url = source if url == None else url

    try:
        req = requests.get(url)
    except:
        return

    links.append(url)
    print(f"\r[!] Page found ({req.status_code}): {url}" + " " * len(source))
    print(f"\rWe found {len(links)} pages from source: '{source}'", end="")

    soup = BeautifulSoup(req.text.lower(), "html.parser")
    file_links = [link.get("href") for link in soup.find_all("a")]
    res = []

    for item in file_links:
        if item in files:
            pass
        elif not item.startswith("https://") and not item.startswith("mailto"):
            files.append(item)
            res.append(f"{source}/{item}")
        else:
            res.append(item)

    for result in res:
        if result not in links and result.startswith(source):
            crawl(result[: result.rfind("/")], result)


def main():
    print(rf"""
 __      __   _       _ _          ___                 _
 \ \    / /__| |__ __(_) |_ ___   / __|_ _ __ ___ __ _| |___ _ _
  \ \/\/ / -_) '_ (_-< |  _/ -_) | (__| '_/ _` \ V  V / / -_) '_|
   \_/\_/\___|_.__/__/_|\__\___|  \___|_| \__,_|\_/\_/|_\___|_|
 Antoine LANDRIEUX (https://github.com/AntoineLandrieux/website-crawler)
""")

    if len(sys.argv) < 2:
        print("USAGE: py crawler.py <link>")
        print("ex   : py crawler.py https://www.galaxy-studio-web.fr")
        return

    crawl(sys.argv[1])


if __name__ == "__main__":
    main()
