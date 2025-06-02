import streamlit as st
import pandas as pd
import io
from plots import create_gdp_life_expectancy_scatter, create_country_trend_plot # import from plots.py
from model import train_model, predict_life_expectancy, plot_feature_importance

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
#st.write("Available columns:", df.columns.tolist())

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
    
    # Add scatter plot
    st.plotly_chart(
        create_gdp_life_expectancy_scatter(df, selected_year),
        use_container_width=True
    )
    
    # Add model section
    st.header("Life Expectancy Prediction Model")
    
    # Train model
    model, feature_ranges = train_model(df)
    
    # Create input fields
    col1, col2, col3 = st.columns(3)
    
    with col1:
        gdp = st.number_input(
            "GDP per Capita (USD)",
            min_value=float(feature_ranges['GDP per capita'][0]),
            max_value=float(feature_ranges['GDP per capita'][1]),
            value=float(feature_ranges['GDP per capita'][0]),
            step=1000.0
        )
    
    with col2:
        poverty_rate = st.number_input(
            "Poverty Rate (%)",
            min_value=float(feature_ranges['headcount_ratio_upper_mid_income_povline'][0]),
            max_value=float(feature_ranges['headcount_ratio_upper_mid_income_povline'][1]),
            value=float(feature_ranges['headcount_ratio_upper_mid_income_povline'][0]),
            step=1.0
        )
    
    with col3:
        year = st.number_input(
            "Year",
            min_value=int(feature_ranges['year'][0]),
            max_value=int(feature_ranges['year'][1]),
            value=int(feature_ranges['year'][1]),
            step=1
        )
    
    # Make prediction
    if st.button("Predict Life Expectancy"):
        prediction = predict_life_expectancy(model, gdp, poverty_rate, year)
        st.metric(
            label="Predicted Life Expectancy",
            value=f"{prediction:.1f} years"
        )
    
    # Show feature importance
    st.subheader("Feature Importance")
    st.plotly_chart(
        plot_feature_importance(model, ['GDP per capita', 'Poverty Rate', 'Year']),
        use_container_width=True
    )

with tab2:
    st.header("Country Deep Dive")
    
    # Country selection
    countries = sorted(df['country'].unique())
    default_countries = ['United States', 'Russia', 'China', 'Germany', 'Thailand']
    selected_countries = st.multiselect(
        "Select Countries to Compare",
        options=countries,
        default=default_countries
    )
    
    if selected_countries:
        # Create trend plot
        st.plotly_chart(
            create_country_trend_plot(df, selected_countries),
            use_container_width=True
        )
        
        # Show summary statistics
        st.subheader("Summary Statistics")
        
        # Filter data for selected countries
        country_data = df[df['country'].isin(selected_countries)]
        
        # Calculate statistics
        stats = country_data.groupby('country').agg({
            'Life Expectancy (IHME)': ['mean', 'min', 'max'],
            'GDP per capita': ['mean', 'min', 'max'],
            'headcount_ratio_upper_mid_income_povline': ['mean', 'min', 'max']
        }).round(2)
        
        # Display statistics
        st.dataframe(stats)
    else:
        st.info("Please select at least one country to view the trends.")

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