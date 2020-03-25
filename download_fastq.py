# access TCGA cloud credentials
from os import read
import sevenbridges as sbg
import sys

# cgc credentials
api = sbg.Api(url='https://cgc-api.sbgenomics.com/v2', token='655963abb0424c3ca5bab03e16e0465c')

# project details
project_name = 'all_fastq'
file_name = sys.argv[1]
project_id = api.projects.query(name=project_name)
file = api.files.query(project=project_id[0], names=[file_name])
file[0].download(path=file_name)
