import pandas as pd
from bs4 import BeautifulSoup
from ebooklib import epub


def extract_text_beautifulsoup(html):
    soup = BeautifulSoup(html, "html.parser")
    for script in soup(["script", "style"]):
        script.decompose()
    text = soup.get_text()
    return text.strip()


def extract_chapter_text(ebook_path):
    book = epub.read_epub(ebook_path)
    item_records = []
    for item in book.get_items():
        if "html" in item.get_name():
            # TODO: add file name, issue, author, metadata
            item_record = {
                "item": item,
                "name": item.get_name(),
                "type": item.get_type(),
                "content": item.get_body_content(),
                "parsed_content": extract_text_beautifulsoup(item.get_body_content()),
            }
            item_records.append(item_record)
    return pd.DataFrame(item_records)


if __name__ == "__main__":
    # TODO: glob dir/ingest all
    ebook = "/Users/samhardyhey/Desktop/nautilus_scrape/NautilusIss000.epub"
    df = extract_chapter_text(ebook).pipe(
        lambda x: x[x.parsed_content.apply(lambda y: len(y.split(" ")) > 10)]
    )
    df.to_csv("./data/naut_0.csv", index=False)
    print(df.head())
