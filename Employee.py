import pandas as pd
import streamlit as st

# --- Page Configuration ---
st.set_page_config(page_title="Unemployment Dashboard", layout="wide")

# --- Title ---
st.title("📊 Indian Unemployment Dashboard")
st.markdown("This dashboard provides insights into the unemployment data across Indian states.")

# --- Load and Clean Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("C:/Users/priya/PycharmProjects/gestureVolume/unemployment_data.csv")
 # replace with your correct path
    df.columns = [col.strip() for col in df.columns]  # remove whitespace from column names
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
    df.dropna(subset=['Date'], inplace=True)
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.strftime('%b')
    return df

df = load_data()

# --- Sidebar Filters ---
st.sidebar.header("📍 Filter Options")

regions = df['Region'].dropna().unique()
selected_region = st.sidebar.multiselect("Select Region(s)", options=regions, default=regions)

years = sorted(df['Year'].dropna().unique())
selected_year = st.sidebar.multiselect("Select Year(s)", options=years, default=years)

# --- Filter Data ---
filtered_df = df[(df['Region'].isin(selected_region)) & (df['Year'].isin(selected_year))]

# --- Display Filtered Data ---
st.subheader("📅 Filtered Data")
st.dataframe(filtered_df)

# --- Line Chart: Unemployment Rate over Time ---
st.subheader("📈 Estimated Unemployment Rate Over Time")
chart_data = filtered_df[['Date', 'Estimated Unemployment Rate (%)', 'Region']].sort_values('Date')
chart_pivot = chart_data.pivot_table(index='Date', columns='Region', values='Estimated Unemployment Rate (%)')

st.line_chart(chart_pivot)
