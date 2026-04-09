import ctypes
import os
import json
import sys

# Load the shared library depending on platform
lib_name = 'memory_engine.dll' if sys.platform == 'win32' else 'memory_engine.so'
lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend', lib_name))

try:
    memory_lib = ctypes.CDLL(lib_path)
    
    # Define argument and return types for C functions
    memory_lib.write_to_buffer.argtypes = [ctypes.c_char_p]
    memory_lib.write_to_buffer.restype = ctypes.c_int

    memory_lib.lock_project_brief.argtypes = [ctypes.c_char_p]
    
    memory_lib.get_memory_stats.restype = ctypes.c_char_p
    memory_lib.read_project_brief.restype = ctypes.c_char_p
except OSError:
    print(f"Warning: Could not load {lib_name}. Ensure it is compiled and placed in backend/")
    memory_lib = None

def init_memory():
    """Initializes the C memory engine."""
    if memory_lib:
        memory_lib.init_memory_engine()
        print("Bridge: Memory Initialized")
    else:
        print("Bridge: memory_lib not loaded.")

def write_message(message):
    """Writes a message to the C circular buffer."""
    if memory_lib:
        encoded_message = message.encode('utf-8')
        return memory_lib.write_to_buffer(encoded_message)
    return -1

def lock_brief(summary):
    """Locks the project brief in C memory."""
    if memory_lib:
        encoded_summary = summary.encode('utf-8')
        memory_lib.lock_project_brief(encoded_summary)
        print("Bridge: Project Brief Locked")

def get_stats():
    """Fetches memory usage stats from C."""
    if memory_lib:
        c_stats = memory_lib.get_memory_stats()
        if c_stats:
            stats_str = c_stats.decode('utf-8')
            try:
                return json.loads(stats_str)
            except json.JSONDecodeError:
                pass
    
    # Fallback return
    return {
        "buffer_usage": 0,
        "brief_locked": False,
        "total_allocated": 0
    }
