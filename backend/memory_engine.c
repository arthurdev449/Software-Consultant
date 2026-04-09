#include "memory_engine.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define BUFFER_SIZE 4096

// Global instances
static CircularBuffer *chat_buffer = NULL;
static ProjectBrief *project_brief = NULL;

void init_memory_engine() {
    chat_buffer = (CircularBuffer *)malloc(sizeof(CircularBuffer));
    chat_buffer->buffer = (char *)malloc(BUFFER_SIZE);
    chat_buffer->head = 0;
    chat_buffer->tail = 0;
    chat_buffer->size = 0;

    project_brief = (ProjectBrief *)malloc(sizeof(ProjectBrief));
    project_brief->content = NULL;
    project_brief->is_locked = 0;

    printf("Memory Engine Initialized\n");
}

int write_to_buffer(const char *message) {
    if (!chat_buffer || !chat_buffer->buffer) return -1;

    size_t len = strlen(message);
    if (len > BUFFER_SIZE) return -1; // Message too large

    for (size_t i = 0; i < len; ++i) {
        chat_buffer->buffer[chat_buffer->head] = message[i];
        chat_buffer->head = (chat_buffer->head + 1) % BUFFER_SIZE;
        
        if (chat_buffer->size < BUFFER_SIZE) {
            chat_buffer->size++;
        } else {
            // Buffer full, tail must move forward to make room for new head
            chat_buffer->tail = (chat_buffer->tail + 1) % BUFFER_SIZE;
        }
    }
    
    // Add null terminator at head for safety when reading back
    chat_buffer->buffer[chat_buffer->head] = '\0';
    return 0; // Success
}

void lock_project_brief(const char *summary) {
    if (!project_brief || project_brief->is_locked) return;

    size_t len = strlen(summary) + 1;
    project_brief->content = (char *)malloc(len);
    strcpy(project_brief->content, summary);
    project_brief->is_locked = 1;

    printf("Project Brief Locked\n");
}

const char* read_project_brief() {
    if (project_brief && project_brief->is_locked) {
        return project_brief->content;
    }
    return "";
}

const char* get_memory_stats() {
    static char stats_json[256];
    if (!chat_buffer) return "{}";

    double usage = ((double)chat_buffer->size / BUFFER_SIZE) * 100.0;
    int is_locked = project_brief ? project_brief->is_locked : 0;
    int total_alloc = sizeof(CircularBuffer) + BUFFER_SIZE + sizeof(ProjectBrief);
    if (project_brief && project_brief->content) {
        total_alloc += strlen(project_brief->content) + 1;
    }

    snprintf(stats_json, sizeof(stats_json), 
             "{\"buffer_usage\": %.1f, \"brief_locked\": %s, \"total_allocated\": %d}", 
             usage, is_locked ? "true" : "false", total_alloc);
    
    return stats_json;
}

void free_memory_engine() {
    if (chat_buffer) {
        if (chat_buffer->buffer) free(chat_buffer->buffer);
        free(chat_buffer);
        chat_buffer = NULL;
    }
    if (project_brief) {
        if (project_brief->content) free(project_brief->content);
        free(project_brief);
        project_brief = NULL;
    }
    printf("Memory Engine Freed\n");
}
