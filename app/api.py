import os
from io import StringIO
from pathlib import Path

import pandas as pd
import uvicorn
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import RedirectResponse
from sqlmodel import Session, SQLModel, create_engine, select

from config import BUCKET_NAME, NAUT_ALL_OBJECT_KEY, S3_CLIENT
from models import Article
from utils import list_s3_bucket_contents, to_snake_case

app = FastAPI()

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)


def get_db_session():
    with Session(engine) as session:
        yield session


async def api_key_header(api_key: str = Header(None)):
    if api_key != os.environ.get("API_KEY"):
        raise HTTPException(status_code=403, detail="Could not validate credentials")


@app.get("/")
def read_root():
    return RedirectResponse(url="/docs")


@app.get("/articles")
def read_articles(
    session: Session = Depends(get_db_session), api_key: str = Depends(api_key_header)
):
    result = session.execute(select(Article).limit(10))
    return result.scalars().all()


@app.get("/articles/{id}")
def read_article(
    id: int,
    session: Session = Depends(get_db_session),
    api_key: str = Depends(api_key_header),
):
    if article := session.get(Article, id):
        return article
    else:
        raise HTTPException(status_code=404, detail="Article not found")


@app.get("/articles/{id}/stream")
def stream_article(
    id: int,
    session: Session = Depends(get_db_session),
    api_key: str = Depends(api_key_header),
):
    article = session.get(Article, id)

    # Generate a pre-signed URL for the S3 object with a specific expiration time
    presigned_url = S3_CLIENT.generate_presigned_url(
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
    object_data = S3_CLIENT.get_object(Bucket=BUCKET_NAME, Key=NAUT_ALL_OBJECT_KEY)
    file_data = object_data["Body"].read()

    # Convert the file data to a pandas DataFrame
    data = pd.read_csv(StringIO(file_data.decode("utf-8")))

    df = (
        data.assign(issue_number=lambda x: x.issue_title.factorize()[0] + 1)
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

def list_s3_bucket_contents(bucket_name):
    return [
        item["Key"]
        for item in S3_CLIENT.list_objects_v2(Bucket=bucket_name)["Contents"]
    ]


if __name__ == "__main__":
    port = int(os.getenv("API_PORT"))
    uvicorn.run("api:app", host="0.0.0.0", port=port, reload=True)
