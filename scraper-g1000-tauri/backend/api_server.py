"""
Scraper G1000 - Flask REST API Server
Provides HTTP endpoints for Electron frontend to communicate with Python backend
"""

import sys
import os
import asyncio
import threading
from flask import Flask, jsonify, request
from flask_cors import CORS

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.profile_manager import ProfileManager
from src.database import LeadsDatabase
from src.scraper_free_bypass import scrape_yellowpages_free

app = Flask(__name__)
CORS(app)  # Enable CORS for Electron frontend

# Global state
profile_manager = ProfileManager()
scraping_state = {
    'active': False,
    'paused': False,
    'current_zip': None,
    'current_category': None,
    'total_leads': 0,
    'progress': 0,
    'stop_requested': False
}

# === HEALTH CHECK ===

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'Scraper G1000 Backend Running'}), 200

# === PROFILE MANAGEMENT ===

@app.route('/api/profiles', methods=['GET'])
def get_profiles():
    """Get all profiles"""
    try:
        profiles = profile_manager.get_all_profiles()
        return jsonify({
            'success': True,
            'profiles': [
                {
                    'id': p.profile_id,
                    'name': p.name,
                    'icon': p.icon,
                    'businessType': p.business_type,
                    'totalLeads': p.total_leads,
                    'lastUsed': p.created_at
                }
                for p in profiles
            ]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/profiles', methods=['POST'])
def create_profile():
    """Create a new profile"""
    try:
        data = request.json
        profile = profile_manager.create_profile(
            name=data['name'],
            icon=data.get('icon', '📊'),
            business_type=data.get('businessType', ''),
            default_city=data.get('defaultCity', ''),
            default_state=data.get('defaultState', ''),
            categories=data.get('categories', [])
        )
        return jsonify({
            'success': True,
            'profileId': profile.profile_id
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# === SCRAPING OPERATIONS ===

@app.route('/api/scrape/start', methods=['POST'])
def start_scraping():
    """Start a scraping job"""
    global scraping_state

    if scraping_state['active']:
        return jsonify({'success': False, 'error': 'Scraping already active'}), 400

    try:
        data = request.json
        profile_id = data.get('profileId')
        zip_code = data.get('zipCode')
        category = data.get('category')
        max_pages = data.get('maxPages', 2)

        # Reset state
        scraping_state.update({
            'active': True,
            'paused': False,
            'current_zip': zip_code,
            'current_category': category,
            'total_leads': 0,
            'progress': 0,
            'stop_requested': False
        })

        # Start scraping in background thread
        thread = threading.Thread(
            target=run_scrape_job,
            args=(profile_id, zip_code, category, max_pages),
            daemon=True
        )
        thread.start()

        return jsonify({
            'success': True,
            'message': 'Scraping started',
            'status': scraping_state
        }), 200

    except Exception as e:
        scraping_state['active'] = False
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/scrape/pause', methods=['POST'])
def pause_scraping():
    """Pause scraping"""
    global scraping_state

    if not scraping_state['active']:
        return jsonify({'success': False, 'error': 'No active scrape'}), 400

    scraping_state['paused'] = True
    return jsonify({'success': True, 'message': 'Scraping paused'}), 200

@app.route('/api/scrape/resume', methods=['POST'])
def resume_scraping():
    """Resume scraping"""
    global scraping_state

    if not scraping_state['active']:
        return jsonify({'success': False, 'error': 'No active scrape'}), 400

    scraping_state['paused'] = False
    return jsonify({'success': True, 'message': 'Scraping resumed'}), 200

@app.route('/api/scrape/stop', methods=['POST'])
def stop_scraping():
    """Stop scraping"""
    global scraping_state

    scraping_state['stop_requested'] = True
    scraping_state['active'] = False
    scraping_state['paused'] = False

    return jsonify({'success': True, 'message': 'Scraping stopped'}), 200

@app.route('/api/scrape/status', methods=['GET'])
def get_scrape_status():
    """Get current scraping status"""
    return jsonify({
        'success': True,
        'status': scraping_state
    }), 200

# === LEAD MANAGEMENT ===

@app.route('/api/leads/<profile_id>', methods=['GET'])
def get_leads(profile_id):
    """Get leads for a profile"""
    try:
        profile = profile_manager.get_profile(profile_id)
        if not profile:
            return jsonify({'success': False, 'error': 'Profile not found'}), 404

        db = LeadsDatabase(profile.get_database_path())
        leads = db.get_all_leads()

        return jsonify({
            'success': True,
            'leads': [
                {
                    'id': i,
                    'name': lead[0],
                    'phone': lead[1],
                    'address': lead[2],
                    'website': lead[3],
                    'email': lead[4],
                    'category': lead[5] if len(lead) > 5 else 'N/A',
                    'zipCode': lead[6] if len(lead) > 6 else 'N/A'
                }
                for i, lead in enumerate(leads)
            ]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# === BACKGROUND SCRAPING LOGIC ===

def run_scrape_job(profile_id, zip_code, category, max_pages):
    """Run scraping job in background thread"""
    global scraping_state

    try:
        print(f"[Scrape Job] Starting: {zip_code} - {category}")

        # Create new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Run scraping
        leads = loop.run_until_complete(
            scrape_yellowpages_free(zip_code, category, max_pages)
        )

        scraping_state['total_leads'] = len(leads)
        scraping_state['progress'] = 100

        # Save leads to database
        profile = profile_manager.get_profile(profile_id)
        if profile and leads:
            db = LeadsDatabase(profile.get_database_path())
            for lead in leads:
                db.add_lead(
                    name=lead['name'],
                    phone_number=lead['phone_number'],
                    address=lead['address'],
                    website=lead['website'],
                    email=lead['email']
                )
            profile_manager.update_profile_leads(profile_id, db.get_total_leads())

        print(f"[Scrape Job] Complete: {len(leads)} leads")

    except Exception as e:
        print(f"[Scrape Job] Error: {e}")
        scraping_state['error'] = str(e)

    finally:
        scraping_state['active'] = False
        scraping_state['paused'] = False

# === SERVER STARTUP ===

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5050
    print(f"[API Server] Starting on http://localhost:{port}")
    print("[API Server] Press Ctrl+C to stop")

    app.run(
        host='127.0.0.1',  # Localhost only for security
        port=port,
        debug=False,
        threaded=True
    )
