import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import plotly.express as px
from plotly.graph_objects import Figure
import joblib
import os

def train_model(df: pd.DataFrame) -> tuple[RandomForestRegressor, dict]:
    """
    Train a Random Forest model to predict life expectancy.
    If a saved model exists, it will be loaded instead of training a new one.
    
    Args:
        df (pd.DataFrame): The input dataframe
        
    Returns:
        tuple: (trained model, feature ranges dictionary)
    """
    model_path = 'model.joblib'
    ranges_path = 'feature_ranges.joblib'
    
    # Check if saved model exists
    if os.path.exists(model_path) and os.path.exists(ranges_path):
        model = joblib.load(model_path)
        feature_ranges = joblib.load(ranges_path)
        return model, feature_ranges
    
    # Prepare features and target
    features = ['GDP per capita', 'headcount_ratio_upper_mid_income_povline', 'year']
    X = df[features]
    y = df['Life Expectancy (IHME)']
    
    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Get feature ranges for input validation
    feature_ranges = {
        'GDP per capita': (df['GDP per capita'].min(), df['GDP per capita'].max()),
        'headcount_ratio_upper_mid_income_povline': (df['headcount_ratio_upper_mid_income_povline'].min(), 
                                                   df['headcount_ratio_upper_mid_income_povline'].max()),
        'year': (int(df['year'].min()), int(df['year'].max()))
    }
    
    # Save model and ranges
    joblib.dump(model, model_path)
    joblib.dump(feature_ranges, ranges_path)
    
    return model, feature_ranges

def predict_life_expectancy(model: RandomForestRegressor, 
                          gdp: float, 
                          poverty_rate: float, 
                          year: int) -> float:
    """
    Predict life expectancy for given input values.
    
    Args:
        model: Trained Random Forest model
        gdp: GDP per capita value
        poverty_rate: Poverty rate value
        year: Year value
        
    Returns:
        float: Predicted life expectancy
    """
    # Create input array
    X_pred = np.array([[gdp, poverty_rate, year]])
    
    # Make prediction
    prediction = model.predict(X_pred)[0]
    
    return prediction

def plot_feature_importance(model: RandomForestRegressor, 
                          features: list[str]) -> Figure:
    """
    Create a bar plot of feature importance.
    
    Args:
        model: Trained Random Forest model
        features: List of feature names
        
    Returns:
        Figure: Plotly figure object
    """
    # Get feature importance
    importance = model.feature_importances_
    
    # Create DataFrame for plotting
    importance_df = pd.DataFrame({
        'Feature': features,
        'Importance': importance
    }).sort_values('Importance', ascending=True)
    
    # Create bar plot
    fig = px.bar(
        importance_df,
        x='Importance',
        y='Feature',
        orientation='h',
        title='Feature Importance for Life Expectancy Prediction',
        labels={'Importance': 'Relative Importance', 'Feature': 'Features'}
    )
    
    # Update layout
    fig.update_layout(
        showlegend=False,
        yaxis_title='',
        xaxis_title='Relative Importance'
    )
    
    return fig 