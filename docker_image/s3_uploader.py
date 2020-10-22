import boto3
import os
import sys
from elasticsearch import Elasticsearch, RequestsHttpConnection, helpers
import csv
import datetime

#expecting credentials in env vars
#invoke from shell using: python s3_uploader.py directory_path s3_bucketname

def upload_files(path, region, bucket):
    session = boto3.Session(
        aws_access_key_id = os.environ['aws_access_key_id'],
        aws_secret_access_key = os.environ['aws_secret_access_key'],
        region_name = region
    )
    s3 = session.resource('s3')
    bucket = s3.Bucket(bucket)
    i=1# file counter
    for subdir, dirs, files in os.walk(path):
        for file in files:
            full_path = os.path.join(subdir, file)
            with open(full_path, 'rb') as data:
                bucket.put_object(Key=full_path[len(path):], Body=data)
                sys.stdout.write("\rfiles uploaded: %s" %i )
                i = i + 1
                sys.stdout.flush()

if __name__ == "__main__":
    upload_files(sys.argv[1], sys.argv[2], sys.argv[3])
