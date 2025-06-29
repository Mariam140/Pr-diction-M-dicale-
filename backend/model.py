import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

# Charger les données
df = pd.read_csv("heart.csv")
X = df.drop('target', axis=1)
y = df['target']

# Standardiser les données
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Séparer en train/test
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)

# Entraîner le modèle
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Sauvegarder modèle + scaler
joblib.dump((model, scaler), "main.pkl")
print("Modèle entraîné et sauvegardé !")
