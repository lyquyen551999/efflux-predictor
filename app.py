import streamlit as st
import pandas as pd
import joblib
from Bio import SeqIO
import io

# Load mô hình đã huấn luyện
model = joblib.load("svm_efflux_model.pkl")

# Danh sách 20 amino acid chuẩn
amino_acids = 'ACDEFGHIKLMNPQRSTVWY'

def compute_aac(seq):
    length = len(seq)
    return [seq.count(aa) / length for aa in amino_acids]

# Giao diện chính
st.title("🧬 Efflux Protein Family Predictor")

st.markdown("""
Upload một file `.fasta` chứa các chuỗi protein để dự đoán họ vận chuyển (Efflux family).
""")

uploaded_file = st.file_uploader("📂 Chọn file FASTA", type=["fasta"])

if uploaded_file:
    # Đọc nội dung dạng văn bản
    fasta_text = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
    records = list(SeqIO.parse(fasta_text, "fasta"))

    result_rows = []
    for record in records:
        seq = str(record.seq)
        aac = compute_aac(seq)
        pred = model.predict([aac])[0]
        prob = model.predict_proba([aac])[0].max()

        result_rows.append({
            "Protein ID": record.id,
            "Predicted Family": pred,
            "Confidence": round(prob, 3)
        })

    result_df = pd.DataFrame(result_rows)
    st.success("✅ Work done!")
    st.dataframe(result_df)

    # Cho phép tải kết quả về
    csv = result_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 DownloadDownload CSV", data=csv, file_name="prediction_result.csv", mime="text/csv")
