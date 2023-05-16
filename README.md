Problem/use-case
- suffering from info overload, hard to keep head above flow of information
- finding that I'm not having alot of time to read text > but do haev lots of free time to listen to podcasts/audio
- take text publications from high quality publishers > TTS > listen as audio/podcast

0. nautilus subscription
- chrome downloader?
    - can't quite remember: https://www.downthemall.net/
    - https://chrome.google.com/webstore/detail/simple-mass-downloader/abdkkegmcbiomijcbdaodaflgehfffed
- download 96 copies of nautilus, a long-form, science a-current afair style publication, similar to Quanta

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

3.2 GPU inference
- canvas a few options
https://www.banana.dev/serverless-gpu-inference
https://www.runpod.io/console/pods

- clone repo > SCP data > TTS > SCP back
- formalize pipeline/CI/CD as an extension

3.2 Voice cloning
- Dr. Karl? > find some audio, pull down
    - how much audio?
    - experiments? > num minutes, hours, try a few different voices > aus personalities

4. streaming API?
    - notional stream API? > FastAPI sketch
    - docker compose > postgres, minio, API
    - docker containers

Polly IAM
# get IAM users
aws iam list-users

# get policies associated with user
aws iam list-attached-user-policies --user-name sam.hardy

# get full poly iam permissions
aws iam attach-user-policy --user-name sam.hardy --policy-arn arn:aws:iam::aws:policy/AmazonPollyFullAccess

