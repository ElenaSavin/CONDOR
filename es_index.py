import boto3
import os
import sys
from elasticsearch import Elasticsearch, RequestsHttpConnection, helpers
import csv
import datetime
host = "search-tcga-refs-pmqkhf65ypmv3tvfewkatun6vu.us-east-1.es.amazonaws.com"
port = 443

def insert_fastq_refs_to_es(file_path):
    es = Elasticsearch([{'host': host, 'port': port, 'use_ssl': True}])
    if not es.indices.exists(index="tcga_v2"):
        request_body = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 1
            },
            'mappings': {
                'tcga_v2': {
                    'properties': {
                        'id': {'type': 'text'},
                        'inserted_date': {'format': 'dateOptionalTime', 'type': 'date'},
                        'aligned': {'type': 'date'},
                        'uploaded': {'type': 'date'},
                        'filename': {'type': 'text'},
                        'processed': {'type': 'boolean'}
                    }
                }
            }
        }
        es.indices.create(index='tcga_v2', body=request_body)
    with open(file_path) as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_ALL, delimiter=',')  # base it on delimiter
        next(reader, None)  # skip the headers
        for row in reader:  # each row is a list
            timestamp = datetime.datetime.now()
            print("adding ", row[0])
            itemId = row[0].replace('\'', '')
            document = {
                "id": itemId,
                "filename": row[1].replace('\'', ''),
                "uploaded": timestamp,
                "aligned": timestamp,
                "processed": False
            }
            es.index(index="tcga_v2", doc_type="_doc", id=itemId, body=document)
            print(es.get(index="tcga_v2", doc_type="_doc", id=itemId))


if __name__ == "__main__":
    insert_fastq_refs_to_es('C:/Users/lenak/Documents/bar-illan/masters/tcr to identify tumor/all_fastq_metadata.csv')