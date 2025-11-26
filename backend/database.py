import json
import os
from datetime import datetime

class Database:
    def __init__(self, db_file='data.json', prompts_file='default_prompts.json'):
        self.db_file = db_file
        self.prompts_file = prompts_file
        self.data = self.load_data()
    
    def load_data(self):
        """Load data from JSON file"""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"✅ Loaded data from {self.db_file}")
                    # Ensure prompts exist
                    if 'prompts' not in data or not data['prompts']:
                        print("⚠️  No prompts found, loading defaults")
                        data['prompts'] = self._load_default_prompts()
                    return data
            except json.JSONDecodeError:
                print(f"⚠️  Warning: {self.db_file} is corrupted, creating new one")
                return self._create_default_data()
        return self._create_default_data()
    
    def _load_default_prompts(self):
        """Load default prompts from file"""
        if os.path.exists(self.prompts_file):
            try:
                with open(self.prompts_file, 'r', encoding='utf-8') as f:
                    prompts = json.load(f)
                    print(f"✅ Loaded default prompts from {self.prompts_file}")
                    return prompts
            except Exception as e:
                print(f"⚠️  Error loading default prompts: {str(e)}")
        
        # Fallback to hardcoded defaults
        return {
            'categorization': 'Categorize this email into exactly ONE of these categories: Important, Newsletter, Spam, or To-Do.\n\nRules:\n- Important: Emails requiring immediate attention but no specific action\n- To-Do: Emails with explicit requests or tasks requiring your action\n- Newsletter: Promotional content, updates, or marketing emails\n- Spam: Unwanted or suspicious emails\n\nRespond with ONLY the category name.',
            'actionItem': 'Extract all actionable tasks from this email.\n\nRespond ONLY with valid JSON:\n{\n  "tasks": [\n    {"task": "task description", "deadline": "deadline if mentioned"}\n  ]\n}\n\nIf no tasks, return: {"tasks": []}',
            'autoReply': 'Generate a professional email reply based on the content.\n\n- For meeting requests: Ask for agenda\n- For task requests: Acknowledge and provide timeline\n- Keep responses concise (2-4 paragraphs)\n- Use professional, friendly tone',
            'chat': 'You are an email assistant. Answer questions about emails clearly and helpfully.'
        }
    
    def _create_default_data(self):
        """Create default data structure"""
        print("📝 Creating new data file with defaults")
        return {
            'prompts': self._load_default_prompts(),
            'emails': [],
            'drafts': []
        }
    
    def save_data(self):
        """Save data to JSON file"""
        try:
            with open(self.db_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Error saving data: {str(e)}")
            raise
    
    def update_prompts(self, prompts):
        """Update prompt configurations"""
        if not isinstance(prompts, dict):
            raise ValueError("Prompts must be a dictionary")
        
        self.data['prompts'].update(prompts)
        self.save_data()
        print(f"✅ Updated {len(prompts)} prompt(s)")
        return self.data['prompts']
    
    def reset_to_defaults(self):
        """Reset prompts to default values"""
        self.data['prompts'] = self._load_default_prompts()
        self.save_data()
        print("✅ Reset prompts to defaults")
        return self.data['prompts']
    
    def get_prompts(self):
        """Get all prompts"""
        return self.data['prompts']
    
    def save_emails(self, emails):
        """Save processed emails"""
        if not isinstance(emails, list):
            raise ValueError("Emails must be a list")
        
        self.data['emails'] = emails
        self.save_data()
        print(f"✅ Saved {len(emails)} email(s)")
    
    def get_emails(self):
        """Get all emails"""
        return self.data.get('emails', [])
    
    def add_draft(self, draft):
        """Add email draft"""
        if not isinstance(draft, dict):
            raise ValueError("Draft must be a dictionary")
        
        # Add metadata
        draft['id'] = str(datetime.now().timestamp()).replace('.', '')
        draft['createdAt'] = datetime.now().isoformat()
        draft['status'] = 'draft'
        
        if 'drafts' not in self.data:
            self.data['drafts'] = []
        
        self.data['drafts'].append(draft)
        self.save_data()
        print(f"✅ Created draft: {draft['id']}")
        return draft
    
    def get_drafts(self):
        """Get all drafts"""
        return self.data.get('drafts', [])
    
    def delete_draft(self, draft_id):
        """Delete draft by ID"""
        if 'drafts' not in self.data:
            return
        
        original_count = len(self.data['drafts'])
        self.data['drafts'] = [d for d in self.data['drafts'] if d.get('id') != draft_id]
        
        if len(self.data['drafts']) < original_count:
            self.save_data()
            print(f"✅ Deleted draft: {draft_id}")
        else:
            print(f"⚠️  Draft not found: {draft_id}")
    
    def get_statistics(self):
        """Get database statistics"""
        return {
            'total_emails': len(self.data.get('emails', [])),
            'total_drafts': len(self.data.get('drafts', [])),
            'categories': self._count_categories(),
            'emails_with_actions': self._count_emails_with_actions()
        }
    
    def _count_categories(self):
        """Count emails by category"""
        categories = {}
        for email in self.data.get('emails', []):
            cat = email.get('category', 'Uncategorized')
            categories[cat] = categories.get(cat, 0) + 1
        return categories
    
    def _count_emails_with_actions(self):
        """Count emails with action items"""
        count = 0
        for email in self.data.get('emails', []):
            if email.get('actionItems') and len(email['actionItems']) > 0:
                count += 1
        return count