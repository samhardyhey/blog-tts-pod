0. nautilus subscription
- chrome downloader

1. parse ebook
    - extract chapters
    - format chapter meta-data
        - title, author
            - maybe use spacy? > nervous when scaling out across other 90 issues
            - consider using langchain extraction
    - consolidated

1.1 nautilus specific structures
- native ebook sents structure
- authorship/attribution

2. summarize/extract?
- short summaries?
- "threaded" summaries across all articles?
- skip for now?

3. text-to-speech
3.1 Cocqui TTS
- well regarded - Yoshua Bengio?
- https://github.com/coqui-ai/TTS
- 196 words > 55 seconds processing > 1.5 minutes
    - probably going to need some acceleration > runpod serverless GPUs?

3.2 Voice cloning
- Dr. Karl? > find some audio

4. access?
    - notional stream API?

5. deployment
    - formalize ingestion pipeline
        - DB for finalized articles
        - S3 for audio
    - API
        - FastAPI stream
    - query streams