"""
Tracking system for used ZIP codes and categories
Stores data in data/used_zips.json
"""
import json
import os
from typing import Dict, List, Set
from datetime import datetime


class ZipTracker:
    """Track which ZIP + category combinations have been scraped"""
    
    def __init__(self, tracking_file: str = "data/used_zips.json"):
        self.tracking_file = tracking_file
        self.data = self._load_data()
    
    def _load_data(self) -> Dict:
        """Load tracking data from JSON file"""
        if os.path.exists(self.tracking_file):
            try:
                with open(self.tracking_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"⚠️  Warning: Could not parse {self.tracking_file}, starting fresh")
                return {}
        return {}
    
    def _save_data(self):
        """Save tracking data to JSON file"""
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.tracking_file), exist_ok=True)
        
        with open(self.tracking_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def is_used(self, zip_code: str, category: str) -> bool:
        """Check if a ZIP + category combination has been used"""
        zip_code = str(zip_code)
        if zip_code not in self.data:
            return False
        return category in self.data[zip_code].get('categories', [])
    
    def mark_used(self, zip_code: str, category: str, leads_count: int = 0, output_file: str = ""):
        """Mark a ZIP + category as used"""
        zip_code = str(zip_code)
        
        if zip_code not in self.data:
            self.data[zip_code] = {
                'categories': [],
                'history': []
            }
        
        # Add category if not already there
        if category not in self.data[zip_code]['categories']:
            self.data[zip_code]['categories'].append(category)
        
        # Add to history
        self.data[zip_code]['history'].append({
            'category': category,
            'scraped_at': datetime.now().isoformat(),
            'leads_found': leads_count,
            'output_file': output_file
        })
        
        self._save_data()
    
    def get_used_categories(self, zip_code: str) -> List[str]:
        """Get list of categories already scraped for a ZIP"""
        zip_code = str(zip_code)
        if zip_code not in self.data:
            return []
        return self.data[zip_code].get('categories', [])
    
    def get_available_categories(self, zip_code: str, all_categories: List[str]) -> List[str]:
        """Get list of categories NOT yet scraped for a ZIP"""
        used = set(self.get_used_categories(zip_code))
        return [cat for cat in all_categories if cat not in used]
    
    def is_zip_fully_used(self, zip_code: str, all_categories: List[str]) -> bool:
        """Check if all categories have been scraped for this ZIP"""
        used = set(self.get_used_categories(zip_code))
        return len(used) >= len(all_categories)
    
    def get_stats(self) -> Dict:
        """Get statistics about scraped data"""
        total_zips = len(self.data)
        total_scrapes = sum(len(z.get('categories', [])) for z in self.data.values())
        
        return {
            'total_zips_used': total_zips,
            'total_scrapes': total_scrapes,
            'zips': self.data
        }
    
    def print_stats(self):
        """Print tracking statistics"""
        stats = self.get_stats()
        
        print("\n" + "=" * 60)
        print("📊 TRACKING STATISTICS")
        print("=" * 60)
        print(f"   📮 Total ZIP codes scraped: {stats['total_zips_used']}")
        print(f"   📦 Total ZIP+Category combinations: {stats['total_scrapes']}")
        
        if stats['zips']:
            print("\n   📋 Breakdown by ZIP:")
            for zip_code, data in sorted(stats['zips'].items()):
                categories = data.get('categories', [])
                print(f"      • {zip_code}: {len(categories)} categories scraped")
                for cat in categories:
                    print(f"         - {cat}")
        
        print("=" * 60)


if __name__ == "__main__":
    # Test the tracker
    tracker = ZipTracker()
    tracker.print_stats()

