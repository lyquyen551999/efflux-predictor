from Bio import SeqIO
import pandas as pd

# Danh sách 20 amino acid chuẩn
amino_acids = 'ACDEFGHIKLMNPQRSTVWY'

def compute_aac(seq):
    length = len(seq)
    return [seq.count(aa) / length for aa in amino_acids]

# Đọc file fasta
records = list(SeqIO.parse("efflux.fasta", "fasta"))

aac_features = []
labels = []
ids = []

# Gán nhãn theo header
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

print("🔍 Đang xử lý các chuỗi protein...")
for record in records:
    seq = str(record.seq)
    header = record.description
    aac = compute_aac(seq)
    family = assign_family(header)
    
    if family != "Unknown":
        aac_features.append(aac)
        labels.append(family)
        ids.append(record.id)
        print(f"✔ {record.id} → {family}")
    else:
        print(f"⚠ Bỏ qua {record.id} (không rõ family)")

# Tạo DataFrame và lưu
df = pd.DataFrame(aac_features, columns=list(amino_acids))
df["label"] = labels
df["id"] = ids
df.to_csv("AAC_features_clean.csv", index=False)

print("✅ Hoàn tất! Đã lưu thành AAC_features_clean.csv")
