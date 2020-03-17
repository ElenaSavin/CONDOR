#this script has access to tcga fastq files.
#   :param conn: none
#  :return: the tar fastq file
# """

file_name = $(python3 workflow_tcga.py)
file_id=$(tar -zxvf $file)
file_id=$(echo "$file_id" | cut -f1 -d' '| head -1)
file_id=${file_id::-8}
echo $file_id

#dir for output
mkdir $file_id

#tarball
tar xvzf $file_name

#star
docker run -it --rm \
    -m 4g \
    -v ~/PycharmProjects/untitled/:/work \
    genome/docker-star \
    STAR --runThreadN 16 \
    --genomeDir /home/lena/PycharmProjects/starIndex/ \
    --readFilesIn ${file_id}?1.fastq ${file_id}?2.fastq \
    --outFileNamePrefix $file_id --outReadsUnmapped Fastx --outFilterScoreMinOverLread 0.96 --outFilterMatchNminOverLread 0.96;

#mixcr
docker run -it --rm \
    -m 4g \
    -v ~/PycharmProjects/untitled/:/work \
    milaboratory/mixcr \
    mixcr analyze shotgun -s hsa --starting-material rna ${file_id}Unmapped.out.mate1 ${file_id}Unmapped.out.mate2 $file_id/$file_id;

#upload results to s3
python3 upload_drive_api.py $file_id/$file_id