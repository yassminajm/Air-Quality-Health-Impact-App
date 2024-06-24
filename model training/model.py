# -*- coding: utf-8 -*-

# Import libraries
import pandas as pd
from sklearn.preprocessing import StandardScaler
# !pip install scikit-learn==1.2.2
# !pip install imbalanced-learn=0.10.1
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
import joblib

# Load data
df = pd.read_csv('air_quality_health_impact_data.csv')
df['HealthImpactClass'] = df['HealthImpactClass'].astype(int)
df.drop(columns=['RecordID'], axis=1, inplace=True)

# Split data
X = df.drop(columns=['HealthImpactScore', 'HealthImpactClass'], axis=1)
y = df['HealthImpactClass']
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
smote = SMOTE(sampling_strategy={2:546, 3: 285, 4: 224}, random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42, stratify=y_resampled)

# Train and evaluate data
xgb_clf = XGBClassifier(n_estimators=100, objective='multi:softmax')
xgb_clf.fit(X_train, y_train)
y_pred_xgb = xgb_clf.predict(X_test)

# Save model
joblib.dump(xgb_clf, 'xgboost_model.joblib')