import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Đọc dữ liệu đã có AAC + DPC (420 features)
df = pd.read_csv("AAC_DPC_features_clean.csv")

# Tách đặc trưng và nhãn
X = df.drop(columns=["label", "id"]).astype(float)
y = df["label"]

# Chia train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Huấn luyện lại SVM với 420 đặc trưng
model = SVC(kernel='linear', probability=True)
model.fit(X_train, y_train)

# Dự đoán và đánh giá
y_pred = model.predict(X_test)
print("🎯 Accuracy:", accuracy_score(y_test, y_pred))
print("\n📋 Classification Report:\n", classification_report(y_test, y_pred))

# Ghi lại mô hình mới
joblib.dump(model, "svm_efflux_model.pkl")
print("✅ Mô hình mới đã được lưu thành 'svm_efflux_model.pkl'")
