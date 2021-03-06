![CONDOR logo](https://github.com/ElenaSavin/CONDOR/blob/master/condor.png)

# CONDOR - Cloud Operations Niche, Docker Orchestration for Research 
# Workflow suggestion
### Note:
to use a software other than MiXCR, find it on dockerhub and when creating the docker image, use it as a base image instead.

! Make sure you have all the needed dependencies !


## Pre - processing
1. Start a project on the CGC and add all the files needed to the project. (https://docs.cancergenomicscloud.org/docs/quickstart)
2. Download the metadata manifest file from your project.
3. Create a bucket on S3.
4. Start a ElasticSearch service on AWS.
4. Create an elasticsearch index using the es_index.py script. (https://elasticsearch-py.readthedocs.io/en/master/api.html)
   fields: uuid: item uuid,
           filename": full file name,
           started_process: True/False,
           start_time: timestamp,
           processed: True/False,
           uploaded: True/False,
           done_time: timestamp
5. Start a EC2 simple vm and create a SQL database on it, containing the output fields and a python script for insert (sql_db.py)
6. Create a cron task, for time hh:02 repeating n times a day on the vm - to sync with S3, start the script for insert, empty the s3 - the script (s3_sync_delete.sh)
7. Create a cron task on your computer starting the vm on hh:00 n times a day.
* Make sure you have AWS CLI and eksctl installed on your machine.

## Cluster configuration:
1. Create a new kubernetes cluster (https://eksctl.io/usage/creating-and-managing-clusters/)

```
eksctl create cluster --name myCluster --without-nodegroup --zones=us-east-1a,us-east-1b,us-east-1d
```
2. Create a nodegroup with only spot nodes - spotnodes.yaml.
   (https://eksworkshop.com/beginner/150_spotworkers/workers) 


## Workflow - process.sh  
1. Retrieve file name and uuid using elasticsearch api (es_api.py).
2. Retrieve file size in GB from Seven-Bridges API (file_size.py).
2. Update timestamp and size of this file on elasticsearch and mark as "started process: true" (es_api.py).
3. Download the fastq file into the container (download_fastq.py)
4. Untar file 

```
tar -xvzf <file_name>.tar.gz
```

5. Run mixcr (https://mixcr.readthedocs.io/en/master/quickstart.html)
```
mixcr analyze shotgun -s hsa --starting-material rna *1.fastq *2.fastq $fileuuid/$fileuuid
```

6. Update timestamp of this file on elasticsearch and mark as "processed: true" (es_api.py)
7. Upload mixcr output to S3. (s3_uploader.py).
8. Mark "uploaded: true" on elasticsearch (es_api.py).
9. Deleate all files from container.


## Hourly execute cron task in a us-east-1 virtual machine containing a sqlite db:
script - s3_sync_delete.sh and sql_db.py
1. Mount output files to vm.
2. Update db with data from output files.
3. Delete the files from s3 bucket.
4. Turn off the vm.
