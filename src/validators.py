"""
Data validation and quality checks for lead generation
"""
import re
import sqlite3
from typing import Optional, Tuple
from difflib import SequenceMatcher
from urllib.parse import urlparse


class LeadValidator:
    """Validates and enriches lead data to ensure quality"""

    def __init__(self, db_path: str = None):
        self.db_path = db_path

        # Common generic email prefixes to flag
        self.generic_emails = [
            'info', 'contact', 'hello', 'admin', 'support',
            'sales', 'service', 'office', 'mail', 'general'
        ]

        # Suspicious phone patterns
        self.fake_phone_patterns = [
            r'^0{10}$',  # 0000000000
            r'^1{10}$',  # 1111111111
            r'^(\d)\1{9}$',  # Any repeating digit
            r'^123-?456-?7890$',  # 123-456-7890
            r'^555-?555-?5555$',  # 555-555-5555
        ]

    def validate_phone(self, phone: str) -> Tuple[bool, Optional[str]]:
        """
        Validate US phone number format
        Returns: (is_valid, reason_if_invalid)
        """
        if not phone or phone.strip() == "" or phone == "N/A":
            return False, "No phone number provided"

        # Remove all non-digit characters for validation
        digits_only = re.sub(r'\D', '', phone)

        # Check if it's 10 digits (US format)
        if len(digits_only) != 10:
            return False, f"Invalid length: {len(digits_only)} digits (expected 10)"

        # Check for fake/suspicious patterns
        for pattern in self.fake_phone_patterns:
            if re.match(pattern, digits_only):
                return False, f"Suspicious pattern detected: {phone}"

        # Check if area code is valid (not starting with 0 or 1)
        if digits_only[0] in ['0', '1']:
            return False, f"Invalid area code: {digits_only[:3]}"

        return True, None

    def validate_email(self, email: str) -> Tuple[bool, Optional[str], bool]:
        """
        Validate email format and check if it's generic
        Returns: (is_valid, reason_if_invalid, is_generic)
        """
        if not email or email.strip() == "" or email == "N/A":
            return False, "No email provided", False

        # Basic email regex
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if not re.match(email_pattern, email):
            return False, "Invalid email format", False

        # Check if it's a generic email
        email_prefix = email.split('@')[0].lower()
        is_generic = any(generic in email_prefix for generic in self.generic_emails)

        return True, None, is_generic

    def validate_website(self, website: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Validate website URL and extract domain
        Returns: (is_valid, reason_if_invalid, domain)
        """
        if not website or website.strip() == "" or website == "N/A":
            return False, "No website provided", None

        # Add http:// if missing
        if not website.startswith(('http://', 'https://')):
            website = 'https://' + website

        try:
            parsed = urlparse(website)
            domain = parsed.netloc or parsed.path.split('/')[0]

            if not domain or '.' not in domain:
                return False, "Invalid domain format", None

            return True, None, domain

        except Exception as e:
            return False, f"URL parsing error: {str(e)}", None

    def check_near_duplicate(self, name: str, threshold: float = 0.85) -> Optional[Tuple[int, str, float]]:
        """
        Check for near-duplicate business names using fuzzy matching
        Returns: (lead_id, existing_name, similarity_score) if found, None otherwise
        """
        if not self.db_path:
            return None

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get all existing business names
        cursor.execute('SELECT id, name FROM leads')
        existing_leads = cursor.fetchall()
        conn.close()

        # Normalize the input name
        normalized_name = name.lower().strip()

        # Check similarity with each existing name
        for lead_id, existing_name in existing_leads:
            normalized_existing = existing_name.lower().strip()

            # Calculate similarity ratio
            similarity = SequenceMatcher(None, normalized_name, normalized_existing).ratio()

            if similarity >= threshold and normalized_name != normalized_existing:
                return (lead_id, existing_name, similarity)

        return None

    def standardize_address(self, address: str) -> str:
        """
        Standardize address format (light normalization)
        """
        if not address or address == "N/A":
            return address

        # Common abbreviations to standardize
        replacements = {
            r'\bSt\.?\b': 'Street',
            r'\bAve\.?\b': 'Avenue',
            r'\bBlvd\.?\b': 'Boulevard',
            r'\bRd\.?\b': 'Road',
            r'\bDr\.?\b': 'Drive',
            r'\bLn\.?\b': 'Lane',
            r'\bCt\.?\b': 'Court',
            r'\bPl\.?\b': 'Place',
            r'\bPkwy\.?\b': 'Parkway',
            r'\bN\.?\b': 'North',
            r'\bS\.?\b': 'South',
            r'\bE\.?\b': 'East',
            r'\bW\.?\b': 'West',
        }

        standardized = address
        for pattern, replacement in replacements.items():
            standardized = re.sub(pattern, replacement, standardized, flags=re.IGNORECASE)

        return standardized.strip()

    def enrich_lead_data(self, lead_data: dict) -> dict:
        """
        Enrich lead data with validation flags and extracted info
        """
        enriched = lead_data.copy()

        # Validate phone
        phone_valid, phone_reason = self.validate_phone(lead_data.get('phone', ''))
        enriched['phone_valid'] = phone_valid
        enriched['phone_validation_reason'] = phone_reason

        # Validate email
        email_valid, email_reason, email_is_generic = self.validate_email(lead_data.get('email', ''))
        enriched['email_valid'] = email_valid
        enriched['email_validation_reason'] = email_reason
        enriched['email_is_generic'] = email_is_generic

        # Validate website and extract domain
        website_valid, website_reason, domain = self.validate_website(lead_data.get('website', ''))
        enriched['website_valid'] = website_valid
        enriched['website_validation_reason'] = website_reason
        enriched['website_domain'] = domain

        # Standardize address
        if 'address' in lead_data:
            enriched['address_standardized'] = self.standardize_address(lead_data['address'])

        # Check for near-duplicates
        if self.db_path:
            near_dup = self.check_near_duplicate(lead_data.get('name', ''))
            if near_dup:
                enriched['near_duplicate'] = {
                    'lead_id': near_dup[0],
                    'existing_name': near_dup[1],
                    'similarity': near_dup[2]
                }

        return enriched

    def is_valid_lead(self, lead_data: dict, strict: bool = False) -> Tuple[bool, list]:
        """
        Check if a lead meets minimum quality standards
        Returns: (is_valid, list_of_issues)

        Args:
            strict: If True, require valid email and website too
        """
        issues = []

        # Must have name
        if not lead_data.get('name') or lead_data.get('name') == 'N/A':
            issues.append("Missing business name")

        # Must have valid phone (critical)
        phone_valid, phone_reason = self.validate_phone(lead_data.get('phone', ''))
        if not phone_valid:
            issues.append(f"Phone: {phone_reason}")

        if strict:
            # Strict mode: require valid email
            email_valid, email_reason, _ = self.validate_email(lead_data.get('email', ''))
            if not email_valid:
                issues.append(f"Email: {email_reason}")

            # Strict mode: require valid website
            website_valid, website_reason, _ = self.validate_website(lead_data.get('website', ''))
            if not website_valid:
                issues.append(f"Website: {website_reason}")

        return len(issues) == 0, issues


def print_validation_report(lead_data: dict, validator: LeadValidator):
    """
    Print a detailed validation report for a single lead
    """
    print("\n" + "="*60)
    print(f"📋 Validation Report: {lead_data.get('name', 'Unknown')}")
    print("="*60)

    enriched = validator.enrich_lead_data(lead_data)

    # Phone validation
    phone_icon = "✅" if enriched['phone_valid'] else "❌"
    print(f"\n{phone_icon} Phone: {lead_data.get('phone', 'N/A')}")
    if not enriched['phone_valid']:
        print(f"   Issue: {enriched['phone_validation_reason']}")

    # Email validation
    email_icon = "✅" if enriched['email_valid'] else "❌"
    print(f"\n{email_icon} Email: {lead_data.get('email', 'N/A')}")
    if not enriched['email_valid']:
        print(f"   Issue: {enriched['email_validation_reason']}")
    elif enriched['email_is_generic']:
        print(f"   ⚠️  Generic email (info@, contact@, etc.)")

    # Website validation
    website_icon = "✅" if enriched['website_valid'] else "❌"
    print(f"\n{website_icon} Website: {lead_data.get('website', 'N/A')}")
    if not enriched['website_valid']:
        print(f"   Issue: {enriched['website_validation_reason']}")
    elif enriched['website_domain']:
        print(f"   Domain: {enriched['website_domain']}")

    # Near duplicates
    if 'near_duplicate' in enriched:
        dup = enriched['near_duplicate']
        print(f"\n⚠️  Near Duplicate Detected!")
        print(f"   Similar to: {dup['existing_name']}")
        print(f"   Similarity: {dup['similarity']*100:.1f}%")
        print(f"   Existing Lead ID: {dup['lead_id']}")

    # Overall quality
    is_valid, issues = validator.is_valid_lead(lead_data)
    print("\n" + "-"*60)
    if is_valid:
        print("✅ Overall: VALID - Lead meets quality standards")
    else:
        print("❌ Overall: INVALID - Lead has quality issues:")
        for issue in issues:
            print(f"   • {issue}")

    print("="*60 + "\n")
