import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(page_title="Gyro Dashboard", layout="wide")
st.title("Streamlit Gyroscope Dashboard")

# Auto-refresh every 10 seconds to simulate live data integration
from streamlit_autorefresh import st_autorefresh  # only if external package
st_autorefresh(interval=10 * 1000, limit=None, key="refresh")

@st.cache_data
def load_data(file):
    try:
        df = pd.read_csv(file)
        df['time'] = df.index
        return df
    except FileNotFoundError:
        st.error(f"Data file '{file}' not found. Please place it in the same directory.")
        return None

# Load your data
df = load_data('clean.csv')

if df is not None:
    # Controls in the Sidebar
    st.sidebar.header("Controls")
    chart_type = st.sidebar.selectbox("Chart Type", ('Line', 'Scatter', 'Distribution'))
    axis = st.sidebar.selectbox("Axis", ('all', 'x', 'y', 'z'))
    n_samples = st.sidebar.number_input("Number of Samples", 50, len(df), 150, 10)

    # Navigation and Data Slicing
    if 'start_index' not in st.session_state:
        st.session_state.start_index = 0

    col1, col2 = st.sidebar.columns(2)
    if col1.button("Previous"):
        st.session_state.start_index = max(0, st.session_state.start_index - n_samples)
    if col2.button("Next"):
        if st.session_state.start_index + n_samples < len(df):
            st.session_state.start_index += n_samples

    start = st.session_state.start_index
    end = start + n_samples
    data_slice = df.iloc[start:end]
    plot_cols = ['x', 'y', 'z'] if axis == 'all' else [axis]
    st.sidebar.info(f"Showing samples {start} to {end-1}")

    # Plotting and Summary
    st.header(f"{chart_type} Plot for '{axis}' axis")

    if chart_type in ['Line', 'Scatter']:
        chart_data = data_slice.set_index('time')[plot_cols]
        if chart_type == 'Line':
            st.line_chart(chart_data)
        else:
            st.scatter_chart(chart_data)
    else:  # Distribution
        fig, ax = plt.subplots()
        data_slice[plot_cols].plot(kind='hist', ax=ax, alpha=0.7, bins=30, legend=True)
        ax.set_xlabel("Gyroscope Value")
        st.pyplot(fig)

    # Summary table
    st.header("Summary of Current Data")
    st.write(data_slice[plot_cols].describe())
