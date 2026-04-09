# Software Consultant: System Architecture & Interaction Flow

This document details the high-level architecture, module logic, and active integrations that comprise the **Software Consultant Interactive Support System**.

---

## 1. Directory Blueprint & Tech Stack

**Language & Frameworks Core:**
*   **Web Framework:** Python 3 (`Flask`)
*   **Memory Engine:** C language (dynamic heap allocation, explicit memory tracking via pointers)
*   **Interoperability Bridge:** Python (`ctypes`)
*   **Language Models:** Google Generative AI (`google-generativeai`) natively utilizing `gemini-3.1-flash-lite-preview`
*   **Frontend UI:** Vanilla HTML/CSS/JS bundled with `marked.js` parser

---

## 2. Component Deep Dive

### A. The C-Core Memory Engine (`backend/memory_engine.c`)
Operating as a compiled shared library (`.dll` on Windows / `.so` on Linux), this backend manages highly optimized short-term and static memory explicitly.
*   **`CircularBuffer`**: A structure housing a dynamically resizing char blob (1MB). Designed with `head` and `tail` pointers wrapping around bounds so old chat sequences naturally overwrite once memory caps out.
*   **`ProjectBrief`**: A vault holding a serialized "lock" containing the absolute summary requirements agreed upon in the discovery phase.
*   **Interaction**: Handles direct writes and reads, actively reporting precise byte size usage, locking states, and total capacity utilizing `snprintf()` formatting for Python layer parsing.

### B. The Python Interoperability Bridge (`middleware/bridge.py`)
Responsible solely for natively loading the C shared library utilizing Python's `ctypes`.
*   **`init_memory()`**: Spawns memory structures upon the start of the Flask application lifecycle.
*   **`write_message()` & `lock_brief()`**: Encodes standard Python strings into robust `UTF-8` bytes securely bridging into native C memory arguments. 
*   **`get_stats()`**: Casts pointers to string structures fetching serialized JSON memory profiles and decodes them into Python dictionaries for Flask routes to serve.

### C. Large Language Model Integration (`middleware/agents.py`)
Encapsulates multiple distinct agent profiles utilizing Object-Oriented Principles.
*   **`Agent Base Class`**: The parent configuration handler initializing `genai.GenerativeModel` explicitly binding the instance to Google Gemini using tokens ingested directly from `secrets.json`.
*   **`Interviewer` / `Architect` / `CouncilMember`**: Specifically scoped subclasses. They dynamically map unique rules from `prompts.py` utilizing the `SYSTEM` boundary. 
*   **Interaction Rule**: When `generate_response()` fires, the module safely concatenates conversation history with native prompt injections before streaming HTTP payloads to the Google Cloud. 

### D. Flask Orchestration Endpoint (`middleware/app.py`)
The orchestrator handling the overall state-machine state-space flow control. It opens dual API endpoints.
*   **The State Tracking**: Manipulates native `current_stage` enumerators (Discovery ➔ Architecture ➔ Debate).
*   **`/api/chat` Route**: When strings hit this terminal, it:
    1. Mirrors requests to the `bridge.write_message()` C engine simultaneously.
    2. Modifies `chat_history`.
    3. Detects global boundary transition keywords (e.g., `"done"`), actively cutting off the Interviewer, dispatching the Architect LLM to generate the final design brief document, and firing `bridge.lock_brief()`.
*   **`/api/memory-status` Route**: Simply pulls and delivers active RAM specs from C bindings sequentially.

### E. Frontend Native DOM (`frontend/`)
*   **`script.js` Event Poller**: Actively runs `setInterval` requests every `1000ms`, dynamically polling the `/api/memory-status` tracking payload—filling up visual HTML `div` CSS width graphs natively updating real-time memory without refreshing.
*   **Markdown Chat UI**: `marked.patch(text)` intercepts Gemini's native markdown markdown (asterisks, numbers, hashes) and injects strictly structured DOM Nodes directly into the message `div`, retaining structural aesthetics perfectly spaced by `style.css` padding properties within the UI bounds.
