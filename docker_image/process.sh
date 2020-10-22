fileuuid=$(python3 es_api.py getuuid)
filename=$(python3 es_api.py getname $fileuuid)
filesize=$(python3 file_size.py $fileuuid)

python3 es_api.py updateStartProcess $fileuuid
python3 es_api.py updateSize $fileuuid $filesize
python3 download_fastq.py $filename

tar -zxvf *.tar.gz
mkdir $fileuuid

# run mixcr
mixcr analyze shotgun -s hsa --starting-material rna *1.fastq *2.fastq $fileuuid/$fileuuid
rm *.tar.gz

#update in es processed = true
python3 es_api.py updateProcess $fileuuid
#upload the files in the foldet to s3
python3 s3_uploader.py $fileuuid us-east-1 tcga-lena
#update the time of upload to s3
python3 es_api.py updateUpload $fileuuid
rm *.fastq
