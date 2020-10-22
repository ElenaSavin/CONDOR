![CONDOR logo](https://github.com/ElenaSavin/CONDOR/blob/master/condor.png?raw=true)

# CONDOR Workflow suggestion

## Pre - processing
1. Download TCGA metadata:
   Enter...
2. create a bucket on S3.
3. create an elasticsearch index using the py script.
   fields:
4. start a EC2 simple vm and create a SQL db on it, containing the output fields and a python script for insert
5. create a cron task, for time hh:02 repeating n times a day on the vm - to sync with S3, start the script for insert, empty the s3
6. create a cron task on your computer starting the vm on hh:00 n times a day.


## Workflow - process.sh  
1. Retrieve file name and uuid using elasticsearch api (es_api.py).
2. Retrieve file size in GB from Seven-Bridges API.
2. Update timestamp and size of this file on elasticsearch and mark as "started process: true"
3. Download the fastq file into the container
4. untar file
5. run mixcr
6. Update timestamp of this file on elasticsearch and mark as "processed: true"
7. upload mixcr output to S3.
8. mark "uploaded: true" on elasticsearch
9. deleate all files from container.


-	Hourly execute cron task in a us-east-1 virtual machine containing a sqlite db:
-	Mount output files to vm.
-	Update db with data from output files.
-	Delete the files from s3 bucket.
-	Turn off the vm.

## Note:
to use a software other than MiXCR, find it on dockerhub and when creating the docker image, use it as base image instead.
! Make sure you have all the needed dependencies !
