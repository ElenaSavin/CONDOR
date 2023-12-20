from os import read, system
import requests
import json

#token to secured data 
token_file = "token.txt"

#read the file ids from file
with open("brca.txt", "r") as file:
  for line in file:
    file_id = line.strip() 
    data_endpt = f"https://api.gdc.cancer.gov/slicing/view/{file_id}"
    
    print(f"Downloading file id: {file_id}")
    with open(token_file,"r") as token:
      token_string = str(token.read().strip())

    params = {"gencode": ["BRCA1", "BRCA2"]}

    response = requests.post(data_endpt, 
                            data = json.dumps(params), 
                            headers = {
                              "Content-Type": "application/json",
                              "X-Auth-Token": token_string
                              })

    file_name = f"brca_{file_id}.bam"

    with open(file_name, "wb") as output_file:
      output_file.write(response.content)
        
    system(f"samtools fasta -F 4 brca_{file_id}.bam > brca_{file_id}.fasta")