import pandas as pd
import pydeck as pdk
from typing import Dict, List

def get_country_coordinates() -> pd.DataFrame:
    """
    Returns a DataFrame with country coordinates.
    This is a simplified version - in a real application, you would use a proper geocoding service.
    """
    return pd.DataFrame({
        'country': ['United States', 'China', 'Germany', 'Russia', 'Thailand'],
        'lat': [37.0902, 35.8617, 51.1657, 61.5240, 15.8700],
        'lon': [-95.7129, 104.1954, 10.4515, 105.3188, 100.9925]
    })

def create_map_layers(df: pd.DataFrame, selected_year: int) -> Dict[str, pdk.Layer]:
    """
    Create map layers for different metrics.
    
    Args:
        df (pd.DataFrame): The input dataframe
        selected_year (int): The year to display
        
    Returns:
        Dict[str, pdk.Layer]: Dictionary of layers
    """
    # Filter data for selected year
    year_data = df[df['year'] == selected_year]
    
    # Merge with coordinates
    coordinates = get_country_coordinates()
    map_data = pd.merge(year_data, coordinates, on='country', how='inner')
    
    # Add formatted columns for tooltips
    map_data['life_exp_str'] = map_data['Life Expectancy (IHME)'].round(1).astype(str) + ' years'
    map_data['gdp_str'] = map_data['GDP per capita'].round(0).map(lambda x: f"${int(x):,}")
    map_data['poverty_str'] = map_data['headcount_ratio_upper_mid_income_povline'].round(1).astype(str) + '%'
    
    # Create layers
    layers = {
        "Life Expectancy": pdk.Layer(
            "ScatterplotLayer",
            data=map_data,
            get_position=["lon", "lat"],
            get_fill_color=[255, 140, 0, 160],
            get_radius=50000,
            pickable=True,
            opacity=0.8,
            stroked=True,
            filled=True,
            radius_scale=6,
            radius_min_pixels=1,
            radius_max_pixels=100,
            line_width_min_pixels=1,
            auto_highlight=True
        ),
        "GDP per Capita": pdk.Layer(
            "HexagonLayer",
            data=map_data,
            get_position=["lon", "lat"],
            get_elevation="GDP per capita",
            elevation_scale=100,
            elevation_range=[0, 100000],
            extruded=True,
            pickable=True,
            color_range=[
                [255, 255, 178],
                [254, 217, 118],
                [254, 178, 76],
                [253, 141, 60],
                [240, 59, 32],
                [189, 0, 38]
            ],
            coverage=1,
            auto_highlight=True
        ),
        "Poverty Rate": pdk.Layer(
            "TextLayer",
            data=map_data,
            get_position=["lon", "lat"],
            get_text="country",
            get_color=[0, 0, 0, 200],
            get_size=12,
            get_alignment_baseline="'bottom'",
            pickable=True,
            auto_highlight=True
        )
    }
    
    return layers

def create_map_view(df: pd.DataFrame, selected_year: int, selected_layers: List[str]) -> pdk.Deck:
    """
    Create the map view with selected layers.
    
    Args:
        df (pd.DataFrame): The input dataframe
        selected_year (int): The year to display
        selected_layers (List[str]): List of layer names to display
        
    Returns:
        pdk.Deck: The deck object
    """
    all_layers = create_map_layers(df, selected_year)
    layers = [all_layers[layer] for layer in selected_layers if layer in all_layers]
    
    tooltip_data = {
        "html": """
            <b>Country:</b> {country}<br/>
            <b>Life Expectancy:</b> {life_exp_str}<br/>
            <b>GDP per Capita:</b> {gdp_str}<br/>
            <b>Poverty Rate:</b> {poverty_str}
        """,
        "style": {
            "backgroundColor": "white",
            "color": "black",
            "font-family": "Arial",
            "font-size": "12px",
            "padding": "10px"
        }
    }
    
    return pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=30,
            longitude=0,
            zoom=1,
            pitch=50,
        ),
        layers=layers,
        tooltip=tooltip_data
    ) 