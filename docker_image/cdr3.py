import Bio.SeqIO 
import csv
import multiprocessing
import logging

def get_target_sequences(seq_file):
  hashed_sequences = {}
  base = 256
  mod = 2**64
# Open the CSV file in read mode
  with open(seq_file, "r") as csvfile:
    # Create a CSV reader object
    csv_reader = csv.reader(csvfile)

    # Read the header row
    header = next(csv_reader)

    for row in csv_reader:
      sequence = row[0]
      hashed_sequences[sequence] = initial_hash(sequence, base, mod)  # Use hashed sequence as key

  return(hashed_sequences)

def translate_frames(file_id):
  print(f"translating file id: {file_id}")
  target_hashes = get_target_sequences("top_1000.csv")
  
  for read in Bio.SeqIO.parse(file_id, "fastq"):
    
    sequence = str(read.seq.complement())
    #sequence = str(read.seq)
    for frame in range(3):
      translation = []
      for i in range(frame, len(sequence), 3):
        codon = sequence[i : i + 3]

        # Handle partial codons
        if len(codon) != 3:
          codon += "N" * (3 - len(codon))  # Add trailing Ns
        amino_acid = str(Bio.Seq.Seq(codon).translate())  # Convert to string
        translation.append(amino_acid)
      
      translated_read = ("".join(translation))  # Join strings
      # print(f"encoding and comparing read number: {read.id}, frame: {frame} read: {translated_read}")
      # print(f"translated_read: {translated_read}")
      with multiprocessing.Pool() as pool:
        pool.starmap(process_target_sequence, [(target_sequence, sequence_hashed, translated_read, read, frame, logging.getLogger()) for target_sequence, sequence_hashed in target_hashes.items()])
      #encode_compare(translated_read, read, frame)

def hash_read(translated_read, sequence_length):
  hashed_read = {}
  base = 256
  mod = 2**64
  
  hashed_read[0] = initial_hash(translated_read[:sequence_length], base, mod)
  for i in range(1, len(translated_read) - sequence_length + 1):
    hashed_read[i] = rolling_hash(hashed_read[i-1], translated_read[i - 1], translated_read[i + sequence_length - 1], sequence_length, base)
  return hashed_read
  
def rolling_hash(prev_hash, prev_char, next_char, sequence_length, base):
  mod = 2**64  # Large prime for modulo operation to avoid overflow
  new_hash = (prev_hash - ord(prev_char) * pow(base, sequence_length - 1, mod)) % mod
  new_hash = (new_hash * base + ord(next_char)) % mod
  return new_hash

def initial_hash(s, base, mod):
  h = 0
  for char in s:
      h = (h * base + ord(char)) % mod
  return h

def process_target_sequence(target_sequence, sequence_hashed, translated_read, read, frame, logger):
  sequence_length = len(target_sequence)
  for i, read_hash in hash_read(translated_read, sequence_length).items():   
    if sequence_hashed == read_hash:
      print(f"Target sequence found in read: {read.id}")
      print(f"Frame: {frame + 1}")
      print(f"Index: {i}")
      print(f"Original sequence: {read.id}")
      print(f"Original translated sequence: {translated_read}")

#TODO algorithms instead of hash for parallel search
def encode_compare(translated_read, read, frame):
  target_hashes = get_target_sequences("top_1000.csv")
  #print(f"target sequences are: {target_hashes.keys()}")
  for sequence, sequence_hashed in target_hashes.items():
    sequence_length = len(sequence)
    #print(f"searching for: {sequence}, length: {sequence_length}")
    for i, read_hash in hash_read(translated_read, sequence_length).items():
      
      if sequence_hashed == read_hash: 
        print(f"Target sequence found in read: {read.id}")
        print(f"Frame: {frame + 1}")
        print(f"index: {i}")
        print(f"Original sequence: {read.id}")
        print(f"Original translated sequence: {translated_read}")

        # # Find the specific matching target sequence
        # matching_target = target_hashes.values().get(read_hash)
        # if matching_target:  # Exact match
        #   print(f"Matching target sequence: {matching_target}")
        # else:  # Partial match
        #   print(f"Partial match with a target sequence")