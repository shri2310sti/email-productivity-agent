import time
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import json
from dotenv import load_dotenv

load_dotenv()

print("=" * 50)
print("🚀 Starting Email Productivity Agent Backend")
print("=" * 50)

app = Flask(__name__)

CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type"],
    }
})

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-12345')

# Import services
try:
    from llm_service import LLMService
    print("✅ LLM service imported")
    llm = LLMService()
    print("✅ LLM service initialized")
except Exception as e:
    print(f"❌ LLM service error: {str(e)}")
    sys.exit(1)

try:
    from database import Database
    print("✅ Database imported")
    db = Database()
    print("✅ Database initialized")
except Exception as e:
    print(f"❌ Database error: {str(e)}")
    sys.exit(1)

# Gmail service (optional)
gmail = None
try:
    from gmail_service import GmailService
    print("✅ Gmail service available (optional)")
except Exception as e:
    print("ℹ️  Gmail service not available - using mock data only")

def load_mock_inbox_from_file():
    """Load mock inbox from JSON file"""
    try:
        mock_file = 'mock_inbox.json'
        if not os.path.exists(mock_file):
            print(f"⚠️  {mock_file} not found, using generated mock data")
            return generate_mock_emails()
        
        with open(mock_file, 'r', encoding='utf-8') as f:
            emails = json.load(f)
            print(f"✅ Loaded {len(emails)} emails from {mock_file}")
            return emails
    except Exception as e:
        print(f"⚠️  Error loading mock file: {str(e)}, using generated data")
        return generate_mock_emails()

def generate_mock_emails():
    """Generate sample emails (fallback if JSON file not found)"""
    return [
        {
            'id': 'mock_1',
            'from': 'john.smith@techcorp.com',
            'subject': 'Q4 Project Deadline - Action Required',
            'body': 'Hi Team, We need to finalize the Q4 report by Friday, November 29th. Please review the attached document and send me your feedback by EOD Wednesday. Also, can you provide the latest sales figures for the presentation?',
            'timestamp': '2025-11-25T10:30:00',
            'category': None,
            'actionItems': []
        },
        {
            'id': 'mock_2',
            'from': 'newsletter@techdigest.com',
            'subject': 'Weekly Tech Digest - AI Trends & Updates',
            'body': 'Welcome to this week\'s Tech Digest! Check out the latest AI developments, new framework releases, and trending open-source projects.',
            'timestamp': '2025-11-25T09:15:00',
            'category': None,
            'actionItems': []
        },
        {
            'id': 'mock_3',
            'from': 'spam.bot@randomsite.xyz',
            'subject': 'YOU WON $1,000,000!!! CLAIM NOW!!!',
            'body': 'Congratulations! You have been selected as our lucky winner! Click here to claim your prize now!',
            'timestamp': '2025-11-25T08:45:00',
            'category': None,
            'actionItems': []
        }
    ]

# Routes
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Email Productivity Agent',
        'version': '1.0.0',
        'mock_mode': gmail is None
    })

# ✅ THE MISSING ROUTE - THIS WAS THE PROBLEM
@app.route('/api/emails/load-mock', methods=['POST'])
def load_mock_emails():
    """Load mock email data from JSON file"""
    try:
        print("📧 Loading mock email data from file...")
        emails = load_mock_inbox_from_file()
        db.save_emails(emails)
        print(f"✅ Loaded {len(emails)} mock emails")
        return jsonify({
            'success': True, 
            'emails': emails, 
            'count': len(emails),
            'message': f'Successfully loaded {len(emails)} mock emails'
        })
    except Exception as e:
        print(f"❌ Error loading mock emails: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/emails/fetch', methods=['GET'])
def fetch_emails():
    """Fetch emails from Gmail (requires Gmail setup)"""
    global gmail
    try:
        if gmail is None:
            try:
                from gmail_service import GmailService
                print("🔐 Initializing Gmail service...")
                gmail = GmailService()
                print("✅ Gmail service initialized")
            except FileNotFoundError as e:
                return jsonify({
                    'success': False,
                    'error': 'Gmail credentials not found. Please set up credentials.json or use mock data.'
                }), 400
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': f'Gmail setup error: {str(e)}'
                }), 400
        
        max_results = request.args.get('max_results', 20, type=int)
        print(f"📧 Fetching {max_results} emails from Gmail...")
        
        emails = gmail.get_emails(max_results)
        db.save_emails(emails)
        
        print(f"✅ Fetched {len(emails)} emails from Gmail")
        return jsonify({
            'success': True, 
            'emails': emails,
            'count': len(emails)
        })
    except Exception as e:
        print(f"❌ Error fetching emails: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/emails/process', methods=['POST'])
def process_emails():
    """Process emails with LLM - OPTIMIZED for speed"""
    try:
        emails = db.get_emails()
        
        if not emails:
            return jsonify({
                'success': False,
                'error': 'No emails to process. Load mock inbox or fetch from Gmail first.'
            }), 400
        
        prompts = db.get_prompts()
        
        print(f"🤖 Processing {len(emails)} emails with AI (optimized mode)...")
        print(f"⚡ Using {llm.model.model_name} for processing")

        
        processed_count = 0
        start_time = time.time()
        
        for i, email in enumerate(emails):
            try:
                # Progress indicator
                progress = f"{i+1}/{len(emails)}"
                subject_preview = email['subject'][:40]
                print(f"  [{progress}] {subject_preview}...")
                
                # ✅ OPTIMIZATION 1: Categorize (fast)
                email['category'] = llm.categorize_email(email, prompts['categorization'])
                
                # ✅ OPTIMIZATION 2: Only extract action items for To-Do and Important emails
                if email['category'] in ['To-Do', 'Important']:
                    email['actionItems'] = llm.extract_action_items(email, prompts['actionItem'])
                else:
                    email['actionItems'] = []
                
                processed_count += 1
                
                # Show speed info every 5 emails
                if (i + 1) % 5 == 0:
                    elapsed = time.time() - start_time
                    rate = (i + 1) / elapsed
                    print(f"  ⚡ Speed: {rate:.1f} emails/second")
                
            except Exception as e:
                print(f"  ⚠️  Error processing email {i+1}: {str(e)}")
                email['category'] = 'Error'
                email['actionItems'] = []
        
        # Save results
        db.save_emails(emails)
        
        elapsed = time.time() - start_time
        avg_time = elapsed / len(emails) if len(emails) > 0 else 0
        
        print(f"✅ Processed {processed_count}/{len(emails)} emails in {elapsed:.1f}s")
        print(f"⚡ Average: {avg_time:.2f}s per email")
        
        return jsonify({
            'success': True, 
            'emails': emails,
            'processed': processed_count,
            'total': len(emails),
            'time_taken': round(elapsed, 1),
            'avg_per_email': round(avg_time, 2)
        })
        
    except Exception as e:
        print(f"❌ Error processing emails: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500



@app.route('/api/emails', methods=['GET'])
def get_emails():
    """Get all stored emails"""
    try:
        emails = db.get_emails()
        return jsonify({
            'success': True, 
            'emails': emails,
            'count': len(emails)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat with email agent about a specific email"""
    try:
        data = request.json
        email = data.get('email')
        query = data.get('query')
        history = data.get('history', '')
        
        if not email or not query:
            return jsonify({
                'success': False,
                'error': 'Email and query are required'
            }), 400
        
        print(f"💬 Chat query: {query[:50]}...")
        
        response = llm.chat_response(email, query, history)
        
        return jsonify({'success': True, 'response': response})
    except Exception as e:
        print(f"❌ Chat error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/draft/generate', methods=['POST'])
def generate_draft():
    """Generate email draft reply"""
    try:
        data = request.json
        email = data.get('email')
        
        if not email:
            return jsonify({
                'success': False,
                'error': 'Email is required'
            }), 400
        
        prompts = db.get_prompts()
        
        print(f"✍️  Generating draft for: {email['subject'][:50]}...")
        
        reply_body = llm.generate_reply(email, prompts['autoReply'])
        
        draft = {
            'to': email['from'],
            'subject': f"Re: {email['subject']}",
            'body': reply_body,
            'originalEmailId': email['id']
        }
        
        saved_draft = db.add_draft(draft)
        print("✅ Draft generated and saved")
        
        return jsonify({'success': True, 'draft': saved_draft})
    except Exception as e:
        print(f"❌ Draft generation error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/drafts', methods=['GET'])
def get_drafts():
    """Get all email drafts"""
    try:
        drafts = db.get_drafts()
        return jsonify({
            'success': True, 
            'drafts': drafts,
            'count': len(drafts)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/drafts/<draft_id>', methods=['DELETE'])
def delete_draft(draft_id):
    """Delete a draft"""
    try:
        db.delete_draft(draft_id)
        return jsonify({'success': True, 'message': 'Draft deleted'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/prompts', methods=['GET'])
def get_prompts():
    """Get prompt configurations"""
    try:
        prompts = db.get_prompts()
        return jsonify({'success': True, 'prompts': prompts})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/prompts', methods=['PUT'])
def update_prompts():
    """Update prompt configurations"""
    try:
        data = request.json
        if not data:
            return jsonify({
                'success': False,
                'error': 'Prompt data is required'
            }), 400
            
        prompts = db.update_prompts(data)
        print("✅ Prompts updated successfully")
        return jsonify({
            'success': True, 
            'prompts': prompts,
            'message': 'Prompts updated. Process emails again to see changes.'
        })
    except Exception as e:
        print(f"❌ Error updating prompts: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/prompts/reset', methods=['POST'])
def reset_prompts():
    """Reset prompts to default values"""
    try:
        prompts = db.reset_to_defaults()
        print("✅ Prompts reset to defaults")
        return jsonify({
            'success': True,
            'prompts': prompts,
            'message': 'Prompts reset to default values'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    print("=" * 50)
    print(f"🌐 Starting server on port {port}")
    print("=" * 50)
    
    # Use gunicorn in production, Flask dev server locally
    if os.environ.get('RENDER'):
        # Production mode on Render
        print("Running in PRODUCTION mode")
    else:
        # Development mode
        print("Running in DEVELOPMENT mode")
        app.run(host='0.0.0.0', port=port, debug=False)
