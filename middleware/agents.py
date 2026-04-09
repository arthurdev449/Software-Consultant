# agents.py

import os
import google.generativeai as genai
from prompts import SYSTEM_PROMPTS

# Extract API key
secrets_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../secrets.json'))
api_key = None
if os.path.exists(secrets_path):
    with open(secrets_path, 'r') as f:
        content = f.read()
        if "=" in content:
            api_key = content.split("=", 1)[1].strip()

if api_key:
    genai.configure(api_key=api_key)

class Agent:
    def __init__(self, name, role, system_prompt):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.model = genai.GenerativeModel('gemini-3.1-flash-lite-preview') if api_key else None

    def generate_response(self, context):
        if not self.model:
            return f"[{self.name}]: (Mocked API) Analyzing: {context[:20]}... Update secrets.json API Key."
        
        prompt = f"System:\n{self.system_prompt}\n\nContext:\n{context}"
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"[{self.name} Error]: {str(e)}"

class Interviewer(Agent):
    def __init__(self):
        super().__init__("Interviewer", "Gather requirements", SYSTEM_PROMPTS["INTERVIEWER"])

class Architect(Agent):
    def __init__(self):
        super().__init__("Architect", "Summarize requirements", SYSTEM_PROMPTS["ARCHITECT"])
    
    def create_brief(self, chat_history):
        if not self.model:
            return "Project Brief: Build a super cool AI app."
        
        prompt = f"System:\n{self.system_prompt}\n\nChat History to summarize:\n{chat_history}\n\nPlease generate a concise design brief."
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"[Architect Error]: {str(e)}"

class CouncilMember(Agent):
    def __init__(self, name, perspective, prompt_key):
        super().__init__(name, perspective, SYSTEM_PROMPTS[prompt_key])

class Judge(Agent):
    def __init__(self):
        super().__init__("Judge", "Provide final consensus", SYSTEM_PROMPTS["JUDGE"])

# Factory/Manager to handle agent lifecycle
def get_agent_response(agent_type, user_input, history=""):
    context = history + f"\nUser: {user_input}"
    if agent_type == "interviewer":
        agent = Interviewer()
    elif agent_type == "architect":
        agent = Architect()
        return agent.create_brief(context)
    elif agent_type == "council":
        agent = CouncilMember("Risk Manager", "Identify flaws", "COUNCIL_RISK")
    elif agent_type == "judge":
        agent = Judge()
    else:
        agent = Agent("System", "None", "")
        
    return agent.generate_response(context)
