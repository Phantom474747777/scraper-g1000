import sqlite3

conn = sqlite3.connect('profiles/crittercaptures/leads_tracker.db')
cursor = conn.cursor()

# Total
cursor.execute('SELECT COUNT(*) FROM leads')
total = cursor.fetchone()[0]
print(f'Total entries: {total}')

# Junk patterns
junk_count = 0
cursor.execute('SELECT COUNT(*) FROM leads WHERE name LIKE "%![%" OR name LIKE "%[Website%" OR name LIKE "%About Search%" OR name LIKE "%[Next]%"')
junk_count = cursor.fetchone()[0]

# Valid leads
cursor.execute('SELECT COUNT(*) FROM leads WHERE phone NOT IN ("N/A", "") AND phone IS NOT NULL AND name NOT LIKE "%![%" AND name NOT LIKE "%[Website%" AND name NOT LIKE "%About Search%"')
valid = cursor.fetchone()[0]

print(f'Valid leads (with phone, clean name): {valid}')
print(f'Junk/incomplete: {total - valid}')
print(f'Quality rate: {valid/total*100:.1f}%')

conn.close()
