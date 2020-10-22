![CONDOR logo](https://github.com/ElenaSavin/CONDOR/blob/master/condor.png =200x100)

# CONDOR Workflow suggestion
### Note:
to use a software other than MiXCR, find it on dockerhub and when creating the docker image, use it as a base image instead.

! Make sure you have all the needed dependencies !


## Pre - processing
1. Start a project on the CGC and add all the files needed to the project.
2. Download TCGA metadata from the project.
3. Create a bucket on S3.
4. Start a ElasticSearch service on AWS.
4. Create an elasticsearch index using the es_index.py script.
   fields: uuid: item uuid,
           filename": full file name,
           started_process: True/False,
           start_time: timestamp,
           processed: True/False,
           uploaded: True/False,
           done_time: timestamp
5. Start a EC2 simple vm and create a SQL db on it, containing the output fields and a python script for insert
6. Create a cron task, for time hh:02 repeating n times a day on the vm - to sync with S3, start the script for insert, empty the s3
7. Create a cron task on your computer starting the vm on hh:00 n times a day.


## Workflow - process.sh  
1. Retrieve file name and uuid using elasticsearch api (es_api.py).
2. Retrieve file size in GB from Seven-Bridges API.
2. Update timestamp and size of this file on elasticsearch and mark as "started process: true"
3. Download the fastq file into the container
4. Untar file
5. Run mixcr
6. Update timestamp of this file on elasticsearch and mark as "processed: true"
7. Upload mixcr output to S3.
8. Mark "uploaded: true" on elasticsearch
9. Deleate all files from container.


### Hourly execute cron task in a us-east-1 virtual machine containing a sqlite db:
-	Mount output files to vm.
-	Update db with data from output files.
-	Delete the files from s3 bucket.
-	Turn off the vm.


