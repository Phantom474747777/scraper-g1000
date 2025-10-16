import sqlite3
import sys

db_path = 'profiles/crittercaptures/leads_tracker.db'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=" * 60)
print("DATABASE INTEGRITY CHECK")
print("=" * 60)

# Total leads
cursor.execute('SELECT COUNT(*) FROM leads')
print(f"\nTotal leads in DB: {cursor.fetchone()[0]}")

# Valid leads (with phone)
cursor.execute('SELECT COUNT(*) FROM leads WHERE phone NOT IN ("N/A", "") AND phone IS NOT NULL')
print(f"Valid leads (with phone): {cursor.fetchone()[0]}")

# Status breakdown
print("\n--- STATUS BREAKDOWN ---")
cursor.execute('SELECT COALESCE(status, "NULL") as status, COUNT(*) FROM leads WHERE phone NOT IN ("N/A", "") AND phone IS NOT NULL GROUP BY status')
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]}")

# Category breakdown
print("\n--- CATEGORY BREAKDOWN ---")
cursor.execute('SELECT COALESCE(category, "NULL") as cat, COUNT(*) FROM leads WHERE phone NOT IN ("N/A", "") AND phone IS NOT NULL GROUP BY category ORDER BY COUNT(*) DESC')
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]}")

# ZIP breakdown
print("\n--- ZIP BREAKDOWN (Top 10) ---")
cursor.execute('SELECT COALESCE(zip_code, "NULL") as zip, COUNT(*) FROM leads WHERE phone NOT IN ("N/A", "") AND phone IS NOT NULL GROUP BY zip_code ORDER BY COUNT(*) DESC LIMIT 10')
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]}")

# Check for NULL categories
cursor.execute('SELECT COUNT(*) FROM leads WHERE category IS NULL AND phone NOT IN ("N/A", "") AND phone IS NOT NULL')
null_cats = cursor.fetchone()[0]
print(f"\n--- NULL CATEGORIES ---")
print(f"Leads with NULL category: {null_cats}")

# Sample leads with NULL category
if null_cats > 0:
    cursor.execute('SELECT id, name, phone, zip_code FROM leads WHERE category IS NULL AND phone NOT IN ("N/A", "") AND phone IS NOT NULL LIMIT 5')
    print("\nSample leads with NULL category:")
    for row in cursor.fetchall():
        print(f"  ID {row[0]}: {row[1]} | {row[2]} | ZIP {row[3]}")

conn.close()
print("\n" + "=" * 60)
