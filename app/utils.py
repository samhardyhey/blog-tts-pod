import re

from config import S3_CLIENT


def list_s3_bucket_contents(bucket_name):
    return [
        item["Key"]
        for item in S3_CLIENT.list_objects_v2(Bucket=bucket_name)["Contents"]
    ]


def to_snake_case(s):
    """
    Converts a string to snake case.
    """
    # Replace all non-alphanumeric characters with underscores
    s = re.sub(r"\W", "_", s)

    # Split the string into words
    words = s.split()

    return "_".join(re.sub(r"__", "_", word.lower()) for word in words if word != "_")
