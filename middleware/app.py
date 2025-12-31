from flask import Flask, render_template, request, jsonify
import bridge
import agents

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

# Initialize C memory on startup
bridge.init_memory()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    current_stage = data.get('stage', 'discovery') # discovery, debate, consensus

    # 1. Write user message to C memory
    bridge.write_message(user_message)

    # 2. Determine which agent should respond
    # PSEUDO CODE: Logic to switch agents based on stage
    response = f"Echo: {user_message}"

    # 3. If stage changes (e.g., Interview done), trigger Architect
    if user_message.lower() == "done":
        bridge.lock_brief("Summary of requirements...")
        response = "Requirements locked. Starting debate..."

    return jsonify({"response": response})

@app.route('/api/memory-status', methods=['GET'])
def memory_status():
    # Get real-time stats from C engine
    stats = bridge.get_stats()
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
