import sys
from elasticsearch import Elasticsearch
import json
from datetime import datetime

# elasticsearch credentials
host = "search-tcga-refs-pmqkhf65ypmv3tvfewkatun6vu.us-east-1.es.amazonaws.com"
port = 443
es = Elasticsearch([{'host': host, 'port': port, 'use_ssl': True}])


# returns the name of the next unprocessed file.
def get():
    res_json = es.search(index="tcga_v2", body={
        "from": 0, "size": 1,
        "query": {
            "term": {
                "processed": False
            }
        }
    })
    print(res_json['hits']['hits'][0]['_source']['filename'])


# After processing updates the tag to true.
def updateProcess(fileId):
    es.update(index='tcga_v2',
              id=fileId,
              body={"doc": {"processed": True}})


# updating uploading date
def updateUpload(fileId):
    current_datetime = datetime.now()
    es.update(index='tcga_v2',
              id=fileId,
              body={"doc": {"uploaded": current_datetime}})


'''
receive input from command line
param 1: name of function
param 2: only for updateProcess - the file id
'''
if __name__ == "__main__":
    function = sys.argv[1]
    if function == "get":
        get()
    if function == "updateProcess":
        fileId = sys.argv[2]
        updateProcess(fileId)