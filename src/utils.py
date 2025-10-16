import csv
import os
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Tuple, List
from src.validators import LeadValidator

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


def validate_and_filter_leads(leads: list, db_path: str = None, strict: bool = False) -> Tuple[List[dict], List[dict]]:
    """
    Validate leads and separate valid from invalid ones
    Returns: (valid_leads, invalid_leads_with_reasons)
    """
    validator = LeadValidator(db_path)

    valid_leads = []
    invalid_leads = []

    print(f"\n🔍 Validating {len(leads)} leads...")

    for lead in leads:
        is_valid, issues = validator.is_valid_lead(lead, strict=strict)

        if is_valid:
            valid_leads.append(lead)
        else:
            invalid_leads.append({
                'lead': lead,
                'issues': issues
            })

    # Print summary
    print(f"✅ Valid leads: {len(valid_leads)}")
    print(f"❌ Invalid leads: {len(invalid_leads)}")

    if invalid_leads and len(invalid_leads) <= 5:
        print("\n⚠️  Invalid lead details:")
        for item in invalid_leads:
            print(f"   • {item['lead'].get('name', 'Unknown')}")
            for issue in item['issues']:
                print(f"     - {issue}")

    return valid_leads, invalid_leads


def enrich_lead_with_validation_flags(lead: dict, db_path: str = None) -> dict:
    """
    Add validation flags and enriched data to a lead
    Useful for exporting leads with quality indicators
    """
    validator = LeadValidator(db_path)
    return validator.enrich_lead_data(lead)
