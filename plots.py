import plotly.express as px
import pandas as pd
from plotly.graph_objects import Figure

def create_gdp_life_expectancy_scatter(df: pd.DataFrame, selected_year: int) -> Figure:
    """
    Create a scatter plot of GDP per capita vs Life Expectancy for a selected year.
    
    Args:
        df (pd.DataFrame): The input dataframe
        selected_year (int): The year to filter the data
        
    Returns:
        Figure: A plotly figure object
    """
    # Filter data for selected year
    year_data = df[df['year'] == selected_year]
    
    # Create scatter plot
    fig = px.scatter(
        year_data,
        x='GDP per capita',
        y='Life Expectancy (IHME)',
        hover_data=['country', 'Population'],
        size='Population',
        color='headcount_ratio_upper_mid_income_povline',
        color_continuous_scale='Viridis',
        log_x=True,  # Log scale for GDP
        title=f'Relationship between GDP per Capita and Life Expectancy ({selected_year})',
        labels={
            'GDP per capita': 'GDP per Capita (USD, log scale)',
            'Life Expectancy (IHME)': 'Life Expectancy (years)',
            'headcount_ratio_upper_mid_income_povline': 'Poverty Rate (%)'
        }
    )
    
    # Update layout
    fig.update_layout(
        xaxis_title='GDP per Capita (USD, log scale)',
        yaxis_title='Life Expectancy (years)',
        hovermode='closest',
        showlegend=True
    )
    
    return fig

def create_country_trend_plot(df: pd.DataFrame, selected_countries: list[str]) -> Figure:
    """
    Create a line chart showing life expectancy and GDP trends for selected countries.
    
    Args:
        df (pd.DataFrame): The input dataframe
        selected_countries (list[str]): List of countries to plot
        
    Returns:
        Figure: Plotly figure object
    """
    # Filter data for selected countries
    country_data = df[df['country'].isin(selected_countries)]
    
    # Create figure with secondary y-axis
    fig = px.line(
        country_data,
        x='year',
        y='Life Expectancy (IHME)',
        color='country',
        title='Life Expectancy and GDP Trends by Country',
        labels={
            'year': 'Year',
            'Life Expectancy (IHME)': 'Life Expectancy (years)',
            'country': 'Country'
        }
    )
    
    # Add GDP line
    fig.add_trace(
        px.line(
            country_data,
            x='year',
            y='GDP per capita',
            color='country',
            line_dash='country'
        ).data[0]
    )
    
    # Update layout
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Life Expectancy (years)',
        yaxis2=dict(
            title='GDP per Capita (USD)',
            overlaying='y',
            side='right'
        ),
        hovermode='x unified',
        showlegend=True
    )
    
    # Update traces
    for i, trace in enumerate(fig.data):
        if i < len(selected_countries):  # Life expectancy traces
            trace.name = f"{trace.name} - Life Expectancy"
        else:  # GDP traces
            trace.name = f"{trace.name} - GDP"
            trace.yaxis = 'y2'
    
    return fig

def create_world_map(df: pd.DataFrame, selected_year: int) -> Figure:
    """
    Create a choropleth world map showing life expectancy by country.
    
    Args:
        df (pd.DataFrame): The input dataframe
        selected_year (int): The year to display
        
    Returns:
        Figure: Plotly figure object
    """
    # Filter data for selected year
    year_data = df[df['year'] == selected_year]
    
    # Create choropleth map
    fig = px.choropleth(
        year_data,
        locations='country',
        locationmode='country names',
        color='Life Expectancy (IHME)',
        hover_name='country',
        hover_data={
            'Life Expectancy (IHME)': ':.1f',
            'GDP per capita': ':,.0f',
            'headcount_ratio_upper_mid_income_povline': ':.1f',
            'country': False
        },
        color_continuous_scale='Viridis',
        title=f'World Life Expectancy Map ({selected_year})',
        labels={'Life Expectancy (IHME)': 'Life Expectancy (years)'}
    )
    
    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='equirectangular'
        )
    )
    
    return fig

def create_gdp_poverty_scatter(df: pd.DataFrame, selected_year: int) -> Figure:
    """
    Create a scatter plot of GDP vs Poverty Rate.
    
    Args:
        df (pd.DataFrame): The input dataframe
        selected_year (int): The year to display
        
    Returns:
        Figure: Plotly figure object
    """
    # Filter data for selected year
    year_data = df[df['year'] == selected_year]
    
    # Create scatter plot
    fig = px.scatter(
        year_data,
        x='GDP per capita',
        y='headcount_ratio_upper_mid_income_povline',
        hover_data=['country', 'Life Expectancy (IHME)'],
        size='Population',
        color='Life Expectancy (IHME)',
        color_continuous_scale='Viridis',
        log_x=True,
        title=f'Relationship between GDP and Poverty Rate ({selected_year})',
        labels={
            'GDP per capita': 'GDP per Capita (USD, log scale)',
            'headcount_ratio_upper_mid_income_povline': 'Poverty Rate (%)',
            'Life Expectancy (IHME)': 'Life Expectancy (years)'
        }
    )
    
    fig.update_layout(
        xaxis_title='GDP per Capita (USD, log scale)',
        yaxis_title='Poverty Rate (%)',
        hovermode='closest'
    )
    
    return fig

def create_life_expectancy_boxplot(df: pd.DataFrame, selected_year: int) -> Figure:
    """
    Create a box plot of life expectancy by region.
    
    Args:
        df (pd.DataFrame): The input dataframe
        selected_year (int): The year to display
        
    Returns:
        Figure: Plotly figure object
    """
    # Filter data for selected year
    year_data = df[df['year'] == selected_year]
    
    # Create box plot
    fig = px.box(
        year_data,
        x='country',
        y='Life Expectancy (IHME)',
        title=f'Life Expectancy Distribution by Country ({selected_year})',
        labels={
            'country': 'Country',
            'Life Expectancy (IHME)': 'Life Expectancy (years)'
        }
    )
    
    fig.update_layout(
        xaxis_title='Country',
        yaxis_title='Life Expectancy (years)',
        xaxis={'tickangle': 45}
    )
    
    return fig 