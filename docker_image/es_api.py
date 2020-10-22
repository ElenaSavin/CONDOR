import sys
import urllib3
from elasticsearch import Elasticsearch, RequestsHttpConnection
import json
from datetime import datetime
import os
from requests_aws4auth import AWS4Auth
import boto3
import random as rand

choice = rand.randint(0, 9999)

host = 'search-tcga-refs-pmqkhf65ypmv3tvfewkatun6vu.us-east-1.es.amazonaws.com'
region = 'us-east-1'

service = 'es'
aws_access_key_id= 'AKIA2YI2JIMRDMA3D4X5'
aws_secret_access_key = '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'
#aws_access_key_id = os.environ['aws_access_key_id'],
#aws_secret_access_key = os.environ['aws_secret_access_key']
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(aws_access_key_id, aws_secret_access_key, region, service)

# elasticsearch credentials
port = 443
es = Elasticsearch(hosts = [{"host": host, "port": port}],
    http_auth = awsauth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
)


# returns the name of the next unprocessed file.
def getname(file_uuid):
    res_json = es.search(index="tcga_v2", body={
        "from": 0, "size": 1,
        "query": {
            "term": {
                "id": file_uuid
            }
        }
    })
    print(res_json['hits']['hits'][0]['_source']['filename'])


# returns the file uuid
def getuuid():
    res_json = es.search(index="tcga_v2", body={
    "size" : 1,
    "query": {
        "function_score": {
            "query": { "term": {
      "started_process": False
    } },
            "boost": "5",
            "random_score": {}, 
            "boost_mode":"multiply"
        }
    }})
    print(res_json['hits']['hits'][0]['_source']['id'])


# After processing updates the tag to true.
def updateProcess(fileId):
    es.update(index='tcga_v2',
              id=fileId,
              body={"doc": {"processed": True}}, doc_type="_doc")


# Starting procces on a file, change the tag to true.
def updateStartProcess(fileId):
    es.update(index='tcga_v2',
              id=fileId,
              body={"doc": {"started_process": True}}, doc_type="_doc")


# updating uploading date
def updateUpload(fileId):
    current_datetime = datetime.now()
    es.update(index='tcga_v2',
              id=fileId,
              body={"doc": {"uploaded": current_datetime}}, doc_type="_doc")
              

def GetInfo(fileId):
    res_json = es.search(index="tcga_v2", body={
        "from": choice, "size": 1,
        "query": {
            "term": {
                "id": fileId
            }
        }
    })
    print(res_json)

def updateSize(size, fileId):
  es.update(index='tcga_v2',
              id=fileId,
              body={"doc": {"size_in_bytes": size}}, doc_type="_doc")

'''
receive input from command line
param 1: name of function
param 2: only for updateProcess - the file id
'''
if __name__ == "__main__":
    function = sys.argv[1]
    if function == "getname":
        fileuuid = sys.argv[2]
        getname(fileuuid)
    if function == "updateProcess":
        fileuuid = sys.argv[2]
        updateProcess(fileuuid)
    if function == "getuuid":
        getuuid()
    if function =="GetInfo":
        fileuuid = sys.argv[2]
        GetInfo(fileuuid)
    if function =="updateUpload":
        fileuuid = sys.argv[2]
        updateUpload(fileuuid)
    if function == "updateStartProcess":
        fileuuid = sys.argv[2]
        updateStartProcess(fileuuid)
    if function == "updateSize":
        fileuuid = sys.argv[2]
        size = sys.argv[3]
        updateSize(size, fileuuid)

