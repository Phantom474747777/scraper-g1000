import sqlite3
import hashlib
from datetime import datetime
from typing import Optional
import os

class LeadsDatabase:
    """Persistent database for tracking scraped leads and preventing duplicates"""

    def __init__(self, db_path: str = "data/leads_tracker.db"):
        self.db_path = db_path
        # Ensure the data directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_database()

    def _init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Table for tracking all scraped leads
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                business_hash TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                address TEXT,
                phone TEXT,
                email TEXT,
                website TEXT,
                zip_code TEXT,
                location TEXT,
                scraped_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                source_file TEXT
            )
        ''')

        # Table for tracking scraped zip+category combos (prevents re-scraping)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scraped_combos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                zip_code TEXT NOT NULL,
                category TEXT NOT NULL,
                scraped_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                lead_number INTEGER NOT NULL,
                UNIQUE(zip_code, category)
            )
        ''')

        # Index for fast duplicate checking
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_business_hash
            ON leads(business_hash)
        ''')

        # Index for searching by location/zip
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_location
            ON leads(location, zip_code)
        ''')

        conn.commit()
        conn.close()

    def _generate_hash(self, name: str, phone: str, address: str) -> str:
        """Generate a unique hash for a business based on name + phone + address"""
        # Normalize the data (lowercase, strip whitespace)
        normalized = f"{name.lower().strip()}|{phone.strip()}|{address.lower().strip()}"
        return hashlib.md5(normalized.encode()).hexdigest()

    def is_duplicate(self, name: str, phone: str, address: str) -> bool:
        """Check if a business already exists in the database"""
        business_hash = self._generate_hash(name, phone, address)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            'SELECT COUNT(*) FROM leads WHERE business_hash = ?',
            (business_hash,)
        )
        count = cursor.fetchone()[0]
        conn.close()

        return count > 0

    def add_lead(self, name: str, address: str, phone: str,
                 email: Optional[str] = None, website: Optional[str] = None,
                 zip_code: Optional[str] = None, category: Optional[str] = None,
                 location: Optional[str] = None, source_file: Optional[str] = None) -> bool:
        """
        Add a lead to the database if it doesn't already exist
        Returns True if added, False if duplicate
        """
        business_hash = self._generate_hash(name, phone, address)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Check if category column exists, if not add it
        cursor.execute("PRAGMA table_info(leads)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'category' not in columns:
            cursor.execute('ALTER TABLE leads ADD COLUMN category TEXT')
            conn.commit()

        try:
            cursor.execute('''
                INSERT INTO leads
                (business_hash, name, address, phone, email, website, zip_code, category, location, source_file)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (business_hash, name, address, phone, email, website, zip_code, category, location, source_file))

            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            # Duplicate entry
            conn.close()
            return False

    def get_leads_by_location(self, location: str, zip_code: Optional[str] = None):
        """Retrieve all leads for a specific location"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if zip_code:
            cursor.execute(
                'SELECT * FROM leads WHERE location = ? AND zip_code = ?',
                (location, zip_code)
            )
        else:
            cursor.execute(
                'SELECT * FROM leads WHERE location = ?',
                (location,)
            )

        results = cursor.fetchall()
        conn.close()
        return results

    def get_total_leads(self) -> int:
        """Get total number of unique leads in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM leads')
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def is_combo_scraped(self, zip_code: str, category: str):
        """Check if a zip+category combo has already been scraped
        Returns (is_scraped, scraped_date, lead_number) tuple
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            'SELECT scraped_date, lead_number FROM scraped_combos WHERE zip_code = ? AND category = ?',
            (zip_code, category)
        )
        result = cursor.fetchone()
        conn.close()

        if result:
            return (True, result[0], result[1])
        return (False, None, None)

    def mark_combo_scraped(self, zip_code: str, category: str) -> int:
        """Mark a zip+category combo as scraped and return its lead number"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get the next lead number
        cursor.execute('SELECT MAX(lead_number) FROM scraped_combos')
        max_lead = cursor.fetchone()[0]
        next_lead_number = (max_lead or 0) + 1

        try:
            cursor.execute('''
                INSERT INTO scraped_combos (zip_code, category, lead_number)
                VALUES (?, ?, ?)
            ''', (zip_code, category, next_lead_number))
            conn.commit()
            conn.close()
            return next_lead_number
        except sqlite3.IntegrityError:
            # Already exists, get existing number
            cursor.execute(
                'SELECT lead_number FROM scraped_combos WHERE zip_code = ? AND category = ?',
                (zip_code, category)
            )
            lead_number = cursor.fetchone()[0]
            conn.close()
            return lead_number

    def get_stats(self):
        """Get statistics about the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Total leads
        cursor.execute('SELECT COUNT(*) FROM leads')
        total = cursor.fetchone()[0]

        # Leads by location
        cursor.execute('''
            SELECT location, COUNT(*) as count
            FROM leads
            GROUP BY location
            ORDER BY count DESC
        ''')
        by_location = cursor.fetchall()

        # Leads by zip code
        cursor.execute('''
            SELECT zip_code, COUNT(*) as count
            FROM leads
            WHERE zip_code IS NOT NULL
            GROUP BY zip_code
            ORDER BY count DESC
            LIMIT 10
        ''')
        by_zip = cursor.fetchall()

        conn.close()

        return {
            'total_leads': total,
            'by_location': by_location,
            'top_zip_codes': by_zip
        }
