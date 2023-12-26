from os import read, system
import requests
import json
from cdr3 import translate_frames

#token to secured data 
token_file = "token.txt"

#read the file ids from file
def download(manifest):
  with open(manifest, "r") as file:
    for line in file:
      file_id = line.strip() 
      data_endpt = f"https://api.gdc.cancer.gov/slicing/view/{file_id}"
      try: 
        open(f"brca_{file_id}.fastq")
        print(f"File: {file_id} exists, Skipping Download")
      except FileNotFoundError:
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
            
        system(f"samtools bam2fq brca_{file_id}.bam > brca_{file_id}.fastq")      
      translate_frames(f"brca_{file_id}.fastq")   

if __name__ == "__main__":
    manifest = "brca.txt"  # Replace with your actual FASTQ file name
    download(manifest)