import streamlit as st
import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
from evidently.metrics import DatasetDriftMetric, DataDriftTable
import io

# Streamlit App
st.title("Data Drift Detection and Visualization App")

# File upload
# uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

# Option to use a sample dataset
use_sample = st.checkbox("Use UCI Air Quality Dataset instead of uploading a file")
if use_sample:
    data = pd.read_csv('air_quality_uci.csv')
    st.success(f"Loaded sample data")
else:
    # File upload
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)

if 'data' in locals():
    # Load CSV into a DataFrame
    # data = pd.read_csv(uploaded_file)
    st.write("Preview of the Uploaded Data:")
    st.write(data.head())
    
    # Allow user to select reference and current data
    with st.sidebar:
        st.header("Drift Detection Configuration")
        
        # Choose columns for drift detection
        selected_columns = st.multiselect(
            "Select columns to evaluate for drift",
            options=data.columns.tolist(),
            default=data.columns.tolist()
        )
        
        # Split data into reference and current datasets
        st.write("Split data into reference and current datasets")
        split_ratio = st.slider(" Choose test set size(from last)", 0.1, 0.9, 0.5)
        split_index = int(len(data) * split_ratio)
        
        reference_data = data.iloc[:split_index][selected_columns]
        current_data = data.iloc[split_index:][selected_columns]

    if st.button("Run Drift Detection"):
        # Run drift detection using Evidently
        report = Report(metrics=[
            DataDriftPreset(),
            # DatasetDriftMetric(),
            # DataDriftTable()
        ])
        
        report.run(reference_data=reference_data, current_data=current_data)
        
        # Save the report as an HTML
        html_buffer = io.StringIO()
        report.save_html(html_buffer)
        report_html = html_buffer.getvalue()

        # Visualization in Streamlit
        st.header("Data Drift Report Visualization")
        st.components.v1.html(report_html, height=1000, width=800, scrolling=True)

        # Option to download the report
        st.download_button(
            label="Download Drift Detection Report (HTML)",
            data=report_html,
            file_name="drift_report.html",
            mime="text/html"
        )