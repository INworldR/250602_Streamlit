import streamlit as st
import pandas as pd
import io

# Set page to full width
st.set_page_config(layout="wide")

# Load the data
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/JohannaViktor/streamlit_practical/refs/heads/main/global_development_data.csv"
    df = pd.read_csv(url)
    return df

# Load the data
df = load_data()

# Debug: Print column names
st.write("Available columns:", df.columns.tolist())

# Header and Subtitle
st.title("Worldwide Analysis of Quality of Life and Economic Factors")
st.markdown("""
This app enables you to explore the relationships between poverty, 
life expectancy, and GDP across various countries and years. 
Use the panels to select options and interact with the data.
""")

# Create tabs
tab1, tab2, tab3 = st.tabs(["Global Overview", "Country Deep Dive", "Data Explorer"])

# Tab content will be added later
with tab1:
    st.header("Global Overview")
    
    # Year selection slider
    selected_year = st.slider(
        "Select Year",
        min_value=int(df['year'].min()),
        max_value=int(df['year'].max()),
        value=int(df['year'].max())
    )
    
    # Filter data for selected year
    year_data = df[df['year'] == selected_year]
    
    # Create 4 columns for metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Average Life Expectancy",
            value=f"{year_data['Life Expectancy (IHME)'].mean():.1f} years",
            help="Mean life expectancy across all countries"
        )
    
    with col2:
        st.metric(
            label="Median GDP per Capita",
            value=f"${year_data['GDP per capita'].median():,.0f}",
            help="Median GDP per capita across all countries"
        )
    
    with col3:
        st.metric(
            label="Average Poverty Rate",
            value=f"{year_data['headcount_ratio_upper_mid_income_povline'].mean():.1f}%",
            help="Mean poverty rate (upper-middle income poverty line) across all countries"
        )
    
    with col4:
        st.metric(
            label="Number of Countries",
            value=f"{len(year_data['country'].unique())}",
            help="Total number of countries in the dataset for the selected year"
        )

with tab2:
    st.write("Country Deep Dive content will be added here")

with tab3:
    st.header("Data Explorer")
    
    # Create two columns for filters
    col1, col2 = st.columns(2)
    
    with col1:
        # Country selection
        countries = sorted(df['country'].unique())
        default_countries = ['United States', 'Russia', 'China', 'Germany', 'Thailand']
        selected_countries = st.multiselect(
            "Select Countries",
            options=countries,
            default=default_countries
        )
    
    with col2:
        # Year range selection
        min_year = int(df['year'].min())
        max_year = int(df['year'].max())
        year_range = st.slider(
            "Select Year Range",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year)
        )
    
    # Filter the dataframe
    filtered_df = df[
        (df['country'].isin(selected_countries)) &
        (df['year'] >= year_range[0]) &
        (df['year'] <= year_range[1])
    ]
    
    # Display the filtered dataframe
    st.dataframe(filtered_df)
    
    # Add download button
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="Download Filtered Data as CSV",
        data=csv,
        file_name="filtered_development_data.csv",
        mime="text/csv"
    )