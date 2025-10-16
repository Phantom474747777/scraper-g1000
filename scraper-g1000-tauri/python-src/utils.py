import csv
import os
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

def is_duplicated(record: str, seen_names: set) -> bool:
    return record in seen_names

def generate_filename(location: str, zip_code: Optional[str] = None,
                     business_type: Optional[str] = None) -> str:
    """
    Generate a descriptive filename with timestamp, location, and optional filters

    Example: critter_leads_denver_fl_32456_2025-10-14_143022.csv
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")

    # Clean location name (remove spaces, special chars)
    clean_location = location.lower().replace(" ", "_").replace(",", "")

    parts = ["critter_leads", clean_location]

    if zip_code:
        parts.append(zip_code)

    if business_type:
        clean_type = business_type.lower().replace(" ", "_")
        parts.append(clean_type)

    parts.append(timestamp)

    filename = "_".join(parts) + ".csv"
    return filename

def save_data_to_csv(records: list, data_struct: BaseModel, filename: str,
                     output_dir: str = "data/leads"):
    """
    Save records to CSV with organized directory structure
    """
    if not records:
        print("No records to save.")
        return None

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Full path
    filepath = os.path.join(output_dir, filename)

    # Use field names from the Pydantic data model
    fieldnames = data_struct.model_fields.keys()

    with open(filepath, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"✓ Saved {len(records)} records to '{filepath}'.")
    return filepath
