TTS
https://news.ycombinator.com/item?id=34211457

Polly IAM
# get IAM users
aws iam list-users

# get policies associated with user
aws iam list-attached-user-policies --user-name sam.hardy

# get full poly iam permissions
aws iam attach-user-policy --user-name sam.hardy --policy-arn arn:aws:iam::aws:policy/AmazonPollyFullAccess

# bucket stuff
pip install awscli

aws configure

aws s3api create-bucket --bucket blog-tts-pod --region ap-southeast-2 --create-bucket-configuration LocationConstraint=ap-southeast-2

aws s3 sync ./data s3://blog-tts-pod/data

aws s3 sync s3://blog-tts-pod/data ./data
