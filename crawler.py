
try:

    import sys
    import yaml
    import requests

    from bs4 import BeautifulSoup

except (ImportError, ImportWarning):

    print("ERROR: sys, yaml, requests and bs4 are required.")
    exit(1)


links = []
files = []

with open("files_extensions.yml") as yml:
    files_extensions = yaml.safe_load(yml)


def wtf_is_this_file(file: str) -> str:
    file = file.lower().split(".")[-1]

    for x in files_extensions["files"]:
        for y in files_extensions["files"][x]:
            if y == file:
                return x

    return "File"


def crawl(source: str, url: str = None) -> None:
    url = source if url == None else url

    try:
        req = requests.get(url)
    except:
        return

    links.append(url)
    print(f"\r[!] {wtf_is_this_file(url)} found ({req.status_code}): {url} ")
    print(f"\r{len(links)} files were found", end="", file=sys.stderr)

    res = []
    soup = BeautifulSoup(req.text, "html.parser")

    file_links = [link.get("href") for link in soup.find_all(True)]
    file_links += [link.get("src") for link in soup.find_all(True)]

    for item in file_links:
        if item in files or item == None:
            pass
        elif not item.startswith("https://") and not item.startswith("mailto"):
            files.append(item)
            res.append(f"{source}/{item}")
        else:
            res.append(item)

    for result in res:
        if result.startswith(source) and result not in links:
            crawl(result[: result.rfind("/")], result)


if __name__ == "__main__":
    print(rf"""
 __      __   _       _ _          ___                 _
 \ \    / /__| |__ __(_) |_ ___   / __|_ _ __ ___ __ _| |___ _ _
  \ \/\/ / -_) '_ (_-< |  _/ -_) | (__| '_/ _` \ V  V / / -_) '_|
   \_/\_/\___|_.__/__/_|\__\___|  \___|_| \__,_|\_/\_/|_\___|_|
 Antoine LANDRIEUX (https://github.com/AntoineLandrieux/website-crawler)
""")

    if len(sys.argv) != 2:
        print("USAGE: py crawler.py <link>", file=sys.stderr)
        print("ex   : py crawler.py https://www.galaxy-studio-web.fr", file=sys.stderr)
        exit(1)

    crawl(sys.argv[1])
