from os import read
import os
import sevenbridges as sbg
import sys

# cgc credentials
endpoint_url = os.environ['sb_endpoint_url']
token = os.environ['sb_token']
api = sbg.Api(url=endpoint_url, token=token, advance_access=True)

# project details - expecting your project name
project_name = <name of the project on CGC>
file_name = sys.argv[1]
project_id = api.projects.query(name=project_name)
file = api.files.query(project=project_id[0], names=[file_name])
file[0].download(path=file_name)
