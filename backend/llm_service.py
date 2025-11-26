import os
import json
import time
import re
import google.generativeai as genai
from dotenv import load_dotenv
import threading

load_dotenv()

class LLMService:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")

        genai.configure(api_key=api_key)

        # ✅ Optimized generation config
        self.generation_config = {
            'temperature': 0.3,   # lower = faster, more deterministic
            'top_p': 0.8,
            'top_k': 20,
            'max_output_tokens': 1024,  # reduced for speed
        }

        # ✅ Use correct model name from list_models()
        self.model = genai.GenerativeModel(
            model_name="models/gemini-2.5-flash",   # fast + free tier compatible
            generation_config=self.generation_config
        )

        print("✅ Gemini 2.5 Flash model initialized (optimized for speed)")

        # Rate limiting (15 requests/minute ≈ 1 every 4s)
        self.last_request_time = 0
        self.lock = threading.Lock()
        self.total_requests = 0

    def _safe_text(self, response):
        """Extract text safely using latest SDK format"""
        return response.text.strip()

    def _rate_limit(self):
        """Pace requests to ~1 every 4s (15/minute free tier)"""
        with self.lock:
            now = time.time()
            elapsed = now - self.last_request_time
            min_interval = 4.2  # seconds
            if elapsed < min_interval:
                sleep_time = min_interval - elapsed
                print(f"⏳ Pacing request, waiting {sleep_time:.1f}s...")
                time.sleep(sleep_time)
            self.last_request_time = time.time()
            self.total_requests += 1

    def _retry_on_error(self, func, max_retries=2, delay=0.5):
        """Retry with quick backoff"""
        for attempt in range(max_retries):
            try:
                self._rate_limit()
                return func()
            except Exception as e:
                error_msg = str(e).lower()
                if 'quota' in error_msg or 'rate limit' in error_msg:
                    print("⏳ Rate limit hit, waiting 10s...")
                    time.sleep(10)
                    if attempt == max_retries - 1:
                        raise
                    continue
                if attempt == max_retries - 1:
                    raise
                print(f"⚠️ Attempt {attempt+1} failed, retrying in {delay}s...")
                time.sleep(delay)

    def categorize_email(self, email, prompt):
        """Categorize email into Important, Newsletter, Spam, or To-Do"""
        try:
            full_prompt = f"""Categorize this email. Reply with ONLY one word: Important, Newsletter, Spam, or To-Do

From: {email.get('from', 'Unknown')}
Subject: {email.get('subject', 'No Subject')}
Body: {email.get('body', '')[:500]}

Category:"""

            def generate():
                resp = self.model.generate_content(full_prompt)
                return self._safe_text(resp)

            result = self._retry_on_error(generate).strip().lower()

            if 'spam' in result:
                return 'Spam'
            elif 'newsletter' in result:
                return 'Newsletter'
            elif 'todo' in result or 'to-do' in result:
                return 'To-Do'
            elif 'important' in result:
                return 'Important'

            # Fallback heuristics
            subject = email.get('subject', '').lower()
            sender = email.get('from', '').lower()

            if '!!!' in subject or 'won' in subject or '.xyz' in sender:
                return 'Spam'
            if 'newsletter' in sender or 'digest' in sender:
                return 'Newsletter'
            if any(word in subject for word in ['action required', 'please', 'request', 'need']):
                return 'To-Do'
            return 'Important'

        except Exception as e:
            print(f"❌ Categorization error: {str(e)}")
            return "Uncategorized"

    def extract_action_items(self, email, prompt):
        """Extract action items as JSON"""
        try:
            full_prompt = f"""Extract action items as JSON. Reply ONLY with JSON.

Email:
From: {email.get('from', 'Unknown')}
Subject: {email.get('subject', 'No Subject')}
Body: {email.get('body', '')[:800]}

Format: {{"tasks":[{{"task":"...", "deadline":"..."}}]}}
If no tasks: {{"tasks":[]}}

JSON:"""

            def generate():
                resp = self.model.generate_content(full_prompt)
                return self._safe_text(resp)

            result = self._retry_on_error(generate)

            # Clean markdown if present
            result = re.sub(r'```json\s*|\s*```', '', result)

            match = re.search(r'\{[\s\S]*\}', result)
            if not match:
                print("❌ No JSON block found")
                return []

            try:
                parsed = json.loads(match.group(0))
            except json.JSONDecodeError:
                print("❌ JSON parsing error")
                return []

            tasks = parsed.get("tasks", [])
            return [
                {"task": t.get("task", "").strip(), "deadline": t.get("deadline", "Not specified")}
                for t in tasks if isinstance(t, dict) and t.get("task")
            ]

        except Exception as e:
            print(f"❌ Action item error: {str(e)}")
            return []

    def generate_reply(self, email, prompt):
        """Generate a professional reply"""
        try:
            full_prompt = f"""Write a brief professional reply.

Original:
From: {email.get('from')}
Subject: {email.get('subject')}
Body: {email.get('body', '')[:800]}

Reply (2-3 paragraphs):"""

            def generate():
                resp = self.model.generate_content(full_prompt)
                return self._safe_text(resp)

            reply = self._retry_on_error(generate)
            return reply.replace("**", "").strip()

        except Exception as e:
            print(f"❌ Reply error: {str(e)}")
            sender_name = email.get('from', 'there').split('@')[0].replace('.', ' ').title()
            return f"Hi {sender_name},\n\nThank you for your email. I'll review this and get back to you soon.\n\nBest regards"

    def chat_response(self, email, query, conversation_history=""):
        """Chat about email content"""
        try:
            history_str = ""
            if conversation_history:
                lines = conversation_history.split('\n')[-4:]
                history_str = f"\n\nPrevious:\n{chr(10).join(lines)}"

            full_prompt = f"""Email:
From: {email.get('from')}
Subject: {email.get('subject')}
Body: {email.get('body','')[:800]}{history_str}

Question: {query}

Answer (be concise):"""

            def generate():
                resp = self.model.generate_content(full_prompt)
                return self._safe_text(resp)

            return self._retry_on_error(generate)

        except Exception as e:
            print(f"❌ Chat error: {str(e)}")
            return "I encountered an error processing your request. Please try again."

    def test_connection(self):
        """Test API connection"""
        try:
            self._rate_limit()
            resp = self.model.generate_content("Reply: OK")
            return True, self._safe_text(resp)
        except Exception as e:
            return False, str(e)
