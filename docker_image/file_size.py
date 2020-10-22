import os
from os import read
import sevenbridges as sbg
import sys

# cgc credentials
endpoint_url = os.environ['sb_endpoint_url']
token = os.environ['sb_token']
api = sbg.Api(url=endpoint_url, token=token, advance_access=True)

# project details
project_name = 'all_fastq'
fileid = sys.argv[1]
file = api.files.get(id=fileid)

print(file.size)
