import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score
import joblib

# 1. Đọc dữ liệu từ file AAC đã xử lý
df = pd.read_csv("AAC_features_clean.csv")

# 2. Tách đặc trưng và nhãn
X = df.drop(columns=["label", "id"]).astype(float)
y = df["label"]

# 3. Chia train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 4. Huấn luyện SVM
model = SVC(kernel='linear', probability=True)
model.fit(X_train, y_train)

# 5. Dự đoán và đánh giá
y_pred = model.predict(X_test)
print("🎯 Accuracy:", accuracy_score(y_test, y_pred))
print("\n📋 Classification Report:\n", classification_report(y_test, y_pred))

# 6. Lưu mô hình
joblib.dump(model, "svm_efflux_model.pkl")
print("✅ Mô hình đã được lưu thành 'svm_efflux_model.pkl'")
