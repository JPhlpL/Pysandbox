import os
import time
import pandas as pd
from datetime import datetime
from transformers import pipeline
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

# Load the model and pipeline
pipe = pipeline("image-segmentation", model="briaai/RMBG-1.4", trust_remote_code=True)

input_folder = "samples/input"
output_folder = "samples/output"

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Prepare data collection for Excel
data = []

def process_image(filename):
    if filename.endswith((".jpg", ".jpeg", ".png")):  # Add more extensions if needed
        input_path = os.path.join(input_folder, filename)
        
        start_time = datetime.now()

        # Perform image segmentation
        pillow_image = pipe(input_path)  # Applies mask on input and returns a pillow image
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Create output filename
        base, ext = os.path.splitext(filename)
        output_path_image = os.path.join(output_folder, f"{base}_output{ext}")
        
        # Convert to RGB if saving as JPEG
        if ext.lower() in [".jpg", ".jpeg"]:
            pillow_image = pillow_image.convert("RGB")
        pillow_image.save(output_path_image)
        
        # Record data for Excel
        data.append({
            "Filename": filename,
            "Start Time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "End Time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
            "Duration (seconds)": duration
        })

# Use ThreadPoolExecutor to process images in parallel
with ThreadPoolExecutor() as executor:
    filenames = [f for f in os.listdir(input_folder) if f.endswith((".jpg", ".jpeg", ".png"))]
    executor.map(process_image, filenames)

# Save data to Excel
df = pd.DataFrame(data)
excel_path = os.path.join(output_folder, "processing_log.xlsx")
df.to_excel(excel_path, index=False)

print("Batch processing completed and log saved.")
