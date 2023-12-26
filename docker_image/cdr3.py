import Bio.SeqIO
import hashlib

# Target sequences (replace with your actual sequences)
target_sequences = [
    "CAVMDSNYQLIW",  # Example 1
    "CAVRDSNYQLIW",
    "CAVMDSSYKLIF",
    "CAVNQAGTALIF",
    "CAVNTGGFKTIF",
    "VPRARKTPSIPA"
    # ... Add your other target sequences
]

# Pre-calculate SHA-256 hashes of target sequences
target_hashes = {hashlib.sha256(seq.encode()).hexdigest(): seq for seq in target_sequences}

def translate_frames(file_id):
  for read in Bio.SeqIO.parse(file_id, "fastq"):
    sequence = str(read.seq.complement())
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

      encode_compare(translated_read, read, frame, target_sequences)

def encode_compare(translated_read, read, frame, target_sequences):
  substrings = []
  hashes = {}
  for substring in target_sequences:
    substring_length = len(substring)
    for i in range(len(translated_read) - substring_length + 1):
      read_hash = hashlib.sha256(translated_read[i:i+substring_length].encode()).hexdigest()
      # Check if any target hash is a substring of the read hash
      for target_hash in target_hashes:
        if target_hash in read_hash: 
          print(f"Target sequence found in read: {read.id}")
          print(f"Frame: {frame + 1}")
          print(f"Original sequence: {read.id}")
          print(f"Original translated sequence: {translated_read}")

          # Find the specific matching target sequence
          matching_target = target_hashes.get(read_hash)
          if matching_target:  # Exact match
            print(f"Matching target sequence: {matching_target}")
          else:  # Partial match
            print(f"Partial match with a target sequence")