aws s3 cp s3://tcga-lena . --recursive --exclude "*" --include "*.txt"
aws s3 rm --recursive  s3://tcga-lena//
python3 sql_db.py
rm *.txt
