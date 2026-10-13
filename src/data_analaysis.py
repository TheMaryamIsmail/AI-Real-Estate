import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

class RealEstateEDA:
    def __init__(self, train_path="data/train.csv"):
        self.df = pd.read_csv(train_path)
        os.makedirs("static/images", exist_ok=True)

    def clean_data(self):
        # Handle missing values for key features
        self.df['LotFrontage'] = self.df['LotFrontage'].fillna(self.df['LotFrontage'].median())
        self.df['GarageYrBlt'] = self.df['GarageYrBlt'].fillna(self.df['YearBuilt'])
        
        # Fill categorical missing values with 'None' or Mode
        cat_cols_none = ['Alley', 'FireplaceQu', 'GarageType', 'GarageFinish', 'GarageQual', 'GarageCond', 'PoolQC', 'Fence', 'MiscFeature', 'BsmtQual', 'BsmtCond', 'BsmtExposure', 'BsmtFinType1', 'BsmtFinType2']
        for col in cat_cols_none:
            if col in self.df.columns:
                self.df[col] = self.df[col].fillna('None')

        return self.df

    def generate_visualizations(self):
        sns.set_theme(style="whitegrid")
        
        # 1. Price Distribution
        plt.figure(figsize=(8, 5))
        sns.histplot(self.df['SalePrice'], kde=True, color='teal')
        plt.title('Property Price Distribution')
        plt.xlabel('Sale Price ($)')
        plt.savefig('static/images/price_distribution.png', bbox_inches='tight')
        plt.close()

        # 2. Living Area vs Sale Price
        plt.figure(figsize=(8, 5))
        sns.scatterplot(x='GrLivArea', y='SalePrice', data=self.df, alpha=0.6, color='purple')
        plt.title('Above Grade Living Area vs Sale Price')
        plt.xlabel('Living Area (sq ft)')
        plt.ylabel('Sale Price ($)')
        plt.savefig('static/images/area_vs_price.png', bbox_inches='tight')
        plt.close()

if __name__ == "__main__":
    eda = RealEstateEDA()
    eda.clean_data()
    eda.generate_visualizations()
    print("EDA and Visualizations completed successfully.")