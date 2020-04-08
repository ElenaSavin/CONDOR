FROM milaboratory/mixcr:latest
MAINTAINER Lena Savin
#set dir
#add all the scripts
ADD . ./
RUN apt-get update && apt install -y python3
RUN apt update && apt install python3-pip -y

#install all libraries the file- the file is in github
RUN pip3 install -r ./requirements.txt

#evironment variables
ENV aws_access_key_id=AKIA2YI2JIMRDMA3D4X5
ENV aws_secret_access_key=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
Env url_tcga_enpoint=https://cgc-api.sbgenomics.com/v2
ENV tocken_tcga=655963abb0424c3ca5bab03e16e0465c

CMD ["chmod", "+x", "process.sh"]
RUN ./process.sh
