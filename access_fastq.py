# access TCGA cloud credentials
from os import read
import sevenbridges as sbg
api = sbg.Api(url='https://cgc-api.sbgenomics.com/v2', token='655963abb0424c3ca5bab03e16e0465c')

# [USER INPUT] Set project name and file (f_) index here:
project_name = 'all_fastq'
project_id = api.projects.query(name=project_name)
files = api.files.query(project=project_id)
# download files
for file in files:
    with open(file) as f:
        file.download(path=file.name)
        print(file.name)
'''

project_id = api.projects.query(name=project_name)
file = api.files.query(project=project_id[0], names=[file_name])
#file[0].download(path=file_name)
print(file[0].name)
    '''