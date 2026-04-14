# 🧠 Software Consultant OS

A high-performance, multi-agent AI decision support system. It orchestrates a pipeline of LLM personas (Interviewer, Architect, Risk Manager, and Judge) to transform raw ideas into validated technical execution plans.

The core differentiator is the **Hybrid State Engine**: active conversation state is managed by a native C library via a 1MB Circular Buffer, bridged to Python using the Foreign Function Interface (FFI).

---

## 🚀 Features

*   **Native C-Core Memory**: Custom memory engine built in C managing a 1MB Circular Buffer. Achieves $O(1)$ state permanence without external databases or overhead.
*   **Multi-Agent Pipeline**: 
    *   **Interviewer**: Gathers requirements using Socratic questioning.
    *   **Architect**: Synthesizes transcripts into a structured "Project Brief" locked in the C-Vault.
    *   **Council (Risk/Innovator)**: Vets the architecture for bottlenecks and modern paradigms.
    *   **Judge (CTO)**: Delivers the final binding verdict and execution plan.
*   **Real-Time Memory Telemetry**: A live dashboard tracks C-engine heap allocation and buffer saturation via a vanilla JS poller.

---

## 🏗️ Technical Stack

| Layer | Technology |
| :--- | :--- |
| **Backend Core** | C (Manual Heap Management, Pointers) |
| **Middleware** | Python 3, Flask, `ctypes` (FFI) |
| **LLM Orchestration** | Google Gemini 3.1 Lite Flash (via `google-generativeai`) |
| **Frontend** | Vanilla HTML5, CSS3, JS (ES6+), `marked.js` |

---

## 🛠️ Installation & Setup

### 1. Compile the Native Engine
The Python middleware requires the compiled shared library to manage state.

*   **Linux/WSL**:
    ```bash
    gcc -shared -o backend/memory_engine.so -fPIC backend/memory_engine.c
    ```
*   **Windows (MinGW)**:
    ```bash
    gcc -shared -o backend/memory_engine.dll backend/memory_engine.c
    ```

### 2. Configure Environment
Create a `secrets.json` in the root directory. *Note: Ensure this is ignored by git.*
```json
{
    "api_key": "YOUR_GEMINI_API_KEY"
}
```

### 3. Install Dependencies & Run
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Start the orchestrator
python middleware/app.py
```
*Access the dashboard at `http://127.0.0.1:5000`*

---

## 🧠 Deep Dive: The C/Python Bridge

The system avoids the overhead of traditional databases for session state. Instead, it uses `ctypes` to map C-structures directly into Python objects:

1.  **Circular Buffer**: When the user sends a message, Python encodes the string to `UTF-8` bytes and pushes it into the C-allocated memory.
2.  **The Vault**: Once requirements are finalized, the Architect agent "locks" the data. The C-engine moves this to a read-only block (`ProjectBrief`), ensuring the requirement set cannot be "hallucinated" away by the LLM in later stages.
3.  **Direct Memory Polling**: The frontend requests memory stats every 1s. Flask calls the C-function `get_memory_stats()`, which returns a JSON string built directly in RAM using `snprintf`.

---

## ⚖️ License
Licensed under the **GNU General Public License v3**. See [LICENSE](LICENSE) for details.

**Author:** [Arthur Zanini Marzaagão](https://github.com/arthurdev449)  
*Academic Project - 5th Semester Computer Science*
