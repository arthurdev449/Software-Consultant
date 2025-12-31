# agents.py

from prompts import SYSTEM_PROMPTS

class Agent:
    def __init__(self, name, role, system_prompt):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt

    def generate_response(self, context):
        # PSEUDO CODE:
        # 1. Construct full prompt: self.system_prompt + "\nContext:\n" + context
        # 2. Call LLM API
        return f"[{self.name}]: (Simulated) I am using my system prompt to analyze: {context[:20]}..."

class Interviewer(Agent):
    def __init__(self):
        super().__init__("Interviewer", "Gather requirements", SYSTEM_PROMPTS["INTERVIEWER"])

class Architect(Agent):
    def __init__(self):
        super().__init__("Architect", "Summarize requirements", SYSTEM_PROMPTS["ARCHITECT"])
    
    def create_brief(self, chat_history):
        # PSEUDO CODE: Use self.system_prompt + chat_history
        return "Project Brief: Build a super cool AI app."

class CouncilMember(Agent):
    def __init__(self, name, perspective, prompt_key):
        super().__init__(name, perspective, SYSTEM_PROMPTS[prompt_key])

class Judge(Agent):
    def __init__(self):
        super().__init__("Judge", "Provide final consensus", SYSTEM_PROMPTS["JUDGE"])

# Factory/Manager to handle agent lifecycle
def get_agent_response(agent_type, user_input, history):
    # PSEUDO CODE:
    # Switch based on agent_type, instantiate correct agent
    if agent_type == "interviewer":
        agent = Interviewer()
    elif agent_type == "architect":
        agent = Architect()
    # ... etc
    else:
        agent = Agent("Generic", "None", "")
        
    return agent.generate_response(user_input)
