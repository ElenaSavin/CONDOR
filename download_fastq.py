# access TCGA cloud credentials
from os import read
import sevenbridges as sbg
import sys

# cgc credentials
url = os.environ['url_tcga_enpoint'],
token = os.environ['token_tcga']
api = sbg.Api(url, token)

# project details
project_name = 'all_fastq'
file_name = sys.argv[1]
project_id = api.projects.query(name=project_name)
file = api.files.query(project=project_id[0], names=[file_name])
file[0].download(path=file_name)
