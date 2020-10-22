import sqlite3
from sqlite3 import Error
import pandas as pd
import os

#connect to db
dbase = sqlite3.connect("mixcr_out.db")
cursor = dbase.cursor()

#creating a table
cursor.execute('''CREATE TABLE IF NOT EXISTS mixcr_out
    (tcgaId             text,
    receptorType        text,
    cloneId             text, 
    cloneCount          text, 
    cloneFraction       text, 
    targetSequences     text, 
    targetQualities     text, 
    allVHitsWithScore   text, 
    allDHitsWithScore   text, 
    allJHitsWithScore   text, 
    allCHitsWithScore   text, 
    allVAlignments      text, 
    allDAlignments      text, 
    allJAlignments      text, 
    allCAlignments      text, 
    nSeqCDR3            text, 
    minQualCDR3         text, 
    aaSeqCDR3           text, 
    aaSeqFR4            text, 
    refPoints           text)
    ''')

#table fields
fields = ['cloneId', 'cloneCount', 'cloneFraction', 'targetSequences', 'targetQualities', 'allVHitsWithScore', 'allDHitsWithScore',
    'allJHitsWithScore', 'allCHitsWithScore', 'allVAlignments', 'allDAlignments', 'allJAlignments', 'allCAlignments',
    'nSeqCDR3', 'minQualCDR3', 'aaSeqCDR3', 'aaSeqFR4', 'refPoints']

#inserting each file to pandas dataset
import fnmatch
import os

for root, dirnames, filenames in os.walk('.'):
    for filename in fnmatch.filter(filenames, '*.clonotypes.*.txt'):
        filepath = root + "/" + filename
        data = pd.read_csv(filepath, sep='\t', header=0, usecols=fields)
        fileId = filename[:-19]
        receptorType = filename[-7:]
        receptorType = receptorType[:-4]
        data.insert(1, "receptorType", receptorType)
        data.insert(0, "tcgaId", fileId)
        #inserting pandas dataset to db
        data.to_sql('mixcr_out', dbase, if_exists='append', index=False)

#cursor.execute("SELECT * FROM mixcr_out LIMIT 5;").fetchall()

#save changes and close connection to db
dbase.commit()
dbase.close()
os.system("shutdown now -h")
