"""
Backfill city names for all existing leads in the database
Looks up city name from ZIP code using pgeocode
"""
import sqlite3
import pgeocode
from pathlib import Path

# Database path
DB_PATH = "profiles/crittercaptures/leads_tracker.db"

def backfill_cities():
    """Update all leads with missing city names"""

    if not Path(DB_PATH).exists():
        print(f"[ERROR] Database not found: {DB_PATH}")
        return

    print(f"[Backfill] Opening database: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get all leads with NULL or empty location
    cursor.execute('''
        SELECT id, zip_code
        FROM leads
        WHERE location IS NULL OR location = ''
    ''')

    leads_to_update = cursor.fetchall()
    print(f"[Backfill] Found {len(leads_to_update)} leads without city names")

    if len(leads_to_update) == 0:
        print("[Backfill] All leads already have city names!")
        conn.close()
        return

    # Initialize pgeocode
    nomi = pgeocode.Nominatim('US')

    # Update each lead
    updated_count = 0
    failed_count = 0

    for lead_id, zip_code in leads_to_update:
        try:
            # Look up city name from ZIP
            zip_data = nomi.query_postal_code(zip_code)

            if zip_data is not None and not zip_data.isna().all():
                city_name = str(zip_data.place_name) if hasattr(zip_data, 'place_name') else None

                if city_name and city_name != 'nan':
                    # Update the lead
                    cursor.execute('''
                        UPDATE leads
                        SET location = ?
                        WHERE id = ?
                    ''', (city_name, lead_id))

                    updated_count += 1

                    if updated_count % 100 == 0:
                        print(f"[Backfill] Updated {updated_count} leads...")
                        conn.commit()
                else:
                    print(f"[WARNING] No city found for ZIP {zip_code} (ID: {lead_id})")
                    failed_count += 1
            else:
                print(f"[WARNING] Invalid ZIP data for {zip_code} (ID: {lead_id})")
                failed_count += 1

        except Exception as e:
            print(f"[ERROR] Failed to update lead {lead_id} (ZIP: {zip_code}): {e}")
            failed_count += 1

    # Final commit
    conn.commit()
    conn.close()

    print(f"\n[Backfill] COMPLETE!")
    print(f"  ✓ Updated: {updated_count} leads")
    print(f"  ✗ Failed: {failed_count} leads")
    print(f"  Total processed: {len(leads_to_update)} leads")

if __name__ == "__main__":
    print("=" * 60)
    print("  CritterCaptures - City Name Backfill")
    print("=" * 60)
    backfill_cities()
