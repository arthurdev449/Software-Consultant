# Software Consultant

A Hybrid C/Python Multi-Agent Decision Support System.

## Overview
Software Consultant is an advanced LLM orchestration platform that moves beyond simple chatbots. It uses a custom C-based memory engine for context management and a Python Flask middleware for orchestration.

## Architecture

### 1. Backend Core (The Vault) - C
- **Role**: Handles memory management using a Circular Buffer and a Read-Only Project Brief.
- **Tech**: C (Pseudo-code implementation).

### 2. Middleware (The Orchestrator) - Python
- **Role**: Manages agents (Interviewer, Architect, Council, Judge) and bridges the web frontend with the C core.
- **Tech**: Python, Flask, Ctypes.

### 3. Frontend (The Visualization)
- **Role**: Provides a rich chat interface and a Real-Time Memory Monitor.
- **Tech**: HTML, CSS (Dark Mode), JavaScript.

## Setup & Running

1. **Prerequisites**: Python 3.x, GCC (optional, for compiling C).
2. **Install Dependencies**:
   ```bash
   sudo apt install python3-pip  # If pip is missing
   pip3 install flask
   ```
3. **Run the Application**:
   ```bash
   cd middleware
   python3 app.py
   ```
4. **Access**: Open `http://localhost:5000` in your browser.

## License
MIT License.
