from Bio import SeqIO
import pandas as pd
import itertools

# Danh sách 20 amino acid chuẩn
amino_acids = 'ACDEFGHIKLMNPQRSTVWY'
dipeptides = [a + b for a in amino_acids for b in amino_acids]  # 400 cặp

def compute_aac(seq):
    length = len(seq)
    return [seq.count(aa) / length for aa in amino_acids]

def compute_dpc(seq):
    length = len(seq) - 1
    dpc_values = []
    for dp in dipeptides:
        count = sum(1 for i in range(length) if seq[i:i+2] == dp)
        dpc_values.append(count / length if length > 0 else 0)
    return dpc_values

# Đọc file fasta
records = list(SeqIO.parse("efflux.fasta", "fasta"))

features = []
labels = []
ids = []

def assign_family(header):
    header = header.lower()
    if any(x in header for x in ["mdtk", "mdt", "nor", "norm"]):
        return "MFS"
    elif any(x in header for x in ["acr", "mex", "mexa", "mexb"]):
        return "RND"
    elif any(x in header for x in ["emre", "smr", "qac"]):
        return "SMR"
    elif any(x in header for x in ["abc", "cdr", "cdrl"]):
        return "ABC"
    else:
        return "Unknown"

print("🔍 Đang tính AAC + DPC cho từng chuỗi protein...")
for record in records:
    seq = str(record.seq)
    header = record.description
    family = assign_family(header)

    if family != "Unknown":
        aac = compute_aac(seq)
        dpc = compute_dpc(seq)
        combined = aac + dpc
        features.append(combined)
        labels.append(family)
        ids.append(record.id)
        print(f"✔ {record.id} → {family}")
    else:
        print(f"⚠ Bỏ qua {record.id} (không rõ family)")

# Gộp tên cột: AAC + DPC
aac_cols = list(amino_acids)
dpc_cols = dipeptides
all_cols = aac_cols + dpc_cols

df = pd.DataFrame(features, columns=all_cols)
df["label"] = labels
df["id"] = ids
df.to_csv("AAC_DPC_features_clean.csv", index=False)
print("✅ Đã lưu thành 'AAC_DPC_features_clean.csv'")
