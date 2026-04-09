# 🧠 Software Consultant OS

A high-performance, multi-agent AI decision support system designed to act as an expert software consultant. It orchestrates multiple LLM personas through a strict pipeline to gather requirements, draft structural project briefs, and vigorously debate technical risks.

Built as an exploration into **Foreign Function Interfaces (FFI)**, **Systems Programming**, and **State-Machine Orchestration**.

## 🚀 Features
* **Multi-Agent Pipeline**: Specialized LLM personas (Interviewer, Architect, Risk Manager, Judge) acting in an orchestrated linear state-machine.
* **Native C-Core Memory**: A custom memory engine built in raw C managing a highly optimized 1MB Circular Buffer—achieving $O(1)$ memory state permanence without utilizing an external database.
* **C/Python Interoperability**: Bridged seamlessly via `ctypes` for advanced unmanaged/managed memory handoffs.
* **Live UI Dashboard**: Vanilla frontend with DOM manipulations tracking the C-engine memory byte limits and rendering parsed Markdown in real time.

---

## 🏗️ Architecture Stack

* **Backend Engine**: `C` (Dynamic heap allocation, Pointers, Circular Buffers)
* **Middleware Orchestrator**: `Python 3` + `Flask` + `ctypes`
* **Agent Infrastructure**: `Google Generative AI` (Gemini SDK)
* **Frontend Client**: Vanilla HTML / CSS / JS + `marked.js`

### Design Decisions & Trade-offs
**Why build a custom C-Memory engine instead of using SQLite?**
> While standard local deployments usually rely on embedded SQLite databases or Redis instances for state tracking, I specifically engineered a custom C-driven Circular Buffer to deeply explore Foreign Function Interfaces (FFI), stateless context window limits natively, and manual heap management. This allows the backend to hold an active conversation infinitely by continuously overwriting the oldest buffer data wrapped around absolute character limits.

---

## ⚙️ The Consultation Pipeline

1. **Discovery (The Interviewer)**: Socratic phase where the agent gathers raw project constraints and avoids proposing solutions.
2. **Synthesis (The Architect)**: Once discovery concludes, the entire UI is locked. The Architect reads the history and synthesizes a strict `Project Brief` (The single source of truth locked into the C-Vault).
3. **Validation (The Council)**: Peer-review stage where a "Risk Manager" attempts to aggressively tear down the architecture, citing vulnerabilities or complexity.
4. **Verdict (The Judge)**: The final step that absorbs the debate history and outputs actionable execution directives.

---

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone git@github.com:arthurdev449/Software-Consultant.git
   cd Software-Consultant
   ```

2. **Compile the C-Engine:**
   * **Linux/WSL**: `gcc -shared -o backend/memory_engine.so -fPIC backend/memory_engine.c`
   * **Windows**: Compile as a `.dll` depending on your environment compiler (e.g., MinGW).

3. **Setup the Python Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install flask google-generativeai
   ```

4. **API Configuration:**
   Create a `secrets.json` file in the root directory and add your Gemini API Key:
   ```json
   {
       "Google_generative_ai_api_for_Gemini": "YOUR_API_KEY_HERE"
   }
   ```

5. **Run the Orchestrator:**
   ```bash
   python middleware/app.py
   ```
   *Navigate to `http://127.0.0.1:5000` in your browser.*

---
*Created as a 5th Semester Computer Science academic and portfolio project.*
