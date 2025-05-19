import smtplib
from email.message import EmailMessage

# --- Cấu hình tài khoản gửi thử ---
SENDER = "lyquyen5519999@gmail.com"          # Gmail test (giả lập)
APP_PASSWORD = "fvtgwdsisqnhebvb"              # App password (16 ký tự)

# --- Người nhận ---
RECEIVER = "lyquyen5519999@gmail.com"          # Em nhập email của em ở đây

# --- Nội dung thư ---
msg = EmailMessage()
msg['Subject'] = "✅ Test Send Email from Python (Efflux Project)"
msg['From'] = SENDER
msg['To'] = RECEIVER
msg.set_content("This is a successful email test from your Efflux protein predictor app.\n\n✔ SMTP config OK!\n\n— Support")

# --- Gửi mail ---
try:
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=10) as server:
        server.starttls()
        server.login(SENDER, APP_PASSWORD)
        server.send_message(msg)
    print("✅ Email sent successfully!")
except Exception as e:
    print(f"❌ Failed to send email: {e}")
