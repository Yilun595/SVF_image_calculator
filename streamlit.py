import streamlit as st
import cv2
import numpy as np
import os
import io
import zipfile
import pandas as pd  # Add this to requirements.txt
from SVF_img_calculator import SVF_img_cal as SVF

st.set_page_config(page_title="SVF Batch Calculator", layout="wide")

st.title("🏙️ SVF Batch Calculator")
st.write("Upload one or multiple fisheye images to calculate Sky View Factors in bulk.")

# --- 1. EXAMPLE DOWNLOAD SECTION ---
st.sidebar.header("Help & Resources")
example_files = ["ExampleImg/01.png", "ExampleImg/02.png", "ExampleImg/03.png"]
zip_buffer = io.BytesIO()
with zipfile.ZipFile(zip_buffer, "w") as zf:
    for file_path in example_files:
        if os.path.exists(file_path):
            zf.write(file_path, os.path.basename(file_path))

st.sidebar.download_button(
    label="Download Example Images (ZIP)",
    data=zip_buffer.getvalue(),
    file_name="SVF_Examples.zip",
    mime="application/zip"
)

# --- 2. SETTINGS ---
st.sidebar.header("Calculation Settings")
resize_dim = st.sidebar.slider("Resize Dimensions", 128, 1024, 512, step=128)
ring_num = st.sidebar.number_input("JW1984 Ring Number", min_value=1, max_value=100, value=10)

# --- 3. BATCH UPLOADER ---
# Note the 'accept_multiple_files=True'
uploaded_files = st.file_uploader("Upload fisheye images...", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

if uploaded_files:
    results_data = [] # List to store data for the CSV

    st.header("Processing Results")
    
    # Progress bar for better UX
    progress_bar = st.progress(0)
    
    for i, uploaded_file in enumerate(uploaded_files):
        # Save temp file
        temp_path = f"temp_{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        try:
            # Run Algorithms
            res_rayman = SVF.calVF_rayman(temp_path, (resize_dim, resize_dim))[0]
            res_rayman_p = SVF.calVF_rayman_p(temp_path, (resize_dim, resize_dim))[0]
            res_jw = SVF.calVF_JW1984(temp_path, (resize_dim, resize_dim), ring_no=ring_num)[0]

            # Store in list
            results_data.append({
                "Filename": uploaded_file.name,
                "Rayman_SVF": round(res_rayman, 4),
                "Calibrated_Rayman": round(res_rayman_p, 4),
                "JW1984": round(res_jw, 4)
            })

        except Exception as e:
            st.error(f"Error processing {uploaded_file.name}: {e}")
        
        # Cleanup temp file immediately
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
        # Update progress
        progress_bar.progress((i + 1) / len(uploaded_files))

    # --- 4. DISPLAY SUMMARY TABLE ---
    df = pd.DataFrame(results_data)
    st.subheader("Summary Table")
    st.dataframe(df, use_container_width=True)

    # --- 5. DOWNLOAD CSV REPORT ---
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Results as CSV",
        data=csv,
        file_name="SVF_Results_Report.csv",
        mime="text/csv",
    )