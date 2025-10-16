import sqlite3

db_path = 'profiles/crittercaptures/leads_tracker.db'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=" * 60)
print("DATABASE CLEANUP & FIX")
print("=" * 60)

# 1. Delete junk leads with NULL category or NULL zip
print("\n[1] Removing junk leads with NULL category or NULL zip...")
cursor.execute('SELECT COUNT(*) FROM leads WHERE category IS NULL OR zip_code IS NULL')
junk_count = cursor.fetchone()[0]
print(f"    Found {junk_count} junk leads")

cursor.execute('DELETE FROM leads WHERE category IS NULL OR zip_code IS NULL')
conn.commit()
print(f"    [OK] Deleted {junk_count} junk leads")

# 2. Normalize category names
print("\n[2] Normalizing category names...")

# Property Management variations
cursor.execute('UPDATE leads SET category = "Property Managers" WHERE category IN ("Property Management Companies", "HOA Management", "Apartment Complexes")')
normalized = cursor.rowcount
conn.commit()
print(f"    [OK] Normalized {normalized} Property Management variations")

# 3. Verify all statuses are set
print("\n[3] Ensuring all leads have a status...")
cursor.execute('UPDATE leads SET status = "New" WHERE status IS NULL')
status_fixed = cursor.rowcount
conn.commit()
print(f"    [OK] Fixed {status_fixed} NULL statuses")

# 4. Final counts
print("\n[4] Final database stats:")
cursor.execute('SELECT COUNT(*) FROM leads WHERE phone NOT IN ("N/A", "") AND phone IS NOT NULL')
valid = cursor.fetchone()[0]
print(f"    Total valid leads: {valid}")

cursor.execute('SELECT COUNT(DISTINCT category) FROM leads WHERE phone NOT IN ("N/A", "") AND phone IS NOT NULL')
categories = cursor.fetchone()[0]
print(f"    Unique categories: {categories}")

cursor.execute('SELECT COUNT(DISTINCT zip_code) FROM leads WHERE phone NOT IN ("N/A", "") AND phone IS NOT NULL')
zips = cursor.fetchone()[0]
print(f"    Unique ZIP codes: {zips}")

# 5. Show category breakdown
print("\n[5] Updated category breakdown:")
cursor.execute('SELECT category, COUNT(*) FROM leads WHERE phone NOT IN ("N/A", "") AND phone IS NOT NULL GROUP BY category ORDER BY COUNT(*) DESC')
for row in cursor.fetchall():
    print(f"    {row[0]}: {row[1]}")

conn.close()
print("\n" + "=" * 60)
print("[DONE] DATABASE CLEANUP COMPLETE")
print("=" * 60)
