# Done-Tasks

## Problem 1: Implement Circular Buffer Memory Engine
**Difficulty:** Medium
**Tags:** C, Memory Management, Circular Buffer

**Description:**
You are given a skeleton logic for a `CircularBuffer` and `ProjectBrief`. You need to allocate them, implement circular logic to wrap around the byte array on write, track memory usage, and properly free everything.

**Requirements:**
- Implement `init_memory_engine`: Allocate structs and a buffer (e.g. 1024 bytes).
- Implement `write_to_buffer`: Track head, wrap correctly, override tail if needed.
- Implement `lock_project_brief`: Store summary content, mark locked.
- Implement `get_memory_stats`: Return formatted JSON string.
- Implement `free_memory_engine`: Free all dynamically allocated elements.

---

## Problem 2: Bridge DLL to Python 
**Difficulty:** Easy
**Tags:** Python, ctypes, Interoperability

**Description:**
Given the compiled DLL/SO file of the Memory Engine, establish a bridge in Python using `ctypes`. Load library efficiently across OS bounds, and specify arguments (`argtypes`) and return types (`restype`) strictly.

**Requirements:**
- Initialize `memory_lib` global DLL reference using `os.path`.
- Prepare C-function equivalents. 
- Decode any `c_char_p` coming from C into utf-8 strings for Python seamlessly.

---

## Problem 3: LLM Integration Module
**Difficulty:** Medium
**Tags:** LLM, APIs, Classes

**Description:**
A set of Agents (Interviewer, Architect, etc) rely on the `generate_response` base method to contact an LLM provider. Mock or create an HTTP integration API schema that fuses local configuration system prompts and user's context, simulating an external API like Gemini.

**Requirements:**
- Refactor `generate_response` to accept context and construct the LLM prompt.
- Refactor `get_agent_response` to conditionally instantiate and utilize right agent logic based on the string type passed.

---

## Problem 4: App Orchestration State Machine
**Difficulty:** Hard
**Tags:** State Machine, Flask, Web Backend

**Description:**
Route the flow of chat inside the `/api/chat` Flask endpoint. Based on `user_message` and `current_stage`, pick the context-appropriate agent. You must switch stages dynamically, such as jumping to 'Architect' when the word 'done' is identified.

**Requirements:**
- Pass the user's message to the C Buffer using the bridge.
- Control current_stage tracking via flask responses/requests.
- Implement 'done' detection -> Lock Brief -> Trigger next Stage.
