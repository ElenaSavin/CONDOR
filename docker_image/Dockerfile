FROM milaboratory/mixcr:latest
MAINTAINER Elena Savin

#add all the scripts
ADD . ./
ENTRYPOINT ["/bin/bash", "-c"]
RUN apt-get update && apt install -y python3
RUN apt update && apt install python3-pip -y

#install all libraries the file- the file is in github
RUN pip3 install -r ./requirements.txt

#evironment variables
ENV aws_access_key_id=<access_key_id>
ENV aws_secret_access_key=<secret_access_key>
ENV sb_token= <seven_bridges_token>
ENV sb_endpoint_url= <seven_bridges_url>

# start process
CMD ["./process.sh"]
