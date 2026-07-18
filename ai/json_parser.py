import json
import re

class JSONParser:
    def parse(self, text: str) -> dict:
        # Markdown ব্লকের ভেতর থেকে JSON বের করা
        json_str = re.search(r'\{.*\}', text, re.DOTALL)
        if json_str:
            text = json_str.group(0)
        
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # যদি JSON ভাঙা থাকে, তবে লাস্ট কমা বা বন্ধনী ঠিক করার চেষ্টা
            text = re.sub(r',(\s*[\]}])', r'\1', text)
            try:
                return json.loads(text)
            except:
                return {"error": "PARSING_FAILED", "raw": text}