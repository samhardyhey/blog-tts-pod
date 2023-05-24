import pandas as pd
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from sqlmodel import Session, SQLModel, create_engine, select

from models import Article

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
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    if not article.audio_url:
        raise HTTPException(status_code=404, detail="No audio for this article")

    return RedirectResponse(article.audio_url)


@app.on_event("startup")
def on_startup():
    with Session(engine) as session:
        SQLModel.metadata.create_all(engine)

    # ingest all articles
    df = (
        pd.read_csv("../data/naut_all.csv")
        .assign(issue_number=lambda x: x.issue_title.factorize()[0] + 1)
        .assign(article_number=lambda x: x.groupby("issue_number").cumcount() + 1)
        .assign(audio_url="hello_world")
    )
    articles = [Article(**e) for e in df.to_dict(orient="records")]

    with Session(engine) as session:
        session.add_all(articles)
        session.commit()
