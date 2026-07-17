# Ford Cluster HMI - ROI Detection Tool

A Streamlit-based tool to upload a full HMI (cluster) screenshot and detect:
1. **Text ROIs** – full text blocks with bounding box coordinates
2. **Image ROIs** – match an uploaded icon against the HMI and return its location

---

## Features
- Upload full HMI screenshot (PNG/JPG)
- **Text ROI tab**: runs OCR and returns all detected text with bounding boxes (x, y, width, height)
- **Image ROI tab**: upload an icon, tool finds all matching locations on the HMI using template matching
- Visual overlay of detected boxes on the image
- JSON output for downstream automation/testing use

---

## Project Structure