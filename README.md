1. parse ebook
    - extract chapters
    - format chapter meta-data
        - title, author
        - summarization?
    - consolidated

2. summarize/extract?
    - short summaries?
    - "threaded" summaries across all articles?

3. text-to-speech
    - well regarded:
        - https://github.com/coqui-ai/TTS
            - tts --text "Text for TTS" --out_path speech.wav
            -
4. consumption?
    - stream API?
    - transport control?

5. deployment
    - formalize ingestion pipeline
        - DB for finalized articles
        - S3 for audio
    - API
        - FastAPI stream