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
  for record in Bio.SeqIO.parse(file_id, "fastq"):
    sequence = str(record.seq)
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
      print("".join(translation))  # Join strings
