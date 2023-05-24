from pathlib import Path

import pandas as pd
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from sqlmodel import Session, SQLModel, create_engine, select

from config import BUCKET_NAME, s3_client
from models import Article
from utils import list_s3_bucket_contents, to_snake_case

app = FastAPI()

# DATABASE_URL = "postgresql://postgres:password@0.0.0.0:5432/db"
DATABASE_URL = "sqlite:///./db.db"
engine = create_engine(DATABASE_URL)


def get_db_session():
    with Session(engine) as session:
        yield session


@app.get("/")
def read_root():
    return RedirectResponse(url="/docs")


@app.get("/articles")
def read_articles(session: Session = Depends(get_db_session)):
    result = session.execute(select(Article).limit(10))
    return result.scalars().all()


@app.get("/articles/{id}")
def read_article(id: int, session: Session = Depends(get_db_session)):
    if article := session.get(Article, id):
        return article
    else:
        raise HTTPException(status_code=404, detail="Article not found")


@app.get("/articles/{id}/stream")
def stream_article(id: int, session: Session = Depends(get_db_session)):
    article = session.get(Article, id)

    # Generate a pre-signed URL for the S3 object with a specific expiration time
    presigned_url = s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET_NAME, "Key": article.object_key},
        ExpiresIn=3600,  # URL expiration time in seconds (adjust as needed)
    )

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    if not article.object_key:
        raise HTTPException(status_code=404, detail="No audio for this article")

    return RedirectResponse(presigned_url)


@app.on_event("startup")
def on_startup():
    with Session(engine) as session:
        SQLModel.metadata.create_all(engine)

    # re-assign S3 keys to each record
    contents = list_s3_bucket_contents(BUCKET_NAME)
    s3_keys = pd.DataFrame({"object_key": [e for e in contents if ".mp3" in e]}).assign(
        join_key=lambda x: x.object_key.apply(lambda y: Path(y).name)
    )
    # ingest all articles
    df = (
        pd.read_csv("../data/naut_all.csv")
        .assign(issue_number=lambda x: x.issue_title.factorize()[0] + 1)
        .assign(article_number=lambda x: x.groupby("issue_number").cumcount() + 1)
        .assign(
            join_key=lambda x: x.apply(
                lambda row: f"{row.article_number}_{to_snake_case(row.headline)}.mp3",
                axis=1,
            )
        )
        .merge(s3_keys, how="inner", on="join_key")
        .drop(columns=["join_key"], axis=1)
    )
    articles = [Article(**e) for e in df.to_dict(orient="records")]

    with Session(engine) as session:
        session.add_all(articles)
        session.commit()
