import streamlit as st
import pandas as pd
import joblib
from Bio import SeqIO
import io
import smtplib
from email.message import EmailMessage
import re

# === Email configuration ===
SENDER_EMAIL = "lyquyen5519999@gmail.com"
APP_PASSWORD = "fvtgwdsisqnhebvb"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# === Validate email format ===
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# === Load trained model ===
model = joblib.load("svm_efflux_model.pkl")

# === Feature extraction ===
amino_acids = 'ACDEFGHIKLMNPQRSTVWY'
dipeptides = [a + b for a in amino_acids for b in amino_acids]

def compute_aac(seq):
    length = len(seq)
    return [seq.count(aa) / length for aa in amino_acids]

def compute_dpc(seq):
    length = len(seq) - 1
    return [
        sum(1 for i in range(length) if seq[i:i+2] == dp) / length if length > 0 else 0
        for dp in dipeptides
    ]

# === Email sender ===
def send_email(receiver_email, result_df, username):
    msg = EmailMessage()
    msg['Subject'] = 'Efflux Protein Family Prediction Results'
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver_email
    msg.set_content(f"""
Hello {username},

Thank you for using the Efflux Protein Family Predictor tool.
Please find your prediction results attached in the CSV file.

Best regards,
Efflux Bioinformatics Team
""")
    csv_data = result_df.to_csv(index=False)
    msg.add_attachment(csv_data.encode('utf-8'), maintype='text', subtype='csv', filename='prediction_result.csv')

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)

# === UI title ===
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🧬 Efflux Protein Family Predictor</h1>", unsafe_allow_html=True)

# === Initialize session state
for key in ['submitted', 'name', 'email', 'result_df', 'email_sent']:
    if key not in st.session_state:
        st.session_state[key] = None if key == 'result_df' else False if key in ['submitted', 'email_sent'] else ""

# === Upload file
uploaded_file = st.file_uploader("📂 Upload your FASTA file", type=["fasta"])

# === Start processing
if st.button("🚀 Start Processing"):
    if not st.session_state.get('submitted') and not uploaded_file:
        st.warning("⚠ Please enter your information and upload a FASTA file.")
    elif not st.session_state.get('submitted'):
        st.warning("⚠ Please enter your information (name and email) before processing.")
    elif not uploaded_file:
        st.warning("⚠ Please upload a FASTA file before processing.")
    else:
        fasta_text = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
        records = list(SeqIO.parse(fasta_text, "fasta"))

        result_rows = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        total = len(records)

        st.info(f"🔄 Processing {total} protein sequences...")

        for i, record in enumerate(records):
            seq = str(record.seq)
            aac = compute_aac(seq)
            dpc = compute_dpc(seq)
            combined = aac + dpc

            pred = model.predict([combined])[0]
            prob = model.predict_proba([combined])[0].max()

            result_rows.append({
                "Protein ID": record.id,
                "Predicted Family": pred,
                "Confidence": round(prob, 3)
            })

            percent = (i + 1) / total
            progress_bar.progress(percent)
            status_text.text(f"⏳ Processing: {i + 1}/{total} ({int(percent * 100)}%)")

        st.session_state['result_df'] = pd.DataFrame(result_rows)
        st.success(f"✅ Submission successful! Hello {st.session_state['name']}, your file has been processed.")
        st.dataframe(st.session_state['result_df'])


# === User info form
if not st.session_state['submitted']:
    with st.form("user_info_form"):
        st.write("👤 Please enter your information:")
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        submitted = st.form_submit_button("✅ Submit")

    if submitted:
        if not is_valid_email(email):
            st.error("❌ Invalid email address.")
        elif not uploaded_file:
            st.warning("⚠ Please upload your FASTA file before submitting.")
        else:
            st.session_state['name'] = name
            st.session_state['email'] = email
            st.session_state['submitted'] = True
            st.session_state['email_sent'] = False
            st.info("📌 Info submitted. Now click 'Start Processing' to begin.")
else:
    st.success(f"👋 Hello {st.session_state['name']}, your information has already been submitted.")

# === Download CSV
if st.session_state['result_df'] is not None:
    csv = st.session_state['result_df'].to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV Results", data=csv, file_name="prediction_result.csv", mime="text/csv")

# === Send Email button
if st.session_state['result_df'] is not None and st.session_state['submitted']:
    if not st.session_state['email_sent']:
        if st.button("📧 Send Results via Email"):
            try:
                send_email(st.session_state['email'], st.session_state['result_df'], st.session_state['name'])
                st.success(f"📩 Results have been sent to {st.session_state['email']}!")
                st.session_state['email_sent'] = True
            except Exception as e:
                st.error(f"❌ Failed to send email: {e}") 