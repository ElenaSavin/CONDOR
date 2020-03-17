import sqlite3
from sqlite3 import Error
import pandas as pd
import csv

dbase = sqlite3.connect("try_v1.db")
cursor = dbase.cursor()
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


fields = ['cloneId', 'cloneCount', 'cloneFraction', 'targetSequences', 'targetQualities', 'allVHitsWithScore', 'allDHitsWithScore',
    'allJHitsWithScore', 'allCHitsWithScore', 'allVAlignments', 'allDAlignments', 'allJAlignments', 'allCAlignments',
    'nSeqCDR3', 'minQualCDR3', 'aaSeqCDR3', 'aaSeqFR4', 'refPoints']
files = ['110516_UNC16-SN851_0046_BC037JABXX.6.clonotypes.TRB.txt']
for file in files:
    data = pd.read_csv(file, sep='\t', header=0, usecols=fields)
    fileId = file[:-19]
    receptorType = file[-7:]
    receptorType = receptorType[:-4]
    data.insert(1, "receptorType", receptorType)
    data.insert(0, "id", fileId)

data.to_sql('mixcr_out', dbase, if_exists='append', index=False)
cursor.execute("SELECT * FROM mixcr_out LIMIT 5;").fetchall()
#save and close db
dbase.commit()
dbase.close()
