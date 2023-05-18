import codecs
from pathlib import Path

import ftfy
import pandas as pd
from bs4 import BeautifulSoup
from ebooklib import epub

from utils import logger


def decode_soup_element(element):
    text_raw = element.get_text()
    decoded = codecs.decode(text_raw, "unicode_escape")
    return ftfy.fix_text(decoded).strip()


def parse_article_record(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    h1s = [decode_soup_element(e) for e in soup.find_all("h1")]
    h2s = [decode_soup_element(e) for e in soup.find_all("h2")]
    h3s = [decode_soup_element(e) for e in soup.find_all("h3")]
    h4s = [decode_soup_element(e) for e in soup.find_all("h4")]
    ps = [decode_soup_element(e) for e in soup.find_all("p")]

    article_record = {}
    if any("editor" in e.lower() for e in h1s):
        # editor segments
        article_record["headline"] = h2s[0]
        article_record["segment"] = h1s[0]
        article_record["author"] = h4s[1]
    else:
        article_record["headline"] = h2s[0] if h2s else None
        if h3s and "byline" not in article_record:
            article_record["byline"] = h3s[0]
        else:
            article_record["byline"] = None

        if h4s:
            article_record["segment"] = h4s[0]
            article_record["author"] = h4s[1] if len(h4s) > 1 else None

    article_record["article"] = "\n".join([e for e in ps if len(e) > 1])
    return article_record


def parse_issue_articles(ebook_path):
    book = epub.read_epub(ebook_path)
    article_records = []
    for item in book.get_items():
        # current_chapter = None
        if Path(item.get_name()).suffix == ".html" and "chap" not in item.get_name():
            logger.info(f"Processing {item.get_name()}")
            article_record = parse_article_record(item.get_body_content())

            # add issue metadata
            article_record.update({"item_name": item.get_name(), "issue_title": book.title})
            article_records.append(article_record)
    return pd.DataFrame(article_records)


if __name__ == "__main__":
    nautilus_dir = Path("./data/nautilus_epub/")
    nautilus_issues = sorted(list(nautilus_dir.glob("*.epub")))

    # parse articles for each issue
    nautilus_dfs = []
    for issue in nautilus_issues:
        df = parse_issue_articles(issue)
        nautilus_dfs.append(df)

    df = pd.concat([e for e in nautilus_dfs if not e.empty])
    logger.info(f"Successfully extracted {len(df)} articles")

    # remove mis-parsed articles (~2)
    df = (
        df.pipe(lambda x: x[~x.headline.isna()])
        .pipe(lambda x: x[~x.segment.isna()])
        .pipe(lambda x: x[~x.author.isna()])
        .pipe(lambda x: x[~x.article.isna()])
        .pipe(lambda x: x[~x.item_name.isna()])
        .pipe(lambda x: x[~x.issue_title.isna()])
    )
    logger.info(f"Reducing to {len(df)} articles")
    df.to_csv("./data/naut_all.csv", index=False)
