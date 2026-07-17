import streamlit as st
import numpy as np
import cv2
from PIL import Image

from services.text_detector import detect_text_roi
from services.icon_matcher import match_icon
from utils.draw_utils import draw_boxes

st.set_page_config(page_title="HMI ROI Tool", layout="wide")
st.title("Car 🚗 Cluster HMI - ROI Detection Tool")

def to_cv2(uploaded_file):
    img = Image.open(uploaded_file).convert("RGB")
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

hmi_file = st.file_uploader("Upload Full HMI Screenshot", type=["png", "jpg", "jpeg"])

if hmi_file:
    hmi_img = to_cv2(hmi_file)
    st.write(f"Actual image size loaded: {hmi_img.shape[1]} x {hmi_img.shape[0]} (width x height)")

    tab1, tab2 = st.tabs(["📝 Text ROI", "🖼️ Image ROI (Icon Match)"])

    # ---------------- TEXT ROI TAB ----------------
    with tab1:
        if st.button("Detect Text ROIs"):
            with st.spinner("Running OCR..."):
                results = detect_text_roi(hmi_img)
            st.success(f"Found {len(results)} text regions")

            annotated = draw_boxes(hmi_img, results, color=(0, 255, 0))
            st.image(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB), caption="Detected Text ROIs", use_container_width=True)

            st.subheader("Results (JSON)")
            st.json(results)

    # ---------------- IMAGE ROI TAB ----------------
    with tab2:
        icon_file = st.file_uploader("Upload Icon to Match", type=["png", "jpg", "jpeg"], key="icon")
        threshold = st.slider("Match Confidence Threshold", 0.5, 0.99, 0.75)

        if icon_file and st.button("Find Icon ROI"):
            icon_img = to_cv2(icon_file)
            with st.spinner("Matching icon..."):
                matches = match_icon(hmi_img, icon_img, threshold=threshold)

            if matches:
                st.success(f"Found {len(matches)} match(es)")
                annotated = draw_boxes(hmi_img, matches, color=(255, 0, 0), label_key="confidence")
                st.image(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB), caption="Icon Match ROI", use_container_width=True)
                st.json(matches)
            else:
                st.warning("No match found above threshold. Try lowering it.")