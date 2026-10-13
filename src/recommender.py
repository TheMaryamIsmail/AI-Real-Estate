import pandas as pd

class PropertyRecommender:
    def __init__(self, data_path="data/train.csv"):
        self.df = pd.read_csv(data_path)

    def recommend(self, max_budget: float, min_beds: int, neighborhood: str = None):
        filtered = self.df[
            (self.df['SalePrice'] <= max_budget) & 
            (self.df['BedroomAbvGr'] >= min_beds)
        ]
        
        if neighborhood and neighborhood != "Any":
            filtered = filtered[filtered['Neighborhood'].str.lower() == neighborhood.lower()]
            
        recommendations = []
        for _, row in filtered.head(5).iterrows():
            explanation = (
                f"Recommended because it fits your budget of ${max_budget:,.0f} "
                f"at a list price of ${row['SalePrice']:,.0f}, features {row['BedroomAbvGr']} bedrooms, "
                f"and is located in the desirable {row['Neighborhood']} neighborhood with an overall quality score of {row['OverallQual']}/10."
            )
            recommendations.append({
                "id": int(row['Id']),
                "neighborhood": row['Neighborhood'],
                "price": float(row['SalePrice']),
                "bedrooms": int(row['BedroomAbvGr']),
                "living_area": int(row['GrLivArea']),
                "explanation": explanation
            })
            
        return recommendations