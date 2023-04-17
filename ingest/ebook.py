from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup
from ebooklib import epub


def extract_text_beautifulsoup(html):
    soup = BeautifulSoup(html, "html.parser")
    for script in soup(["script", "style"]):
        script.decompose()
    text = soup.get_text()
    return text.strip()


def find_sentence_index_with_keyword(sentences, keywords, find_first=True):
    index = -1  # default to not found
    for i, sentence in enumerate(sentences):
        for keyword in keywords:
            if keyword.lower().strip() in sentence.lower().strip():
                index = i
                if find_first:
                    return index
    return index


def find_author_sentence_index(sentences):
    index = -1  # default to not found
    return next(
        (i for i, sentence in enumerate(sentences) if sentence.lower().strip().startswith("by")),
        index,
    )


def extract_article_metadata(item_record):
    sents = item_record["parsed_content"].split("\n")
    sents = [e for e in sents if len(e.strip()) > 1]
    # collate sentences
    sents = [e.strip() for e in sents if len(e.strip()) > 1]

    # extract segment > query against known segments
    known_segments = [
        "Editor's Note",
        "Numbers",
        "Biology",
        "Culture",
        "Numbers",
        "Ideas",
        "Astronomy",
        "Matter",
        "Neurology",
        "Numbers",
        "Technology",
        "Evolution",
        "Philosophy",
    ]
    segment_sent_index = find_sentence_index_with_keyword(sents, known_segments, find_first=True)
    article_metadata = {"segment": sents[segment_sent_index]}
    # extract author
    author_sent_index = find_author_sentence_index(sents)
    article_metadata["author"] = sents[author_sent_index].split("By ")[1].strip()

    # extract headline/bylines
    candidate_hb_lines = sents[segment_sent_index + 1 : author_sent_index]
    if len(candidate_hb_lines) > 1 and all(len(e.split(" ")) <= 20 for e in candidate_hb_lines):
        article_metadata["headline"] = sents[segment_sent_index + 1]
        article_metadata["byline"] = sents[segment_sent_index + 2]
    else:
        article_metadata["headline"] = sents[segment_sent_index + 1]
        article_metadata["byline"] = None

    # remove image/photo credits from sents
    visual_credit_keywords = ["illus", "pictur", "photo"]
    visual_credit_sent_index = find_sentence_index_with_keyword(sents, visual_credit_keywords, find_first=True)
    sents = sents[visual_credit_sent_index + 1 :] if visual_credit_sent_index != -1 else sents

    # remove author sign off from sents
    author_keywords = [article_metadata["author"]]
    author_sent_index = find_sentence_index_with_keyword(sents, author_keywords, find_first=False)
    sents = sents[:author_sent_index] if author_sent_index != -1 else sents

    article_metadata["sents"] = sents
    item_record.update(article_metadata)

    return item_record


def extract_chapter_text(ebook_path):
    book = epub.read_epub(ebook_path)
    item_records = []
    for item in book.get_items():
        # current_chapter = None
        if "html" in item.get_name():
            # html ~= articles
            parsed_content = extract_text_beautifulsoup(item.get_body_content())
            if not parsed_content or "Chapter" in parsed_content:
                continue

            item_record = {
                "item": item,
                "name": item.get_name(),
                "content": item.get_body_content(),
                "parsed_content": parsed_content,
                "issue_title": book.title,
            }
            try:
                item_record = extract_article_metadata(item_record)
            except Exception:
                print("Failed to extract article metadata for: ", item_record["name"])
            item_records.append(item_record)
    return pd.DataFrame(item_records)


if __name__ == "__main__":
    # TODO: glob dir/ingest all
    nautilus_dir = Path("/Users/samhardyhey/Desktop/nautilus_scrape")
    nautilus_issues = sorted(list(nautilus_dir.glob("*.epub")))

    nautilus_dfs = []
    for issue in nautilus_issues[:20]:
        # 47 issue?
        df = extract_chapter_text(issue).pipe(lambda x: x[x.parsed_content.apply(lambda y: len(y.split(" ")) > 10)])
        nautilus_dfs.append(df)

    df = pd.concat([e for e in nautilus_dfs if not e.empty])
    df.to_csv("./data/naut_all.csv", index=False)
