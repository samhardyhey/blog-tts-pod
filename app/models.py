from typing import Optional

from sqlmodel import Field, SQLModel


class Article(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    headline: str
    segment: str
    author: str
    article: str
    item_name: str
    issue_title: str
    byline: str
    issue_number: int
    article_number: int
    object_key: str

    class Config:
        table_config = {"unique": ["headline", "author", "issue_number"]}
