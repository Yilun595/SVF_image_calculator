import streamlit as st
import cv2
import numpy as np
import os
from SVF_img_calculator import SVF_img_cal as SVF

st.set_page_config(page_title="SVF Calculator", layout="wide")

st.title("🏙️ Sky View Factor (SVF) Calculator")
st.write("Calculate SVF using Rayman, Calibrated Rayman, and JW1984 algorithms.")

# 1. Sidebar for Settings
st.sidebar.header("Calculation Settings")
resize_dim = st.sidebar.slider("Resize Dimensions", 128, 1024, 512, step=128)
ring_num = st.sidebar.number_input("JW1984 Ring Number", min_value=1, max_value=100, value=10)

# 2. File Uploader
uploaded_file = st.file_uploader("Upload a fisheye image (01.png, 03.png, etc.)", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    # Save temp file for the package to read
    temp_path = "temp_svf_image.png"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Display Image
    col_img, col_res = st.columns([1, 1])
    
    with col_img:
        st.image(uploaded_file, caption=f"Original Image: {uploaded_file.name}", use_container_width=True)
        # Show shape like your print(img.shape) statement
        img_cv = cv2.imread(temp_path)
        st.write(f"Image Shape: `{img_cv.shape}`")

    with col_res:
        st.header("Results")
        
        with st.spinner('Running algorithms...'):
            # Run the three functions from your package
            # Note: I'm assuming these return the SVF value. 
            # If they only print to console, we'd need to wrap them, 
            # but usually, these return a float.
            
            res_rayman = SVF.calVF_rayman(temp_path, (resize_dim, resize_dim))
            res_rayman_p = SVF.calVF_rayman_p(temp_path, (resize_dim, resize_dim))
            res_jw = SVF.calVF_JW1984(temp_path, (resize_dim, resize_dim), ring_no=ring_num)

            # Display as attractive metrics
            st.metric("Rayman SVF", f"{res_rayman:.4f}")
            st.metric("Calibrated Rayman (p)", f"{res_rayman_p:.4f}")
            st.metric("JW1984 Algorithm", f"{res_jw:.4f}")

    # 3. Cleanup
    if os.path.exists(temp_path):
        os.remove(temp_path)

st.divider()
st.markdown("Developed by [Yilun595](https://github.com/Yilun595/SVF_image_calculator)")