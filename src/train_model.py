import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import joblib
import os

def train_and_save_model():
    df = pd.read_csv("data/train.csv")
    
    # Select key predictive features
    features = ['OverallQual', 'GrLivArea', 'GarageCars', 'TotalBsmtSF', 'FullBath', 'YearBuilt', 'Neighborhood']
    target = 'SalePrice'
    
    X = df[features]
    y = df[target]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    numeric_features = ['OverallQual', 'GrLivArea', 'GarageCars', 'TotalBsmtSF', 'FullBath', 'YearBuilt']
    categorical_features = ['Neighborhood']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', SimpleImputer(strategy='median'), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ]
    )
    
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])
    
    model.fit(X_train, y_train)
    
    preds = model.predict(X_test)
    print(f"Model R2 Score: {r2_score(y_test, preds):.4f}")
    print(f"Model RMSE: {np.sqrt(mean_squared_error(y_test, preds)):.2f}")
    
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/house_price_model.pkl")
    print("Model saved to models/house_price_model.pkl")

if __name__ == "__main__":
    train_and_save_model()