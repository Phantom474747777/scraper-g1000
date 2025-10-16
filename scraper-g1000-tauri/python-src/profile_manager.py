"""
Profile Management System for Scraper G1000
Allows multiple business profiles with separate databases and settings
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path


class Profile:
    """Represents a single business profile"""

    def __init__(self, profile_data: Dict):
        self.name = profile_data.get('name', 'Unnamed Profile')
        self.icon = profile_data.get('icon', '📊')
        self.business_type = profile_data.get('business_type', '')
        self.default_city = profile_data.get('default_city', '')
        self.default_state = profile_data.get('default_state', '')
        self.default_radius = profile_data.get('default_radius', 50)
        self.categories = profile_data.get('categories', [])
        self.created_at = profile_data.get('created_at', datetime.now().isoformat())
        self.total_leads = profile_data.get('total_leads', 0)
        self.profile_id = profile_data.get('profile_id', self.name.lower().replace(' ', '_'))

    def to_dict(self) -> Dict:
        """Convert profile to dictionary"""
        return {
            'profile_id': self.profile_id,
            'name': self.name,
            'icon': self.icon,
            'business_type': self.business_type,
            'default_city': self.default_city,
            'default_state': self.default_state,
            'default_radius': self.default_radius,
            'categories': self.categories,
            'created_at': self.created_at,
            'total_leads': self.total_leads
        }

    def get_database_path(self) -> str:
        """Get path to this profile's database"""
        base_dir = Path('profiles') / self.profile_id
        base_dir.mkdir(parents=True, exist_ok=True)
        return str(base_dir / 'leads_tracker.db')

    def get_data_dir(self) -> Path:
        """Get data directory for this profile"""
        data_dir = Path('profiles') / self.profile_id / 'data'
        data_dir.mkdir(parents=True, exist_ok=True)
        return data_dir


class ProfileManager:
    """Manages all business profiles"""

    def __init__(self, profiles_dir: str = 'profiles'):
        self.profiles_dir = Path(profiles_dir)
        self.profiles_dir.mkdir(exist_ok=True)
        self.profiles_file = self.profiles_dir / 'profiles.json'
        self.profiles: Dict[str, Profile] = {}
        self._load_profiles()

    def _load_profiles(self):
        """Load all profiles from disk"""
        if self.profiles_file.exists():
            with open(self.profiles_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for profile_data in data.get('profiles', []):
                    profile = Profile(profile_data)
                    self.profiles[profile.profile_id] = profile
        else:
            # Create default CritterCaptures profile on first run
            self._create_default_profile()

    def _create_default_profile(self):
        """Create the default CritterCaptures profile"""
        default_profile = Profile({
            'profile_id': 'crittercaptures',
            'name': 'CritterCaptures',
            'icon': '🦝',
            'business_type': 'Wildlife Removal',
            'default_city': 'Dover',
            'default_state': 'FL',
            'default_radius': 50,
            'categories': [
                'Real Estate Agents',
                'Property Managers',
                'Home Inspectors',
                'Construction Companies',
                'Roofing Contractors',
                'HVAC Services',
                'Plumbing Companies',
                'Landscaping Companies',
                'Cleaning Services'
            ],
            'created_at': datetime.now().isoformat(),
            'total_leads': 0
        })

        self.profiles['crittercaptures'] = default_profile
        self._save_profiles()

        # Migrate existing data if it exists
        self._migrate_existing_data(default_profile)

    def _migrate_existing_data(self, profile: Profile):
        """Migrate existing CritterCaptures data to profile structure"""
        old_db = Path('data/leads_tracker.db')
        old_tracking = Path('data/used_zips.json')

        profile_dir = Path('profiles') / profile.profile_id
        profile_dir.mkdir(parents=True, exist_ok=True)

        # Move database
        if old_db.exists():
            new_db = profile_dir / 'leads_tracker.db'
            if not new_db.exists():
                import shutil
                shutil.copy2(old_db, new_db)
                print(f"[MIGRATE] Moved database to {new_db}")

        # Move tracking
        if old_tracking.exists():
            new_tracking = profile_dir / 'used_zips.json'
            if not new_tracking.exists():
                import shutil
                shutil.copy2(old_tracking, new_tracking)
                print(f"[MIGRATE] Moved tracking to {new_tracking}")

        # Move CSV files
        old_data_dir = Path('data')
        if old_data_dir.exists():
            for csv_file in old_data_dir.glob('*.csv'):
                new_csv = profile_dir / 'data' / csv_file.name
                new_csv.parent.mkdir(parents=True, exist_ok=True)
                if not new_csv.exists():
                    import shutil
                    shutil.copy2(csv_file, new_csv)
                    print(f"[MIGRATE] Moved {csv_file.name}")

    def _save_profiles(self):
        """Save all profiles to disk"""
        data = {
            'profiles': [profile.to_dict() for profile in self.profiles.values()]
        }

        with open(self.profiles_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def create_profile(self, name: str, icon: str, business_type: str,
                      default_city: str, default_state: str,
                      categories: List[str]) -> Profile:
        """Create a new profile"""
        profile_id = name.lower().replace(' ', '_')

        profile = Profile({
            'profile_id': profile_id,
            'name': name,
            'icon': icon,
            'business_type': business_type,
            'default_city': default_city,
            'default_state': default_state,
            'default_radius': 50,
            'categories': categories,
            'created_at': datetime.now().isoformat(),
            'total_leads': 0
        })

        self.profiles[profile_id] = profile
        self._save_profiles()

        # Create profile directory structure
        profile_dir = Path('profiles') / profile_id
        profile_dir.mkdir(parents=True, exist_ok=True)
        (profile_dir / 'data').mkdir(exist_ok=True)

        return profile

    def get_profile(self, profile_id: str) -> Optional[Profile]:
        """Get a profile by ID"""
        return self.profiles.get(profile_id)

    def get_all_profiles(self) -> List[Profile]:
        """Get all profiles"""
        return list(self.profiles.values())

    def delete_profile(self, profile_id: str):
        """Delete a profile"""
        if profile_id in self.profiles:
            del self.profiles[profile_id]
            self._save_profiles()

    def update_profile_leads(self, profile_id: str, count: int):
        """Update total leads count for a profile"""
        if profile_id in self.profiles:
            self.profiles[profile_id].total_leads = count
            self._save_profiles()


if __name__ == "__main__":
    # Test profile system
    pm = ProfileManager()

    print("\n[TEST] Profile System")
    print("=" * 60)

    profiles = pm.get_all_profiles()
    print(f"\nTotal profiles: {len(profiles)}")

    for profile in profiles:
        print(f"\n[{profile.profile_id}] {profile.name}")
        print(f"  Type: {profile.business_type}")
        print(f"  Default: {profile.default_city}, {profile.default_state}")
        print(f"  Categories: {len(profile.categories)}")
        print(f"  Total Leads: {profile.total_leads}")
        print(f"  Database: {profile.get_database_path()}")

    print("\n[SUCCESS] Profile system working!")
