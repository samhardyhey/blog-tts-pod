TTS
https://news.ycombinator.com/item?id=34211457

## AWS
```
# get IAM users
aws iam list-users

# get policies associated with user
aws iam list-attached-user-policies --user-name sam.hardy

# get full poly iam permissions
aws iam attach-user-policy --user-name sam.hardy --policy-arn arn:aws:iam::aws:policy/AmazonPollyFullAccess
```

```
# configure/create bucket
pip install awscli

aws configure

aws s3api create-bucket --bucket blog-tts-pod --region ap-southeast-2 --create-bucket-configuration LocationConstraint=ap-southeast-2

# rsync
aws s3 sync ./data s3://blog-tts-pod/data --delete

aws s3 sync s3://blog-tts-pod/data ./data --delete
```

## GCP
```
# list existing service account names/emails
gcloud iam service-accounts list

# create a new service account
gcloud iam service-accounts create <account_name> --display-name "<display name>"

# add TTS permissions on the service account
gcloud projects add-iam-policy-binding <project_id> --member serviceAccount:<service_account_name>@<project_id>.iam.gserviceaccount.com --role roles/editor

# create a service account key
gcloud iam service-accounts keys create ~/key.json --iam-account <service_account_name>@<project_id>.iam.gserviceaccount.com

# enable the services on the actual project
gcloud services enable texttospeech.googleapis.com --project=<project_id>
```

## Stream dev
```
uvicorn api:app --reload
```

## Transform
- Ebook parsing, TTS synthesis
- pip install `transform/requirements.txt`
- Adjust main `transform/tts.py` script as needed

## App
- Query/download TTS articles
- Run via `docker-compose up --build -d`