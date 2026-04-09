from flask import Flask, render_template, request, jsonify
import bridge
import agents

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

# Initialize C memory on startup
bridge.init_memory()

# Process state in-memory
chat_history = []
current_stage = "discovery"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    global current_stage
    data = request.json
    user_message = data.get('message', '')
    
    # 1. Write user message to C memory
    bridge.write_message(user_message)
    chat_history.append(f"User: {user_message}")

    response = ""

    # Check if the previous conversation already completed the interview
    history_str = "\n".join(chat_history[-5:]) # limit context
    
    if current_stage == "discovery":
        # Let the interviewer respond first
        response = agents.get_agent_response("interviewer", user_message, history_str)
        
        # If the interviewer decides it's complete, transition immediately
        if "[INTERVIEW_COMPLETE]" in response or user_message.strip().lower() == "done":
            current_stage = "architect"
            # Append the interviewer's final message to history
            chat_history.append(f"System: {response}")
            bridge.write_message(f"System: {response[:50]}...")
            
            # Now trigger the architect to build the brief based on the complete history
            full_history_str = "\n".join(chat_history)
            brief = agents.get_agent_response("architect", "Summarize everything into a brief.", full_history_str)
            bridge.lock_brief(brief)
            
            # Append architect's response
            response += f"\n\n[Architect Transition]: Requirements locked in C-Memory.\n\n{brief}"
            current_stage = "debate"
            return jsonify({"response": response, "stage": current_stage.capitalize()})
            
    elif current_stage == "debate":
        if user_message.strip().lower() == "done":
            current_stage = "judge"
            full_debate_history = "\n".join(chat_history)
            verdict = agents.get_agent_response("judge", "Please deliver the final verdict based on the brief and the risk debate.", full_debate_history)
            response = verdict
            # Free memory natively since the session is over
            bridge.memory_lib.free_memory_engine()
        else:
            response = agents.get_agent_response("council", user_message, "\n".join(chat_history[-3:]))
    elif current_stage == "judge":
        response = "[System]: The consultation is complete. Please restart the application for a new project."
    else:
        response = "[System]: Unhandled stage."

    chat_history.append(f"System: {response}")
    bridge.write_message(f"System: {response[:50]}...")

    return jsonify({"response": response, "stage": current_stage.capitalize()})

@app.route('/api/memory-status', methods=['GET'])
def memory_status():
    # Get real-time stats from C engine
    stats = bridge.get_stats()
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
