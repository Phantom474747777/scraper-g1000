"""
Scraper G1000 - Flask REST API Server
Provides HTTP endpoints for frontend and serves static UI files
"""

import sys
import os
import asyncio
import threading
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.profile_manager import ProfileManager
from src.database import LeadsDatabase
from src.scraper_free_bypass import scrape_yellowpages_free

# Determine UI directory
BASE_DIR = Path(__file__).parent.parent
UI_DIR = BASE_DIR / "scraper-g1000-tauri" / "src"
if not UI_DIR.exists():
    UI_DIR = BASE_DIR / "app"

# Create Flask app with static folder configured
app = Flask(__name__, static_folder=str(UI_DIR), static_url_path='')
CORS(app)  # Enable CORS for frontend

print(f"[Backend] Serving UI from: {UI_DIR}")
print(f"[Backend] UI exists: {UI_DIR.exists()}")

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

# === STATIC FILE SERVING ===

@app.route('/')
def serve_root():
    """Serve index.html at root"""
    return app.send_static_file('index.html')

@app.route('/js/<path:filename>')
def serve_js(filename):
    """Serve JavaScript files"""
    return send_from_directory(str(UI_DIR / 'js'), filename)

@app.route('/styles/<path:filename>')
def serve_styles(filename):
    """Serve CSS files"""
    return send_from_directory(str(UI_DIR / 'styles'), filename)

# === HEALTH CHECK ===

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'Scraper G1000 Backend Running'}), 200

# === PROFILE MANAGEMENT ===

@app.route('/api/profiles', methods=['GET'])
def get_profiles():
    """Get all profiles with real lead counts from database"""
    try:
        profiles = profile_manager.get_all_profiles()
        print(f"[DEBUG] Loaded {len(profiles)} profiles")

        result_profiles = []
        for p in profiles:
            print(f"[DEBUG] Processing profile: {p.name}")

            try:
                # Get database path
                db_path = p.get_database_path()
                print(f"[DEBUG] Database path: {db_path}")

                # Test if file exists
                import os
                if not os.path.exists(db_path):
                    print(f"[ERROR] Database file not found: {db_path}")
                    raise FileNotFoundError(f"Database not found: {db_path}")

                # Count valid leads
                import sqlite3
                print(f"[DEBUG] Connecting to database...")
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()

                # Count valid
                print(f"[DEBUG] Counting valid leads...")
                cursor.execute('SELECT COUNT(*) FROM leads WHERE phone NOT IN ("N/A", "") AND phone IS NOT NULL AND name NOT LIKE "%![%" AND name NOT LIKE "%[Website%" AND name NOT LIKE "%About Search%"')
                valid_count = cursor.fetchone()[0]
                print(f"[DEBUG] Valid leads: {valid_count}")

                # Count total
                print(f"[DEBUG] Counting total leads...")
                cursor.execute('SELECT COUNT(*) FROM leads')
                total_count = cursor.fetchone()[0]
                print(f"[DEBUG] Total leads: {total_count}")

                conn.close()

                result_profiles.append({
                    'id': p.profile_id,
                    'name': p.name,
                    'icon': p.icon,
                    'businessType': p.business_type,
                    'totalLeads': valid_count,
                    'flaggedLeads': total_count - valid_count,
                    'lastUsed': p.created_at
                })
                print(f"[DEBUG] Added profile {p.name} with {valid_count} valid leads, {total_count - valid_count} flagged")

            except Exception as db_error:
                print(f"[ERROR] Database error for profile {p.name}: {db_error}")
                import traceback
                traceback.print_exc()
                # Add profile with 0 leads on error
                result_profiles.append({
                    'id': p.profile_id,
                    'name': p.name,
                    'icon': p.icon,
                    'businessType': p.business_type,
                    'totalLeads': 0,
                    'flaggedLeads': 0,
                    'error': str(db_error),
                    'lastUsed': p.created_at
                })

        print(f"[DEBUG] Returning {len(result_profiles)} profiles")
        return jsonify({
            'success': True,
            'profiles': result_profiles
        }), 200

    except Exception as e:
        print(f"[ERROR] Get profiles outer exception: {e}")
        import traceback
        traceback.print_exc()
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

@app.route('/api/dashboard/<profile_id>', methods=['GET'])
def get_dashboard_stats(profile_id):
    """Get dashboard statistics for a profile"""
    try:
        profile = profile_manager.get_profile(profile_id)
        if not profile:
            return jsonify({'success': False, 'error': 'Profile not found'}), 404

        db = LeadsDatabase(profile.get_database_path())
        stats = db.get_dashboard_stats()

        return jsonify({
            'success': True,
            'stats': stats
        }), 200
    except Exception as e:
        print(f"[Dashboard] Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/leads/<profile_id>', methods=['GET'])
def get_leads(profile_id):
    """Get leads for a profile with optional filtering"""
    try:
        profile = profile_manager.get_profile(profile_id)
        if not profile:
            return jsonify({'success': False, 'error': 'Profile not found'}), 404

        # Get filter parameters
        filter_zip = request.args.get('zip')
        filter_category = request.args.get('category')
        filter_status = request.args.get('status')

        db = LeadsDatabase(profile.get_database_path())

        # Get all leads with status
        leads = db.get_all_leads()

        return jsonify({
            'success': True,
            'leads': [
                {
                    'id': lead[0],  # id from database
                    'name': lead[1],
                    'phone': lead[2],
                    'address': lead[3],
                    'website': lead[4],
                    'email': lead[5],
                    'category': lead[6] if len(lead) > 6 else 'N/A',
                    'zipCode': lead[7] if len(lead) > 7 else 'N/A',
                    'status': lead[8] if len(lead) > 8 else 'New'  # status from database
                }
                for lead in leads
            ]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/leads/<profile_id>/<int:lead_id>/status', methods=['PUT'])
def update_lead_status(profile_id, lead_id):
    """Update the status of a lead"""
    try:
        profile = profile_manager.get_profile(profile_id)
        if not profile:
            return jsonify({'success': False, 'error': 'Profile not found'}), 404

        data = request.json
        new_status = data.get('status')

        if new_status not in ['New', 'Contacted', 'Archived']:
            return jsonify({'success': False, 'error': 'Invalid status'}), 400

        db = LeadsDatabase(profile.get_database_path())
        db.update_lead_status(lead_id, new_status)

        return jsonify({'success': True}), 200
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
