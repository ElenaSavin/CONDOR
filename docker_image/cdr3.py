import Bio.SeqIO
import hashlib

# Target sequences (replace with your actual sequences)
target_sequences = [
    "MLLGSFRLIPKET",  # Example 1
    "CASIQKFGERPF",   # Example 2
    # ... Add your other target sequences
]

# Pre-calculate SHA-256 hashes of target sequences
target_hashes = {hashlib.sha256(seq.encode()).hexdigest(): seq for seq in target_sequences}

def translate_frames(file_id):
  for read in Bio.SeqIO.parse(file_id, "fastq"):
    sequence = str(read.seq)
    for frame in range(3):
      translation = []
      for i in range(frame, len(sequence), 3):
        codon = sequence[i : i + 3]
        # Handle partial codons
        if len(codon) != 3:
          codon += "N" * (3 - len(codon))  # Add trailing Ns
        amino_acid = str(Bio.Seq.Seq(codon).translate())  # Convert to string
        translation.append(amino_acid)
      
      print(f">Frame {frame + 1}")
      translated_read = ("".join(translation))  # Join strings
      encode_compare(translated_read, read, frame)

def encode_compare(translated_read, read, frame):
  read_hash = hashlib.sha256(translated_read.encode()).hexdigest()
  # Check if any target hash is a substring of the read hash
  if any(target_hash in read_hash for target_hash in target_hashes):
    print(f"Target sequence found in read: {read.id}")
    print(f"Frame: {frame + 1}")
    print(f"Original sequence: {translated_read}")

    # Find the specific matching target sequence
    matching_target = target_hashes.get(read_hash)
    if matching_target:  # Exact match
      print(f"Matching target sequence: {matching_target}")
    else:  # Partial match
      print(f"Partial match with a target sequence")