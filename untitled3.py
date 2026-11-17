import os
import zipfile
import urllib.request
import pandas as pd

# 1. Configuration for your local workspace
workspace_dir = r"C:\Users\ASUS\Desktop\eb_images"
excel_filename = "skus_and_titles.xlsx"
base_url = "https://www.everybodyjewelry.com/customer_images/"
output_report_filename = "sku_image_summary_report.xlsx"

# Set working directory
os.chdir(workspace_dir)
print(f"Current working directory set to: {os.getcwd()}")

# 2. Read the SKUs directly from the first column of your Excel file
try:
    excel_path = os.path.join(workspace_dir, excel_filename)
    
    # Reads the first sheet by default
    df = pd.read_excel(excel_path, sheet_name=0)
    
    # Automatically grabs the very first column (index 0) regardless of its name
    raw_skus = df.iloc[:, 0].dropna().tolist()
    
    print(f"Successfully loaded {len(raw_skus)} SKUs from the first column of '{excel_filename}'.")
except Exception as e:
    print(f"Error reading Excel file: {e}")
    raw_skus = []

valid_extensions = ('.jpg', '.jpeg', '.png', '.webp')
report_data = []

print("\nStarting to download individual SKU ZIP files (using the prefix before '-')...")

for full_sku in raw_skus:
    full_sku_clean = str(full_sku).strip()
    
    # Take ONLY the first part before the hyphen '-' (e.g. NODC01-CAR -> NODC01)
    sku_prefix = full_sku_clean.split('-')[0].strip()
    
    zip_url = f"{base_url}{sku_prefix}.zip"
    zip_filename = f"{sku_prefix}.zip"
    sku_extract_dir = os.path.join(workspace_dir, sku_prefix)
    
    matched_images = []
    
    try:
        # Download individual SKU zip file
        urllib.request.urlretrieve(zip_url, zip_filename)
        
        # Extract into a folder named after the SKU prefix
        os.makedirs(sku_extract_dir, exist_ok=True)
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall(sku_extract_dir)
            
        # Remove the zip file after extraction
        os.remove(zip_filename)
        
        # Scan images inside the folder
        for root, dirs, files in os.walk(sku_extract_dir):
            for file in files:
                if file.lower().endswith(valid_extensions):
                    matched_images.append(file)
        matched_images.sort()
        
    except Exception as e:
        # If download fails or zip doesn't exist on server
        print(f"ZIP not found / failed for: {sku_prefix}.zip")

    report_data.append({
        'Full SKU': full_sku_clean,
        'SKU Prefix (Folder/ZIP)': sku_prefix,
        'Number of Images': len(matched_images),
        'Image Names (with Extensions)': ", ".join(matched_images) if matched_images else "None found"
    })

# 3. Export results to an Excel report
report_df = pd.DataFrame(report_data)
output_path = os.path.join(workspace_dir, output_report_filename)
report_df.to_excel(output_path, index=False)

print(f"\n--- Success! ---")
print(f"Summary report saved at: {output_path}")