fileuuid=$(python3 es_api.py getuuid)
echo got file uuid 
filename=$(python3 es_api.py getname $fileuuid)
echo got file name 
filesize=$(python3 file_size.py $fileuuid)
echo got file size
python3 es_api.py updateStartProcess $fileuuid
python3 es_api.py updateSize $fileuuid $filesize
python3 download_fastq.py $filename
echo downloaded file
curl -X POST -H 'Content-type: application/json' --data '{"text":"file ready"}' https://hooks.slack.com/services/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
tar -zxvf *.tar.gz
echo done tar
#dir for output
SECONDS=0
mkdir $fileuuid
# run mixcr
echo runing mixcr
duration=$SECONDS
mixcr analyze shotgun -s hsa --starting-material rna *1.fastq *2.fastq $fileuuid/$fileuuid
rm *.tar.gz
echo removed tar
#update in es processed = true
python3 es_api.py updateProcess $fileuuid
echo updated in es processed
#upload the files in the foldet to s3
python3 s3_uploader.py $fileuuid us-east-1 tcga-lena
echo uploaded files
curl -X POST -H 'Content-type: application/json' --data '{"text":"file uploaded"}' https://hooks.slack.com/services/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
#update the time of upload to s3
python3 es_api.py updateUpload $fileuuid
echo updated in es uploaded
rm *.fastq
echo removed fatq
