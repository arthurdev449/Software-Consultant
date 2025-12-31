#ifndef MEMORY_ENGINE_H
#define MEMORY_ENGINE_H

#include <stddef.h>
#include <stdint.h>

// Define the size of the circular buffer
#define BUFFER_SIZE 1024 * 1024 // 1MB

// Struct for the Circular Buffer (Active Conversation)
typedef struct {
    char *buffer;
    size_t head;
    size_t tail;
    size_t size;
    size_t capacity;
} CircularBuffer;

// Struct for the Project Brief (Read-Only Block)
typedef struct {
    char *content;
    size_t length;
    int is_locked;
} ProjectBrief;

// Function Prototypes

// Initialize the memory engine
void init_memory_engine();

// Write a message to the circular buffer
// Returns 0 on success, -1 on failure
int write_to_buffer(const char *message);

// Lock the current requirements into the Project Brief
// Frees the circular buffer content related to discovery
void lock_project_brief(const char *summary);

// Read the Project Brief (Thread-safe read)
const char* read_project_brief();

// Get current memory usage stats
// Returns a JSON string with usage details
const char* get_memory_stats();

// Cleanup memory
void free_memory_engine();

#endif // MEMORY_ENGINE_H
