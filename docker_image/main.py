from os import remove, system
import os
import requests
import json
import time
from cdr3 import translate_frames, get_target_sequences

#token to secured data 
token_file = "token.txt"
project = "brca"

def download(data_endpt, token_string, file_id):
  params = {"gencode": ["BRCA1", "BRCA2"]}
  response = requests.post(data_endpt, 
                          data = json.dumps(params), 
                          headers = {
                            "Content-Type": "application/json",
                            "X-Auth-Token": token_string
                            })

  file_name = f"files/{project}_{file_id}.bam"
  
  # Create the "files" directory if it doesn't exist
  os.makedirs("files", exist_ok=True)  # Create directory only if needed

  with open(file_name, "wb") as output_file:
    output_file.write(response.content)
      
  system(f"samtools bam2fq files/{project}_{file_id}.bam > files/{project}_{file_id}.fastq")
  
#read the file ids from file
def match(manifest):
  start_time = time.time()
  print(f"Processing started at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")
  with open(manifest, "r") as file:
    for line in file:
      file_id = line.strip() 
      data_endpt = f"https://api.gdc.cancer.gov/slicing/view/{file_id}"
      
      try: 
        open(f"files/{project}_{file_id}.fastq")
        print(f"File: {file_id} exists, Skipping Download")
        translate_frames(f"files/{project}_{file_id}.fastq")
      except FileNotFoundError:
        print(f"Downloading file id: {file_id}")
        with open(token_file,"r") as token:
          token_string = str(token.read().strip())
        try:
          download(data_endpt, token_string, file_id)
          translate_frames(f"files/{project}_{file_id}.fastq")
        except requests.exceptions.ConnectionError as e:
          if "Temporary failure in name resolution" in str(e):
            print(f"Temporary DNS resolution error. File {file_id} was not downloaded")
            
          # Code to retry the operation (e.g., call the function again)
          else:
            print("A different connection error occurred:", e)
  end_time = time.time()  # Record end time
  print(f"Processing finished at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}")
  print(f"Total processing time: {end_time - start_time:.2f} seconds")
           
        # try:
        #   remove(f"files/{project}_{file_id}.bam")
        # except FileNotFoundError:
        #   print("File not found.")
 
#TODO add logger
if __name__ == "__main__":
    manifest = "brca.txt"  # Replace with your actual FASTQ file name
    match(manifest)
    