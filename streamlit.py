import streamlit as st
import cv2
import numpy as np
import os
import io
import zipfile
import pandas as pd
from SVF_img_calculator import SVF_img_cal as SVF

st.set_page_config(page_title="SVF Batch Calculator", layout="wide")

# Initialize session state for results if it doesn't exist
if 'results_data' not in st.session_state:
    st.session_state.results_data = []

st.title("🏙️ SVF Calculator")
st.write("Upload fisheye images (Black & White) to calculate Sky View Factors in bulk.")
st.write("The image should contain only black and white pixels.")

# --- 1. SIDEBAR: EXAMPLES & SETTINGS ---
st.sidebar.header("Example SVF Images")
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

st.sidebar.divider()
st.sidebar.header("Calculation Settings")
resize_dim = st.sidebar.slider("Resize Dimensions", 128, 1024, 512, step=128)
ring_num = st.sidebar.number_input("JW1984 Ring Number", min_value=1, max_value=100, value=10)

if st.sidebar.button("🗑️ Clear All Results"):
    st.session_state.results_data = []
    st.rerun()

# --- 2. BATCH UPLOADER ---
uploaded_files = st.file_uploader("Upload fisheye images...", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

if uploaded_files:
    st.header("Processing New Uploads")
    progress_bar = st.progress(0)
    
    for i, uploaded_file in enumerate(uploaded_files):
        # Check if this file is already in our results to avoid duplicates
        if any(d['Filename'] == uploaded_file.name for d in st.session_state.results_data):
            continue

        temp_path = f"temp_{uploaded_file.name}"
        # file_bytes = uploaded_file.getvalue()
        
        # with open(temp_path, "wb") as f:
        #     f.write(file_bytes)

        try:
            # Run Algorithms (extracting [0] from returned tuple)
            res_rayman = SVF.calVF_rayman(temp_path, (resize_dim, resize_dim))[0]
            res_rayman_p = SVF.calVF_rayman_p(temp_path, (resize_dim, resize_dim))[0]
            res_jw = SVF.calVF_JW1984(temp_path, (resize_dim, resize_dim), ring_no=ring_num)[0]

            # Append to session state
            st.session_state.results_data.append({
                # "Preview": file_bytes,
                "Filename": uploaded_file.name,
                "Rayman_SVF": round(res_rayman, 4),
                "Calibrated_Rayman": round(res_rayman_p, 4),
                "JW1984": round(res_jw, 4)
            })

        except Exception as e:
            st.error(f"Error processing {uploaded_file.name}: {e}")
        
        if os.path.exists(temp_path):
            os.remove(temp_path)
        progress_bar.progress((i + 1) / len(uploaded_files))

# --- 3. DISPLAY SUMMARY TABLE ---
if st.session_state.results_data:
    df = pd.DataFrame(st.session_state.results_data)
    
    st.subheader("Summary Table")
    st.dataframe(
        df,
        column_config={
            "Preview": st.column_config.ImageColumn("Preview", help="Image Thumbnail"),
            "Rayman_SVF": st.column_config.NumberColumn(format="%.4f"),
            "Calibrated_Rayman": st.column_config.NumberColumn(format="%.4f"),
            "JW1984": st.column_config.NumberColumn(format="%.4f"),
        },
        use_container_width=True,
        hide_index=True,
    )

    # --- 4. DOWNLOAD CSV REPORT ---
    csv_df = df.drop(columns=["Preview"])
    csv = csv_df.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="📥 Download Results as CSV",
        data=csv,
        file_name="SVF_Results_Report.csv",
        mime="text/csv",
    )

st.divider()
st.markdown("By [Yilun Li](https://github.com/Yilun595/SVF_image_calculator)")